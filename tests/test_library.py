import json

from abl.library import rescan


class FakeBrowser:
    def __init__(self):
        self.tree = {
            "sounds": [{"name": "Bass", "is_folder": True, "is_loadable": False, "uri": "query:Sounds#Bass"}],
            "sounds/Bass": [{"name": "Sub 808 Bass.adv", "is_folder": False, "is_loadable": True, "uri": "query:Sounds#Bass:FileId_6515"}],
            "drums": [{"name": "808 Core Kit.adg", "is_folder": False, "is_loadable": True, "uri": "query:Drums#FileId_5409"}],
            "packs": [{"name": "Beat Tools", "is_folder": True, "is_loadable": False, "uri": "query:LivePacks#1"}],
            "packs/Beat Tools": [
                {"name": "Drums", "is_folder": True, "is_loadable": False, "uri": "q"},
                {"name": "Samples", "is_folder": True, "is_loadable": False, "uri": "q2"},
            ],
            "packs/Beat Tools/Drums": [{"name": "BT Kit.adg", "is_folder": False, "is_loadable": True, "uri": "query:LivePacks#kit"}],
            "packs/Beat Tools/Samples": [{"name": "huge.wav", "is_folder": False, "is_loadable": True, "uri": "query:LivePacks#wav"}],
        }
        self.calls = []

    def send(self, kind, params=None):
        self.calls.append(params["path"])
        return {"items": self.tree.get(params["path"], [])}


def test_rescan_collects_loadable_items_with_section_and_category(tmp_path, monkeypatch):
    monkeypatch.setattr("abl.library.USER_CATALOG", tmp_path / "catalog.json")
    entries = rescan(FakeBrowser(), roots=("sounds", "drums", "packs"))
    by_name = {e["name"]: e for e in entries}
    assert by_name["Sub 808 Bass.adv"] == {"name": "Sub 808 Bass.adv", "uri": "query:Sounds#Bass:FileId_6515", "section": "Sounds", "category": "Bass"}
    assert by_name["BT Kit.adg"]["section"] == "Packs" and by_name["BT Kit.adg"]["category"] == "Beat Tools/Drums"
    assert json.loads((tmp_path / "catalog.json").read_text()) == entries


def test_rescan_skips_sample_folders(tmp_path, monkeypatch):
    monkeypatch.setattr("abl.library.USER_CATALOG", tmp_path / "catalog.json")
    browser = FakeBrowser()
    entries = rescan(browser, roots=("packs",))
    assert "packs/Beat Tools/Samples" not in browser.calls
    assert all(e["name"] != "huge.wav" for e in entries)
