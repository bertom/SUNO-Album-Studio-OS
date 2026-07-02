"""HTTP client for sunoapi.org."""

from __future__ import annotations

import time
from typing import Any, Callable

import requests

GENERATION_PENDING = {"PENDING", "TEXT_SUCCESS", "FIRST_SUCCESS", "GENERATING"}
GENERATION_FAILED = {
    "CREATE_TASK_FAILED",
    "GENERATE_AUDIO_FAILED",
    "CALLBACK_EXCEPTION",
    "SENSITIVE_WORD_ERROR",
}

WAV_PENDING = {"PENDING"}
WAV_FAILED = {"CREATE_TASK_FAILED", "GENERATE_WAV_FAILED", "CALLBACK_EXCEPTION"}


class SunoApiError(Exception):
    def __init__(self, message: str, code: int | None = None, status: str | None = None):
        super().__init__(message)
        self.code = code
        self.status = status


class SunoClient:
    def __init__(self, api_key: str, base_url: str, callback_url: str):
        self.base_url = base_url.rstrip("/")
        self.callback_url = callback_url
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
        )

    def _request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        response = self.session.request(method, url, timeout=120, **kwargs)
        try:
            data = response.json()
        except ValueError as exc:
            raise SunoApiError(f"Non-JSON response ({response.status_code}): {response.text[:200]}") from exc

        code = data.get("code")
        if code != 200:
            raise SunoApiError(
                _friendly_error(code, data.get("msg", "Unknown error")),
                code=code,
            )
        return data

    def get_credits(self) -> int:
        data = self._request("GET", "/api/v1/generate/credit")
        return int(data["data"])

    def generate_music(self, payload: dict[str, Any]) -> str:
        data = self._request("POST", "/api/v1/generate", json=payload)
        return data["data"]["taskId"]

    def get_generation_details(self, task_id: str) -> dict[str, Any]:
        data = self._request("GET", "/api/v1/generate/record-info", params={"taskId": task_id})
        return data["data"]

    def poll_generation(
        self,
        task_id: str,
        *,
        interval: float,
        timeout: float,
        on_first_success: Callable[[dict[str, Any]], None] | None = None,
    ) -> dict[str, Any]:
        deadline = time.time() + timeout
        first_reported = False

        while time.time() < deadline:
            details = self.get_generation_details(task_id)
            status = details.get("status", "")

            if status == "FIRST_SUCCESS" and on_first_success and not first_reported:
                first_reported = True
                on_first_success(details)

            if status == "SUCCESS":
                return details

            if status in GENERATION_FAILED:
                msg = details.get("errorMessage") or status
                raise SunoApiError(f"Generation failed: {msg}", status=status)

            if status not in GENERATION_PENDING and status not in GENERATION_FAILED:
                if status:
                    raise SunoApiError(f"Unexpected status: {status}", status=status)

            time.sleep(interval)

        raise SunoApiError(f"Timed out waiting for task {task_id} after {timeout}s")

    def start_wav_conversion(self, generation_task_id: str, audio_id: str) -> str:
        payload = {
            "taskId": generation_task_id,
            "audioId": audio_id,
            "callBackUrl": self.callback_url,
        }
        data = self._request("POST", "/api/v1/wav/generate", json=payload)
        return data["data"]["taskId"]

    def get_wav_details(self, wav_task_id: str) -> dict[str, Any]:
        data = self._request("GET", "/api/v1/wav/record-info", params={"taskId": wav_task_id})
        return data["data"]

    def poll_wav(
        self,
        wav_task_id: str,
        *,
        interval: float,
        timeout: float,
    ) -> dict[str, Any]:
        deadline = time.time() + timeout

        while time.time() < deadline:
            details = self.get_wav_details(wav_task_id)
            flag = details.get("successFlag", "")

            if flag == "SUCCESS":
                return details

            if flag in WAV_FAILED:
                msg = details.get("errorMessage") or flag
                raise SunoApiError(f"WAV conversion failed: {msg}", status=flag)

            time.sleep(interval)

        raise SunoApiError(f"Timed out waiting for WAV task {wav_task_id} after {timeout}s")


def _friendly_error(code: int | None, msg: str) -> str:
    hints = {
        401: "Invalid API key — check SUNO_API_KEY in .env",
        413: "Prompt or style too long for this model",
        429: "Insufficient credits — top up at sunoapi.org",
        430: "Rate limited — wait and retry",
        455: "API maintenance — try again later",
    }
    hint = hints.get(code or 0, "")
    return f"API error {code}: {msg}" + (f" ({hint})" if hint else "")


def extract_suno_tracks(details: dict[str, Any]) -> list[dict[str, Any]]:
    response = details.get("response") or {}
    tracks = response.get("sunoData") or response.get("data") or []
    normalized: list[dict[str, Any]] = []
    for track in tracks:
        normalized.append(
            {
                "id": track.get("id") or track.get("audioId"),
                "audio_url": track.get("audioUrl") or track.get("audio_url"),
                "stream_url": track.get("streamAudioUrl") or track.get("stream_audio_url"),
                "title": track.get("title"),
                "duration": track.get("duration"),
            }
        )
    return normalized
