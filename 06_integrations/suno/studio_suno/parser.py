"""Parse Studio OS suno_prompt_vN.md files into structured fields and API payloads."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

FIELD_ORDER = [
    "lyrics",
    "styles",
    "exclude_styles",
    "vocal_gender",
    "weirdness_pct",
    "style_influence_pct",
    "title",
]

FENCED_BLOCK = re.compile(r"```(?:text)?\n(.*?)```", re.DOTALL)
SECTION_HEADER = re.compile(r"^###\s+(.+?)\s*$", re.MULTILINE)

# Common artist-name patterns to warn about (not exhaustive)
ARTIST_PATTERNS = [
    r"\bbob marley\b",
    r"\breggae legend\b",
    r"\bsounds like\b",
    r"\bin the style of\b",
    r"\bstyle of\b",
]

# Studio/repo shorthand — Styles field only (SUNO has no project context)
STYLE_CONTEXT_PATTERNS = [
    r"\binner light tales\b",
    r"\b\w+[- ]like\b",  # groove-family shorthand, e.g. Family-like, acoustic-like
    r"\bdirection [abc]\b",
    r"\bilt\b",
    r"\bstudio os\b",
]

# Reggae technique terms SUNO misreads as artist names
SUNO_SENSITIVE_STYLE_WORDS = [
    r"\bskank\b",
]

# Negative prompting in Styles — use Exclude styles instead
NEGATIVE_STYLE_PATTERNS = [
    r"\bno\s+dub\b",
    r"\bwithout\s+",
    r"\bno\s+",
]

# Unreliable lyric tags
BACKING_VOCAL_TAG = re.compile(r"\[backing\s+vocals?\]", re.IGNORECASE)


@dataclass
class SunoPrompt:
    source_path: Path
    lyrics: str = ""
    styles: str = ""
    exclude_styles: str = ""
    vocal_gender: str = "M"
    weirdness_pct: float = 15.0
    style_influence_pct: float = 65.0
    title: str = ""
    instrumental: bool = False
    warnings: list[str] = field(default_factory=list)

    @property
    def prompt_version(self) -> str:
        return self.source_path.name


def parse_prompt_file(path: Path) -> SunoPrompt:
    text = path.read_text(encoding="utf-8")
    prompt = SunoPrompt(source_path=path)

    sections = _split_sections(text)
    prompt.lyrics = sections.get("Lyrics", "").strip()
    prompt.styles = sections.get("Styles", "").strip()
    prompt.exclude_styles = sections.get("Exclude styles", "").strip()
    prompt.title = sections.get("Song Title", "").strip()

    gender = sections.get("Vocal Gender", "M").strip().upper()
    if gender in ("M", "F"):
        prompt.vocal_gender = gender
    else:
        prompt.warnings.append(f"Unexpected Vocal Gender '{gender}', defaulting to M")

    weirdness = sections.get("Weirdness %", "15%").strip()
    prompt.weirdness_pct = _parse_percent(weirdness, "Weirdness %")

    style_inf = sections.get("Style influence %", "65%").strip()
    prompt.style_influence_pct = _parse_percent(style_inf, "Style influence %")

    if not prompt.lyrics and not prompt.instrumental:
        prompt.warnings.append("Lyrics block is empty")
    if not prompt.styles:
        prompt.warnings.append("Styles block is empty")
    if not prompt.title:
        prompt.warnings.append("Song Title block is empty")

    return prompt


def _split_sections(text: str) -> dict[str, str]:
    headers = list(SECTION_HEADER.finditer(text))
    sections: dict[str, str] = {}

    for i, match in enumerate(headers):
        name = match.group(1).strip()
        start = match.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        body = text[start:end].strip()

        fenced = FENCED_BLOCK.search(body)
        if fenced:
            sections[name] = fenced.group(1).strip()
        else:
            sections[name] = body.strip()

    return sections


def _parse_percent(value: str, label: str) -> float:
    cleaned = value.replace("%", "").strip()
    try:
        return float(cleaned)
    except ValueError as exc:
        raise ValueError(f"Invalid {label}: {value!r}") from exc


def validate_prompt(prompt: SunoPrompt, limits: dict[str, int]) -> list[str]:
    errors: list[str] = []

    if not prompt.instrumental and not prompt.lyrics:
        errors.append("Lyrics required for non-instrumental tracks")
    if len(prompt.lyrics) > limits["prompt_max"]:
        errors.append(f"Lyrics too long: {len(prompt.lyrics)} > {limits['prompt_max']}")
    if len(prompt.styles) > limits["style_max"]:
        errors.append(f"Styles too long: {len(prompt.styles)} > {limits['style_max']}")
    if len(prompt.title) > limits["title_max"]:
        errors.append(f"Title too long: {len(prompt.title)} > {limits['title_max']}")
    if not (0 <= prompt.weirdness_pct <= 100):
        errors.append(f"Weirdness % out of range: {prompt.weirdness_pct}")
    if not (0 <= prompt.style_influence_pct <= 100):
        errors.append(f"Style influence % out of range: {prompt.style_influence_pct}")
    if prompt.vocal_gender not in ("M", "F"):
        errors.append(f"Invalid vocal gender: {prompt.vocal_gender}")

    combined = f"{prompt.lyrics} {prompt.styles}".lower()
    for pattern in ARTIST_PATTERNS:
        if re.search(pattern, combined, re.IGNORECASE):
            errors.append(f"Possible artist-name reference detected: /{pattern}/")

    styles_lower = prompt.styles.lower()
    for pattern in STYLE_CONTEXT_PATTERNS:
        if re.search(pattern, styles_lower, re.IGNORECASE):
            errors.append(
                f"Styles contain studio context SUNO cannot know: /{pattern}/ — "
                "translate to concrete musical terms (see SUNO guide)"
            )

    for pattern in SUNO_SENSITIVE_STYLE_WORDS:
        if re.search(pattern, styles_lower, re.IGNORECASE):
            errors.append(
                f"Styles contain term SUNO may reject as artist reference: /{pattern}/ — "
                'use "offbeat rhythm guitar chop" instead of "skank"'
            )

    return errors


def prompt_warnings(prompt: SunoPrompt) -> list[str]:
    """Soft checks — review before run; not CLI hard failures."""
    warnings: list[str] = []

    if not prompt.exclude_styles.strip():
        warnings.append(
            "Exclude styles is empty — EDM/trap bleed likely; "
            "see suno_learnings.md baseline exclude list"
        )

    if BACKING_VOCAL_TAG.search(prompt.lyrics):
        warnings.append(
            '[Backing vocals] tag unreliable — use parentheses call-response lines'
        )

    if len(prompt.lyrics) > 3500:
        warnings.append(
            f"Lyrics long ({len(prompt.lyrics)} chars) — may affect delivery"
        )

    return warnings


def validate_prompt_extended(prompt: SunoPrompt, limits: dict[str, int]) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) for validate command."""
    errors = validate_prompt(prompt, limits)

    styles_lower = prompt.styles.lower()
    for pattern in NEGATIVE_STYLE_PATTERNS:
        if re.search(pattern, styles_lower, re.IGNORECASE):
            errors.append(
                f"Styles contain negative instruction /{pattern}/ — "
                "use positive Styles + Exclude styles (see SUNO guide)"
            )
            break

    warnings = prompt_warnings(prompt)
    return errors, warnings


def to_api_payload(
    prompt: SunoPrompt,
    *,
    model: str,
    callback_url: str,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "customMode": True,
        "instrumental": prompt.instrumental,
        "model": model,
        "title": prompt.title,
        "style": prompt.styles,
        "negativeTags": prompt.exclude_styles,
        "vocalGender": prompt.vocal_gender.lower(),
        "weirdnessConstraint": round(prompt.weirdness_pct / 100, 2),
        "styleWeight": round(prompt.style_influence_pct / 100, 2),
        "callBackUrl": callback_url,
    }
    if not prompt.instrumental:
        payload["prompt"] = prompt.lyrics
    return payload
