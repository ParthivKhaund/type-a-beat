import json
from pathlib import Path

import pytest

from abl.actions import ActionError, execute
from abl.commands import parse
from abl.importer import fetch_audio, import_song
from abl.session import Session


class FakeTools:
    """Stands in for yt-dlp and ffmpeg: records calls, creates the files they would create."""

    def __init__(self, video_id="dQw4w9WgXcQ", title="Test Song", duration="212"):
        self.calls = []
        self.meta = f"{video_id}\n{title}\n{duration}\n"

    def __call__(self, args):
        self.calls.append(args)
        if args[0] == "yt-dlp" and "--skip-download" in args:
            return self.meta
        if args[0] == "yt-dlp":
            template = args[args.index("-o") + 1]
            Path(template.replace("%(ext)s", "wav")).write_bytes(b"RIFFsource")
            return ""
        if args[0] == "ffmpeg":
            Path(args[-1]).write_bytes(b"RIFFaudio")
            return ""
        if args[0] == "ffprobe":
            return "212.5\n"
        raise AssertionError(f"unexpected tool {args}")


def test_fetch_url_downloads_into_the_shared_cache_layout(tmp_path):
    tools = FakeTools()
    meta = fetch_audio("https://www.youtube.com/watch?v=dQw4w9WgXcQ", tmp_path, lambda s: None, run=tools)
    folder = tmp_path / "dQw4w9WgXcQ"
    assert meta["audio"] == str(folder / "audio.wav") and Path(meta["audio"]).exists()
    assert meta["title"] == "Test Song"
    saved = json.loads((folder / "source.json").read_text())
    assert saved["key"] == "dQw4w9WgXcQ" and saved["url"].endswith("dQw4w9WgXcQ")
    assert not (folder / "source.wav").exists()
    assert any("--no-playlist" in c for c in tools.calls if c[0] == "yt-dlp")


def test_fetch_url_skips_the_download_when_cached(tmp_path):
    fetch_audio("https://youtu.be/dQw4w9WgXcQ", tmp_path, lambda s: None, run=FakeTools())
    tools = FakeTools()
    fetch_audio("https://youtu.be/dQw4w9WgXcQ", tmp_path, lambda s: None, run=tools)
    assert [c[0] for c in tools.calls] == ["yt-dlp"]  # metadata only


def test_fetch_local_file_converts_into_a_hash_folder(tmp_path):
    song = tmp_path / "My Song.mp3"
    song.write_bytes(b"ID3fake")
    meta = fetch_audio(str(song), tmp_path / "cache", lambda s: None, run=FakeTools())
    assert meta["title"] == "My Song"
    assert Path(meta["audio"]).exists() and Path(meta["audio"]).parent.parent == tmp_path / "cache"


def test_fetch_missing_file_is_an_action_error(tmp_path):
    with pytest.raises(ActionError, match="no such file"):
        fetch_audio(str(tmp_path / "nope.mp3"), tmp_path, lambda s: None, run=FakeTools())


def test_fetch_download_failure_is_an_action_error(tmp_path):
    def run(args):
        raise RuntimeError("ERROR: Video unavailable")

    with pytest.raises(ActionError, match="Video unavailable"):
        fetch_audio("https://youtu.be/x", tmp_path, lambda s: None, run=run)


def test_import_uses_an_empty_template_audio_track_and_names_it_after_the_song(studio_live, tmp_path):
    out = import_song(Session(studio_live), "https://youtu.be/dQw4w9WgXcQ", lambda s: None, cache_dir=tmp_path, run=FakeTools())
    track = studio_live.tracks[2]
    assert track["name"] == "Test Song" and track["type"] == "audio"
    assert studio_live.audio_clips[(2, 0)] == str(tmp_path / "dQw4w9WgXcQ" / "audio.wav")
    assert track["clip_names"][0] == "abl Test Song"
    assert "Test Song" in out and "track 2" in out


def test_import_creates_an_audio_track_when_none_is_free(empty_live, tmp_path):
    import_song(Session(empty_live), "https://youtu.be/dQw4w9WgXcQ", lambda s: None, cache_dir=tmp_path, run=FakeTools())
    assert [t["type"] for t in empty_live.tracks] == ["audio"]
    assert empty_live.tracks[0]["name"] == "Test Song"
    assert (0, 0) in empty_live.audio_clips


def test_import_never_uses_an_audio_track_that_already_has_clips(studio_live, tmp_path):
    studio_live.tracks[2]["slots"][0] = True
    import_song(Session(studio_live), "https://youtu.be/dQw4w9WgXcQ", lambda s: None, cache_dir=tmp_path, run=FakeTools())
    assert studio_live.tracks[2]["name"] == "3-Audio"
    assert studio_live.tracks[-1]["name"] == "Test Song"


def test_import_on_a_full_set_refuses_before_downloading(studio_live, tmp_path):
    studio_live.tracks[2]["slots"][0] = True
    for name in ("A", "B", "C"):
        studio_live.add_user_track(name)
    studio_live.track_limit = 8
    tools = FakeTools()
    with pytest.raises(ActionError, match="8 tracks"):
        import_song(Session(studio_live), "https://youtu.be/dQw4w9WgXcQ", lambda s: None, cache_dir=tmp_path, run=tools)
    assert tools.calls == []


def test_import_truncates_long_titles(empty_live, tmp_path):
    long_title = "An Extremely Long Song Title That Keeps Going (Official Video)"
    import_song(Session(empty_live), "https://youtu.be/abc", lambda s: None, cache_dir=tmp_path, run=FakeTools(video_id="abc", title=long_title))
    assert len(empty_live.tracks[0]["name"]) <= 30


def test_import_command_goes_through_execute(empty_live, tmp_path, monkeypatch):
    monkeypatch.setattr("abl.importer.CACHE_DIR", tmp_path)
    monkeypatch.setattr("abl.importer.default_run", FakeTools())
    out = execute(parse("import https://youtu.be/dQw4w9WgXcQ"), Session(empty_live), progress=lambda s: None)
    assert "Test Song" in out


def test_a_youtube_403_suggests_updating_yt_dlp(tmp_path):
    calls = []

    def run(args):
        calls.append(args)
        if "--skip-download" in args:
            return "abc\nSong\n100\n"
        raise RuntimeError("ERROR: unable to download video data: HTTP Error 403: Forbidden")

    with pytest.raises(ActionError, match="brew upgrade yt-dlp"):
        fetch_audio("https://youtu.be/abc", tmp_path, lambda s: None, run=run)
