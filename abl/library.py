"""The sound library as abl knows it: a seed catalog shipped with abl, or a rescan of Live's browser
(`abl catalog`) that also picks up installed Packs and plugins."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Callable

SEED = Path(__file__).resolve().parent / "catalog.json"
USER_CATALOG = Path(os.environ.get("ABL_CATALOG", "~/.abl/catalog.json")).expanduser()
SCAN_ROOTS = ("sounds", "drums", "instruments", "packs", "plugins", "user_library")
SKIP_FOLDERS = {"samples", "clips", "loops", "lessons", "grooves", "midi clips", "sample", "one shots", "multisamples"}
MAX_DEPTH = 6


def load() -> list[dict]:
    """Entries {name, uri, section, category}. The user's rescan wins over the seed."""
    for path in (USER_CATALOG, SEED):
        if path.exists():
            try:
                return json.loads(path.read_text())
            except json.JSONDecodeError:
                continue
    return []


def _walk(client, path: str, section: str, depth: int, progress: Callable[[str], None], out: list[dict], seen: set[str]) -> None:
    if depth > MAX_DEPTH:
        return
    reply = client.send("get_browser_items_at_path", {"path": path})
    items = reply.get("items", []) if isinstance(reply, dict) else []
    for item in items:
        name = str(item.get("name", ""))
        uri = item.get("uri")
        if item.get("is_loadable") and uri and uri not in seen:
            seen.add(uri)
            category = path.split("/", 1)[1] if "/" in path else ""
            out.append({"name": name, "uri": uri, "section": section, "category": category})
        elif item.get("is_folder") and name.lower() not in SKIP_FOLDERS:
            child = f"{path}/{name}"
            if depth <= 1:
                progress(f"catalog: {child} ({len(out)} sounds so far)")
            _walk(client, child, section, depth + 1, progress, out, seen)


def rescan(client, progress: Callable[[str], None] = lambda s: None, roots: tuple[str, ...] = SCAN_ROOTS) -> list[dict]:
    """Walk Live's browser and write ~/.abl/catalog.json."""
    out: list[dict] = []
    seen: set[str] = set()
    for root in roots:
        section = {"sounds": "Sounds", "drums": "Drums", "instruments": "Instruments", "packs": "Packs", "plugins": "Plugins", "user_library": "User Library"}.get(root, root)
        try:
            _walk(client, root, section, 0, progress, out, seen)
        except Exception as exc:
            progress(f"catalog: {root} skipped ({str(exc)[:60]})")
    USER_CATALOG.parent.mkdir(parents=True, exist_ok=True)
    USER_CATALOG.write_text(json.dumps(out))
    return out
