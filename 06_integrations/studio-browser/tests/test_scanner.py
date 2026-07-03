"""Tests for Studio Browser parsers and scanner."""

from __future__ import annotations

from pathlib import Path

ALBUMS_DIR = Path(__file__).parent / "fixtures" / "02_albums"
from server.parsers.album_md import parse_album_md
from server.parsers.track_map import parse_track_map
from server.parsers.track_md import parse_track_md
from server.parsers.suno_runs import parse_suno_runs
from server.scanner import get_album_detail, get_track_detail, list_albums


def test_list_albums():
    albums = list_albums()
    assert len(albums) >= 1
    slugs = [a.slug for a in albums]
    assert "demo-album" in slugs
    assert "_album_template" not in slugs


def test_parse_album_md():
    meta = parse_album_md(ALBUMS_DIR / "demo-album" / "album.md", "demo-album")
    assert meta.title == "Demo Album"
    assert meta.status == "draft-ready"


def test_parse_track_map():
    tm = parse_track_map(ALBUMS_DIR / "demo-album" / "track_map.md")
    assert tm.layout == "active"
    assert len(tm.tracks) == 1
    demo = next(t for t in tm.tracks if t.slug == "demo-track")
    assert demo.status == "suno"
    assert demo.number == 1


def test_parse_track_md():
    meta = parse_track_md(
        ALBUMS_DIR / "demo-album" / "tracks" / "demo-track" / "track.md",
        "demo-track",
    )
    assert meta.title == "Demo Track"
    assert meta.status == "suno"


def test_parse_suno_runs():
    log = parse_suno_runs(
        ALBUMS_DIR / "demo-album" / "tracks" / "demo-track" / "suno" / "suno_runs.md"
    )
    assert len(log.runs) >= 1
    run002 = next(r for r in log.runs if r.run == "002")
    assert run002.status == "complete"


def test_get_album_detail():
    detail = get_album_detail("demo-album")
    assert detail["title"] == "Demo Album"
    assert len(detail["tracks"]) == 1
    assert detail["dashboard"]["total"] == 1


def test_get_track_detail():
    detail = get_track_detail("demo-album", "demo-track")
    assert detail["title"] == "Demo Track"
    assert detail["prompt"] is not None
    assert len(detail["lyrics_files"]) >= 1
    assert len(detail["runs"]) >= 1


def test_parse_track_map_released():
    tm = parse_track_map(ALBUMS_DIR / "released-demo" / "track_map.md")
    assert tm.layout == "released"
    assert len(tm.tracks) == 1
    song = next(t for t in tm.tracks if t.slug == "released-song")
    assert song.title == "Released Song"
    assert song.number == 1
    assert song.status == "final"
    assert "lyrics/01-released-song.md" in song.lyrics_path


def test_get_released_track_detail():
    detail = get_track_detail("released-demo", "released-song")
    assert detail["title"] == "Released Song"
    assert detail["read_only"] is True
    assert detail["layout"] == "released"
    assert len(detail["lyrics_files"]) == 1
    assert detail["prompt"] is not None
    assert detail["prompt"]["fields"]["styles"]


def test_get_track_detail_has_validation():
    detail = get_track_detail("demo-album", "demo-track")
    assert detail["validation"] is not None
    assert "ok" in detail["validation"]
