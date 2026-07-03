"""FastAPI application for Studio Browser."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

import markdown
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from server.config import ALBUMS_DIR, WEB_DEV, WEB_DIST
from server import scanner
from server import suno_bridge
from server.writers.archive_track import archive_track
from server.writers.listening_notes import append_listening_notes
from server.writers.select_final import select_final
from server.writers.track_status import apply_verdict

app = FastAPI(title="Studio Browser", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class VerdictRequest(BaseModel):
    verdict_type: str = Field(..., pattern="^(shortlist|favorite|pass)$")
    run_number: str
    take: str = Field(..., pattern="^[ab]$")


class NotesRequest(BaseModel):
    run_number: str
    take: str = "a"
    prompt_version: str = ""
    audio_file: str = ""
    first_feeling: str = ""
    what_worked: str = ""
    what_failed: str = ""
    decision: str = "keep exploring"
    next_move: str = ""
    quick_tags: list[str] = Field(default_factory=list)


class SelectFinalRequest(BaseModel):
    run_number: str
    take: str = "a"
    reason: str
    album_fit: str = ""
    artist_fit: str = ""


class ArchiveRequest(BaseModel):
    final_audio: str
    track_number: int = 0


class GenerateRequest(BaseModel):
    prompt: str | None = None


class WavRequest(BaseModel):
    run_number: str
    take: str = "a"
    final_name: str | None = None


class DownloadRequest(BaseModel):
    run_number: str
    take: str = "both"


@app.get("/api/albums")
def api_albums() -> list[dict[str, Any]]:
    albums = scanner.list_albums()
    result = []
    for a in albums:
        entry = {
            "slug": a.slug,
            "title": a.title,
            "status": a.status,
            "track_count": a.track_count,
            "progress": asdict(a.progress),
            "has_tracks_workspace": a.has_tracks_workspace,
        }
        cover = scanner.album_cover(a.slug)
        if cover:
            entry["cover"] = cover
        result.append(entry)
    return result


@app.get("/api/art/{album}/{filename:path}")
def api_album_art(album: str, filename: str):
    if ".." in filename:
        raise HTTPException(400, "Invalid filename")
    path = ALBUMS_DIR / album / "album_art" / Path(filename).name
    if not path.is_file():
        raise HTTPException(404, "Cover not found")
    media_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }
    media_type = media_types.get(path.suffix.lower(), "application/octet-stream")
    return FileResponse(path, media_type=media_type)


@app.get("/api/albums/{slug}")
def api_album_detail(slug: str) -> dict[str, Any]:
    try:
        return scanner.get_album_detail(slug)
    except FileNotFoundError as exc:
        raise HTTPException(404, str(exc)) from exc


@app.get("/api/albums/{album}/tracks/{track}")
def api_track_detail(album: str, track: str) -> dict[str, Any]:
    try:
        data = scanner.get_track_detail(album, track)
        # Render markdown fields to HTML for convenience
        for key in ("song_brief", "style_directions", "final_suno_fields", "listening_notes"):
            if data.get(key):
                data[f"{key}_html"] = markdown.markdown(
                    data[key], extensions=["tables", "fenced_code", "nl2br"]
                )
        for lf in data.get("lyrics_files", []):
            lf["html"] = markdown.markdown(lf["content"], extensions=["fenced_code", "nl2br"])
        return data
    except FileNotFoundError as exc:
        raise HTTPException(404, str(exc)) from exc


@app.get("/api/media/{album}/masters/{filename:path}")
def api_media_master(album: str, filename: str):
    if ".." in filename:
        raise HTTPException(400, "Invalid filename")
    path = ALBUMS_DIR / album / "masters" / Path(filename).name
    if not path.exists():
        raise HTTPException(404, "Master not found")
    media_type = "audio/wav" if path.suffix == ".wav" else "audio/mpeg"
    return FileResponse(path, media_type=media_type)


@app.get("/api/media/{album}/{track}/{filename}")
def api_media(album: str, track: str, filename: str):
    if ".." in filename or "/" in filename:
        raise HTTPException(400, "Invalid filename")
    path = ALBUMS_DIR / album / "tracks" / track / "audio" / filename
    if not path.exists():
        raise HTTPException(404, "Audio not found")
    media_type = "audio/mpeg" if path.suffix == ".mp3" else "audio/wav"
    return FileResponse(path, media_type=media_type)


@app.get("/api/credits")
def api_credits():
    return suno_bridge.get_credits()


@app.post("/api/albums/{album}/tracks/{track}/validate")
def api_validate(album: str, track: str, body: GenerateRequest | None = None):
    prompt = body.prompt if body else None
    return suno_bridge.validate_track(album, track, prompt)


@app.post("/api/albums/{album}/tracks/{track}/generate")
def api_generate(album: str, track: str, body: GenerateRequest | None = None):
    if suno_bridge.has_active_job():
        raise HTTPException(409, "Another generation job is running")
    validation = suno_bridge.validate_track(album, track, body.prompt if body else None)
    if not validation["ok"]:
        raise HTTPException(400, {"message": "Validation failed", "validation": validation})
    try:
        job = suno_bridge.start_generate(album, track, body.prompt if body else None)
        return {"job_id": job.id, "status": job.status}
    except RuntimeError as exc:
        raise HTTPException(409, str(exc)) from exc


@app.get("/api/jobs/{job_id}")
def api_job(job_id: str):
    job = suno_bridge.get_job(job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    return {
        "id": job.id,
        "kind": job.kind,
        "track": job.track,
        "status": job.status,
        "logs": job.logs[-50:],
        "result": job.result,
        "error": job.error,
        "started_at": job.started_at,
        "finished_at": job.finished_at,
    }


@app.post("/api/albums/{album}/tracks/{track}/status")
def api_status_poll(album: str, track: str, body: DownloadRequest):
    return suno_bridge.run_status(album, track, body.run_number)


@app.post("/api/albums/{album}/tracks/{track}/download")
def api_download(album: str, track: str, body: DownloadRequest):
    return suno_bridge.run_download(album, track, body.run_number, body.take)


@app.post("/api/albums/{album}/tracks/{track}/wav")
def api_wav(album: str, track: str, body: WavRequest):
    return suno_bridge.run_wav(album, track, body.run_number, body.take, body.final_name)


@app.post("/api/albums/{album}/tracks/{track}/verdict")
def api_verdict(album: str, track: str, body: VerdictRequest):
    return apply_verdict(album, track, body.verdict_type, body.run_number, body.take)


@app.post("/api/albums/{album}/tracks/{track}/notes")
def api_notes(album: str, track: str, body: NotesRequest):
    path = append_listening_notes(
        album,
        track,
        run_number=body.run_number,
        take=body.take,
        prompt_version=body.prompt_version,
        audio_file=body.audio_file,
        first_feeling=body.first_feeling,
        what_worked=body.what_worked,
        what_failed=body.what_failed,
        decision=body.decision,
        next_move=body.next_move,
        quick_tags=body.quick_tags,
    )
    return {"ok": True, "path": str(path)}


@app.post("/api/albums/{album}/tracks/{track}/select-final")
def api_select_final(album: str, track: str, body: SelectFinalRequest):
    return select_final(
        album,
        track,
        run_number=body.run_number,
        take=body.take,
        reason=body.reason,
        album_fit=body.album_fit,
        artist_fit=body.artist_fit,
    )


@app.post("/api/albums/{album}/tracks/{track}/archive")
def api_archive(album: str, track: str, body: ArchiveRequest):
    detail = scanner.get_album_detail(album)
    track_entry = next((t for t in detail["tracks"] if t["slug"] == track), None)
    track_number = body.track_number or (track_entry["number"] if track_entry else 0)
    return archive_track(
        album,
        track,
        final_audio=body.final_audio,
        track_number=track_number,
        album_title=detail.get("title", ""),
    )


@app.get("/api/search")
def api_search(q: str = "", album: str | None = None):
    if not q or len(q) < 2:
        return {"results": []}
    query = q.lower()
    results: list[dict] = []
    albums = [album] if album else [a.slug for a in scanner.list_albums()]
    for slug in albums:
        try:
            detail = scanner.get_album_detail(slug)
        except FileNotFoundError:
            continue
        for track in detail["tracks"]:
            if not track.get("exists"):
                continue
            try:
                td = scanner.get_track_detail(slug, track["slug"])
            except FileNotFoundError:
                continue
            for lf in td.get("lyrics_files", []):
                if query in lf["content"].lower():
                    results.append(
                        {
                            "album": slug,
                            "track": track["slug"],
                            "title": track["title"],
                            "match": "lyrics",
                            "snippet": _snippet(lf["content"], query),
                        }
                    )
            if td.get("prompt") and query in td["prompt"]["fields"].get("styles", "").lower():
                results.append(
                    {
                        "album": slug,
                        "track": track["slug"],
                        "title": track["title"],
                        "match": "styles",
                        "snippet": _snippet(td["prompt"]["fields"]["styles"], query),
                    }
                )
    return {"results": results[:20]}


def _snippet(text: str, query: str, radius: int = 60) -> str:
    idx = text.lower().find(query)
    if idx < 0:
        return text[:120]
    start = max(0, idx - radius)
    end = min(len(text), idx + len(query) + radius)
    return ("…" if start else "") + text[start:end].replace("\n", " ") + ("…" if end < len(text) else "")


# Static frontend
_static = WEB_DIST if WEB_DIST.is_dir() else WEB_DEV
if _static.is_dir():
    app.mount("/", StaticFiles(directory=str(_static), html=True), name="static")
