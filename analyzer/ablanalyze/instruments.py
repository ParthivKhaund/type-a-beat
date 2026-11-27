"""What does each part sound like? Zero-shot tagging of the stems with CLAP, restricted to labels
that make sense for the role, averaged over several windows."""

from __future__ import annotations

from pathlib import Path

import numpy as np

MODEL_ID = "laion/clap-htsat-unfused"
CLAP_SR = 48000
WINDOW_S = 10
MAX_WINDOWS = 6
SILENCE_RMS = 1e-3

ROLE_LABELS: dict[str, list[str]] = {
    "bass": ["a deep 808 sub bass", "an electric bass guitar", "an upright acoustic bass", "a synthesizer bass", "an acid 303 bass"],
    "keys": ["an electric piano", "a grand piano", "a hammond organ", "a warm synth pad", "a plucked synth", "a string ensemble",
             "a brass section", "a choir", "bells and mallets", "a synth lead", "an acoustic guitar", "a clean electric guitar"],
    "lead": ["a singing voice", "a synth lead", "a flute", "a violin", "a trumpet", "an electric guitar solo"],
    "drums": ["an acoustic drum kit", "an 808 drum machine", "a 909 drum machine", "lo-fi dusty drums", "trap drums with rolling hi-hats"],
}

_model = None
_proc = None


def available() -> bool:
    try:
        import transformers  # noqa: F401
    except Exception:
        return False
    return True


def _load():
    global _model, _proc
    if _model is None:
        from transformers import ClapModel, ClapProcessor

        _model = ClapModel.from_pretrained(MODEL_ID)
        _proc = ClapProcessor.from_pretrained(MODEL_ID)
        _model.eval()
    return _model, _proc


def _vec(out):
    import torch

    t = out if torch.is_tensor(out) else getattr(out, "text_embeds", None) or getattr(out, "audio_embeds", None) or out.pooler_output
    return t / t.norm(dim=-1, keepdim=True)


def _embed_audio(path: Path):
    import librosa
    import soundfile as sf
    import torch

    y, sr = sf.read(str(path), dtype="float32", always_2d=True)
    y = y.mean(axis=1)
    if len(y) == 0 or float(np.sqrt((y ** 2).mean())) < SILENCE_RMS:
        return None
    y = librosa.resample(y, orig_sr=sr, target_sr=CLAP_SR)
    hop = CLAP_SR * WINDOW_S
    windows = [y[i:i + hop] for i in range(0, max(1, len(y) - hop), hop)][:MAX_WINDOWS] or [y]
    windows = [w for w in windows if float(np.sqrt((w ** 2).mean())) >= SILENCE_RMS] or [y]
    model, proc = _load()
    with torch.no_grad():
        emb = _vec(model.get_audio_features(**proc(audio=windows, sampling_rate=CLAP_SR, return_tensors="pt")))
    return emb.mean(0, keepdim=True)


def tag(path: Path, role: str) -> list[tuple[str, float]]:
    """Labels for the role ranked by similarity, e.g. [("an electric piano", 0.43), ...]; [] for silence."""
    import torch

    labels = ROLE_LABELS[role]
    audio = _embed_audio(path)
    if audio is None:
        return []
    model, proc = _load()
    with torch.no_grad():
        text = _vec(model.get_text_features(**proc(text=["the sound of " + l for l in labels], return_tensors="pt", padding=True)))
    sims = (audio @ text.T)[0]
    order = torch.argsort(sims, descending=True)
    return [(labels[int(i)], round(float(sims[int(i)]), 4)) for i in order]


def tag_roles(paths: dict[str, Path]) -> dict[str, list[tuple[str, float]]]:
    """paths: role -> stem file. Returns role -> ranked labels."""
    out = {}
    for role, path in paths.items():
        if role in ROLE_LABELS and path is not None and Path(path).exists():
            try:
                out[role] = tag(Path(path), role)
            except Exception:
                out[role] = []
    return out
