"""Tests for FastAPI endpoints."""

from __future__ import annotations

from fastapi.testclient import TestClient

from server.main import app

client = TestClient(app)


def test_api_albums():
    res = client.get("/api/albums")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert any(a["slug"] == "demo-album" for a in data)


def test_api_album_detail():
    res = client.get("/api/albums/demo-album")
    assert res.status_code == 200
    data = res.json()
    assert data["title"] == "Demo Album"
    assert len(data["tracks"]) == 1


def test_api_track_detail():
    res = client.get("/api/albums/demo-album/tracks/demo-track")
    assert res.status_code == 200
    data = res.json()
    assert data["slug"] == "demo-track"
    assert data["prompt"] is not None


def test_api_media():
    res = client.get("/api/media/demo-album/demo-track/run002_take_a.mp3")
    assert res.status_code == 200
    assert "audio" in res.headers.get("content-type", "")


def test_api_validate():
    res = client.post("/api/albums/demo-album/tracks/demo-track/validate", json={})
    assert res.status_code == 200
    data = res.json()
    assert "ok" in data


def test_api_search():
    res = client.get("/api/search?q=gentle")
    assert res.status_code == 200
    assert "results" in res.json()


def test_serve_index():
    res = client.get("/")
    assert res.status_code == 200
