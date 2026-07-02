"""Command-line interface for studio_suno."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

import yaml

from .client import SunoApiError, SunoClient, extract_suno_tracks
from .config import get_api_key, load_config
from .download import download_file
from .parser import parse_prompt_file, to_api_payload, validate_prompt, validate_prompt_extended
from .paths import album_config_path, audio_dir, find_prompt_file, resolve_track_path
from .runs import (
    append_run_log,
    load_run_sidecar,
    next_run_number,
    update_sidecar_wav,
    write_run_sidecar,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="studio-suno",
        description="SUNO Album Studio SUNO API CLI (sunoapi.org)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    gen = sub.add_parser("generate", help="Submit prompt and optionally wait for MP3s")
    gen.add_argument("track", help="Track slug or path under 02_albums")
    gen.add_argument("--prompt", help="Prompt version e.g. v1 or suno_prompt_v1.md")
    gen.add_argument("--model", help="Override default model (default V5_5; also V5, V4_5ALL, …)")
    gen.add_argument("--instrumental", action="store_true", help="Instrumental generation")
    gen.add_argument("--wait", action="store_true", default=True, help="Poll until complete (default)")
    gen.add_argument("--no-wait", action="store_false", dest="wait", help="Submit only, return task ID")
    gen.add_argument("--stream-only", action="store_true", help="Stop after first stream URL is available")
    gen.add_argument("--dry-run", action="store_true", help="Print payload without calling API")

    status = sub.add_parser("status", help="Check generation or WAV task status")
    status.add_argument("task_id", nargs="?", help="Task ID to query")
    status.add_argument("--track", help="Track path — use with --run for latest run task")
    status.add_argument("--run", help="Run number e.g. 003")
    status.add_argument("--wav", action="store_true", help="Query WAV conversion task")

    dl = sub.add_parser("download", help="Re-download MP3s for an existing run")
    dl.add_argument("track", help="Track slug or path")
    dl.add_argument("--run", required=True, help="Run number e.g. 003")
    dl.add_argument("--take", choices=["a", "b", "both"], default="both")

    wav = sub.add_parser("wav", help="Convert and download WAV for a run take")
    wav.add_argument("track", help="Track slug or path")
    wav.add_argument("--run", required=True, help="Run number e.g. 003")
    wav.add_argument("--take", choices=["a", "b"], default="a")
    wav.add_argument("--final-name", help="Save as audio/<name>.wav instead of runNNN_take_X.wav")

    sub.add_parser("credits", help="Show remaining API credits")

    val = sub.add_parser("validate", help="Pre-flight prompt hygiene without calling API")
    val.add_argument("track", help="Track slug or path under 02_albums")
    val.add_argument("--prompt", help="Prompt version e.g. v1 or suno_prompt_v1.md")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = load_config()

    if args.command == "credits":
        return cmd_credits(config)
    if args.command == "validate":
        return cmd_validate(args, config)
    if args.command == "generate":
        return cmd_generate(args, config)
    if args.command == "status":
        return cmd_status(args, config)
    if args.command == "download":
        return cmd_download(args, config)
    if args.command == "wav":
        return cmd_wav(args, config)
    return 1


def cmd_credits(config: dict[str, Any]) -> int:
    client = _client(config)
    credits = client.get_credits()
    print(f"Remaining credits: {credits}")
    threshold = config.get("credit_warning_threshold", 10)
    if credits < threshold:
        print(f"Warning: credits below threshold ({threshold})")
    return 0


def cmd_validate(args: argparse.Namespace, config: dict[str, Any]) -> int:
    track_dir = resolve_track_path(args.track)
    prompt_path = find_prompt_file(track_dir, args.prompt)
    prompt = parse_prompt_file(prompt_path)
    limits = config["limits"]

    print(f"Validating {prompt_path}")
    print(f"  Title: {prompt.title!r}")
    print(f"  Weirdness: {prompt.weirdness_pct}%  Style influence: {prompt.style_influence_pct}%")
    print()

    for warning in prompt.warnings:
        print(f"Parse warning: {warning}")

    errors, warnings = validate_prompt_extended(prompt, limits)

    for warning in warnings:
        print(f"Warning: {warning}")

    if errors:
        print()
        for err in errors:
            print(f"Error: {err}")
        return 1

    print()
    print("OK — no blocking errors.")
    if warnings:
        print(f"({len(warnings)} warning(s) — review before run)")
    return 0


def cmd_generate(args: argparse.Namespace, config: dict[str, Any]) -> int:
    track_dir = resolve_track_path(args.track)
    prompt_path = find_prompt_file(track_dir, args.prompt)
    prompt = parse_prompt_file(prompt_path)
    prompt.instrumental = args.instrumental

    model = _resolve_model(track_dir, config, args.model)
    limits = config["limits"]

    for warning in prompt.warnings:
        print(f"Warning: {warning}", file=sys.stderr)

    errors = validate_prompt(prompt, limits)
    if errors:
        for err in errors:
            print(f"Validation error: {err}", file=sys.stderr)
        return 1

    payload = to_api_payload(
        prompt,
        model=model,
        callback_url=config["callback_url"],
    )

    if args.dry_run:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    client = _client(config)
    _check_credits(client, config)

    run_number = next_run_number(track_dir)
    print(f"Run {run_number} — submitting {prompt_path.name}...")

    try:
        task_id = client.generate_music(payload)
    except SunoApiError as exc:
        _log_failed_run(track_dir, run_number, prompt, model, str(exc), task_id="")
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Task ID: {task_id}")

    sidecar: dict[str, Any] = {
        "run": run_number,
        "date": date.today().isoformat(),
        "prompt_version": prompt.prompt_version,
        "task_id": task_id,
        "model": model,
        "takes": [],
        "status": "submitted",
    }
    write_run_sidecar(track_dir, run_number, sidecar)

    if not args.wait:
        append_run_log(
            track_dir,
            run_number=run_number,
            prompt_version=prompt.prompt_version,
            task_id=task_id,
            model=model,
            vocal_gender=prompt.vocal_gender,
            weirdness_pct=prompt.weirdness_pct,
            style_influence_pct=prompt.style_influence_pct,
            takes=[],
            status="submitted — use `studio-suno status` or re-run with --wait",
        )
        print(f"Submitted. Check status: studio-suno status {task_id}")
        return 0

    def on_first_success(details: dict[str, Any]) -> None:
        tracks = extract_suno_tracks(details)
        print("\n--- Stream preview available (~30-40s) ---")
        for i, track in enumerate(tracks):
            label = chr(ord("a") + i)
            if track.get("stream_url"):
                print(f"Take {label}: {track['stream_url']}")
        print("---\n")

    try:
        if args.stream_only:
            details = client.poll_generation(
                task_id,
                interval=config["poll_interval_seconds"],
                timeout=config["poll_timeout_seconds"],
                on_first_success=on_first_success,
            )
            # For stream-only, we may exit at FIRST_SUCCESS — poll until at least that
            details = client.get_generation_details(task_id)
            while details.get("status") not in ("FIRST_SUCCESS", "SUCCESS"):
                import time

                time.sleep(config["poll_interval_seconds"])
                details = client.get_generation_details(task_id)
            tracks = extract_suno_tracks(details)
            _print_stream_urls(tracks)
            return 0

        details = client.poll_generation(
            task_id,
            interval=config["poll_interval_seconds"],
            timeout=config["poll_timeout_seconds"],
            on_first_success=on_first_success,
        )
    except SunoApiError as exc:
        _log_failed_run(track_dir, run_number, prompt, model, str(exc), task_id=task_id)
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    tracks = extract_suno_tracks(details)
    takes = _download_takes(track_dir, run_number, tracks)

    sidecar["status"] = "complete"
    sidecar["takes"] = takes
    write_run_sidecar(track_dir, run_number, sidecar)

    append_run_log(
        track_dir,
        run_number=run_number,
        prompt_version=prompt.prompt_version,
        task_id=task_id,
        model=model,
        vocal_gender=prompt.vocal_gender,
        weirdness_pct=prompt.weirdness_pct,
        style_influence_pct=prompt.style_influence_pct,
        takes=takes,
    )

    print(f"\nDone. MP3s in {audio_dir(track_dir)}")
    print(f"Log updated: {track_dir / 'suno' / 'suno_runs.md'}")
    print(f"Next: add listening notes — analysis/listening_notes.md (Run {run_number})")
    return 0


def cmd_status(args: argparse.Namespace, config: dict[str, Any]) -> int:
    client = _client(config)
    task_id = args.task_id

    if not task_id and args.track and args.run:
        track_dir = resolve_track_path(args.track)
        sidecar = load_run_sidecar(track_dir, args.run.zfill(3))
        if args.wav:
            task_id = sidecar.get("wav_task_id", "")
            if not task_id:
                print("No wav_task_id on this run — run `studio-suno wav` first", file=sys.stderr)
                return 1
        else:
            task_id = sidecar["task_id"]
    elif not task_id:
        print("Provide task_id or --track with --run", file=sys.stderr)
        return 1

    if args.wav:
        details = client.get_wav_details(task_id)
        flag = details.get("successFlag")
        print(f"WAV task: {task_id}")
        print(f"Status: {flag}")
        wav_url = (details.get("response") or {}).get("audioWavUrl")
        if wav_url:
            print(f"WAV URL: {wav_url}")
        if details.get("errorMessage"):
            print(f"Error: {details['errorMessage']}")
        return 0

    details = client.get_generation_details(task_id)
    status = details.get("status")
    print(f"Task: {task_id}")
    print(f"Status: {status}")

    tracks = extract_suno_tracks(details)
    for i, track in enumerate(tracks):
        label = chr(ord("a") + i)
        print(f"\nTake {label}:")
        print(f"  audio_id: {track.get('id')}")
        if track.get("stream_url"):
            print(f"  stream: {track['stream_url']}")
        if track.get("audio_url"):
            print(f"  mp3: {track['audio_url']}")

    if details.get("errorMessage"):
        print(f"Error: {details['errorMessage']}")
    return 0


def cmd_download(args: argparse.Namespace, config: dict[str, Any]) -> int:
    track_dir = resolve_track_path(args.track)
    run_number = args.run.zfill(3)
    sidecar = load_run_sidecar(track_dir, run_number)
    client = _client(config)

    details = client.get_generation_details(sidecar["task_id"])
    if details.get("status") != "SUCCESS":
        print(f"Generation not complete: {details.get('status')}", file=sys.stderr)
        return 1

    tracks = extract_suno_tracks(details)
    takes = _download_takes(track_dir, run_number, tracks, take_filter=args.take)

    for i, take in enumerate(sidecar.get("takes", [])):
        if i < len(takes):
            take.update({k: v for k, v in takes[i].items() if v})

    sidecar["takes"] = takes if takes else sidecar.get("takes", [])
    write_run_sidecar(track_dir, run_number, sidecar)
    print("Download complete.")
    return 0


def cmd_wav(args: argparse.Namespace, config: dict[str, Any]) -> int:
    track_dir = resolve_track_path(args.track)
    run_number = args.run.zfill(3)
    sidecar = load_run_sidecar(track_dir, run_number)

    take_data = _find_take(sidecar, args.take)
    gen_task_id = sidecar["task_id"]
    audio_id = take_data.get("audio_id")
    if not audio_id:
        print(f"No audio_id for take {args.take}", file=sys.stderr)
        return 1

    client = _client(config)
    _check_credits(client, config)

    print(f"Starting WAV conversion for run {run_number} take {args.take}...")
    try:
        wav_task_id = client.start_wav_conversion(gen_task_id, audio_id)
    except SunoApiError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    sidecar["wav_task_id"] = wav_task_id
    write_run_sidecar(track_dir, run_number, sidecar)
    print(f"WAV task ID: {wav_task_id}")

    try:
        wav_details = client.poll_wav(
            wav_task_id,
            interval=config["poll_interval_seconds"],
            timeout=config["poll_timeout_seconds"],
        )
    except SunoApiError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    wav_url = (wav_details.get("response") or {}).get("audioWavUrl")
    if not wav_url:
        print("No WAV URL in response", file=sys.stderr)
        return 1

    out_dir = audio_dir(track_dir)
    if args.final_name:
        dest = out_dir / f"{args.final_name}.wav"
    else:
        dest = out_dir / f"run{run_number}_take_{args.take}.wav"

    download_file(wav_url, dest)
    rel = dest.relative_to(track_dir)
    update_sidecar_wav(track_dir, run_number, args.take, rel)

    print(f"WAV saved: {dest}")
    return 0


def _client(config: dict[str, Any]) -> SunoClient:
    return SunoClient(
        api_key=get_api_key(),
        base_url=config["api_base_url"],
        callback_url=config["callback_url"],
    )


def _resolve_model(track_dir: Path, config: dict[str, Any], override: str | None) -> str:
    if override:
        return override
    album_cfg = album_config_path(track_dir)
    if album_cfg:
        with album_cfg.open(encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
        if data.get("default_model"):
            return data["default_model"]
    return config["default_model"]


def _check_credits(client: SunoClient, config: dict[str, Any]) -> None:
    threshold = config.get("credit_warning_threshold", 10)
    try:
        credits = client.get_credits()
        if credits < threshold:
            print(f"Warning: only {credits} credits remaining (threshold {threshold})", file=sys.stderr)
    except SunoApiError:
        pass


def _download_takes(
    track_dir: Path,
    run_number: str,
    tracks: list[dict[str, Any]],
    *,
    take_filter: str = "both",
) -> list[dict[str, Any]]:
    out_dir = audio_dir(track_dir)
    takes: list[dict[str, Any]] = []

    for i, track in enumerate(tracks[:2]):
        label = chr(ord("a") + i)
        if take_filter != "both" and label != take_filter:
            continue

        entry: dict[str, Any] = {
            "take": label,
            "audio_id": track.get("id"),
            "stream_url": track.get("stream_url"),
            "audio_url": track.get("audio_url"),
            "duration": track.get("duration"),
        }

        url = track.get("audio_url")
        if url:
            dest = out_dir / f"run{run_number}_take_{label}.mp3"
            print(f"Downloading take {label} → {dest.name}...")
            download_file(url, dest)
            entry["mp3"] = str(dest.relative_to(track_dir))

        takes.append(entry)

    return takes


def _find_take(sidecar: dict[str, Any], take: str) -> dict[str, Any]:
    for item in sidecar.get("takes", []):
        if item.get("take") == take:
            return item
    raise SystemExit(f"Take {take} not found in run sidecar")


def _print_stream_urls(tracks: list[dict[str, Any]]) -> None:
    for i, track in enumerate(tracks):
        label = chr(ord("a") + i)
        if track.get("stream_url"):
            print(f"Take {label} stream: {track['stream_url']}")


def _log_failed_run(
    track_dir: Path,
    run_number: str,
    prompt: Any,
    model: str,
    error: str,
    task_id: str,
) -> None:
    append_run_log(
        track_dir,
        run_number=run_number,
        prompt_version=prompt.prompt_version,
        task_id=task_id or "n/a",
        model=model,
        vocal_gender=prompt.vocal_gender,
        weirdness_pct=prompt.weirdness_pct,
        style_influence_pct=prompt.style_influence_pct,
        takes=[],
        status="failed",
        error=error,
    )
