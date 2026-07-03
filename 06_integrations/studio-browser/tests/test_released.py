"""Tests for released album track detail."""

from fastapi.testclient import TestClient

from server.main import app

client = TestClient(app)


def test_api_released_track():
    res = client.get("/api/albums/released-demo/tracks/released-song")
    assert res.status_code == 200
    data = res.json()
    assert data["slug"] == "released-song"
    assert data["read_only"] is True
    assert len(data["lyrics_files"]) == 1


def test_api_released_track_wrong_case():
    res = client.get("/api/albums/released-demo/tracks/Released-Song")
    assert res.status_code == 200
    assert res.json()["slug"] == "released-song"


def test_api_released_master_media():
    res = client.get("/api/media/released-demo/masters/01%20-%20Released%20Song.wav")
    assert res.status_code == 200
    assert "audio" in res.headers.get("content-type", "")


def test_api_released_album():
    res = client.get("/api/albums/released-demo")
    assert res.status_code == 200
    data = res.json()
    assert data["layout"] == "released"
    assert data["tracks"][0]["slug"] == "released-song"
