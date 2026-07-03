"""Tests for album cover art."""

from pathlib import Path

from server.art import find_album_cover
from server.main import app
from fastapi.testclient import TestClient

ALBUMS_DIR = Path(__file__).parent / "fixtures" / "02_albums"

client = TestClient(app)


def test_find_cover_released():
    cover = find_album_cover(ALBUMS_DIR / "released-demo")
    assert cover is not None
    assert cover["filename"] == "cover.png"
    assert cover["url"] == "/api/art/released-demo/cover.png"


def test_find_cover_missing():
    cover = find_album_cover(ALBUMS_DIR / "demo-album")
    assert cover is None


def test_api_album_art():
    res = client.get("/api/art/released-demo/cover.png")
    assert res.status_code == 200
    assert res.headers["content-type"].startswith("image/")


def test_api_albums_include_cover():
    res = client.get("/api/albums")
    released = next(a for a in res.json() if a["slug"] == "released-demo")
    assert "cover" in released
    assert released["cover"]["url"] == "/api/art/released-demo/cover.png"


def test_api_album_detail_include_cover():
    res = client.get("/api/albums/released-demo")
    assert res.json()["cover"]["filename"] == "cover.png"
