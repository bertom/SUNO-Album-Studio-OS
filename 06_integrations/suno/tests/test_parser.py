"""Tests for suno prompt parser."""

from __future__ import annotations

import unittest
from pathlib import Path

from studio_suno.config import REPO_ROOT
from studio_suno.parser import parse_prompt_file, to_api_payload, validate_prompt, validate_prompt_extended

TEMPLATE_PROMPT = (
    REPO_ROOT / "02_albums/_album_template/tracks/_track_template/suno/suno_prompt_v1.md"
)

LIMITS = {"prompt_max": 5000, "style_max": 1000, "title_max": 100}


class TestParserTemplateTrack(unittest.TestCase):
    def test_parses_title_and_settings(self) -> None:
        prompt = parse_prompt_file(TEMPLATE_PROMPT)
        self.assertEqual(prompt.title, "Hold It Gentle")
        self.assertEqual(prompt.vocal_gender, "M")
        self.assertAlmostEqual(prompt.weirdness_pct, 22.0)
        self.assertAlmostEqual(prompt.style_influence_pct, 68.0)

    def test_parses_lyrics_with_sections(self) -> None:
        prompt = parse_prompt_file(TEMPLATE_PROMPT)
        self.assertIn("[Verse 1]", prompt.lyrics)
        self.assertIn("Hold it gentle", prompt.lyrics)
        self.assertIn("fingerpicked nylon guitar", prompt.styles)

    def test_validates_clean(self) -> None:
        prompt = parse_prompt_file(TEMPLATE_PROMPT)
        errors = validate_prompt(prompt, LIMITS)
        self.assertEqual(errors, [])

    def test_api_payload_mapping(self) -> None:
        prompt = parse_prompt_file(TEMPLATE_PROMPT)
        payload = to_api_payload(prompt, model="V4_5ALL", callback_url="https://localhost/noop")
        self.assertTrue(payload["customMode"])
        self.assertFalse(payload["instrumental"])
        self.assertEqual(payload["title"], "Hold It Gentle")
        self.assertEqual(payload["vocalGender"], "m")
        self.assertEqual(payload["weirdnessConstraint"], 0.22)
        self.assertEqual(payload["styleWeight"], 0.68)
        self.assertIn("[Verse 1]", payload["prompt"])

    def test_rejects_studio_shorthand_in_styles(self) -> None:
        prompt = parse_prompt_file(TEMPLATE_PROMPT)
        prompt.styles = "warm acoustic, Family-like groove"
        errors = validate_prompt(prompt, LIMITS)
        self.assertTrue(any("SUNO cannot know" in e for e in errors))

    def test_rejects_negative_instruction_in_styles(self) -> None:
        prompt = parse_prompt_file(TEMPLATE_PROMPT)
        prompt.styles = "acoustic folk, no dub effects, warm bass"
        errors, _warnings = validate_prompt_extended(prompt, LIMITS)
        self.assertTrue(any("negative instruction" in e for e in errors))


class TestTrackPaths(unittest.TestCase):
    def test_resolves_album_track_slug(self) -> None:
        from studio_suno.paths import resolve_track_path

        path = resolve_track_path("_album_template/_track_template")
        self.assertTrue(path.name == "_track_template")
        self.assertTrue((path / "suno" / "suno_prompt_v1.md").exists())

    def test_resolves_track_slug_only(self) -> None:
        from studio_suno.paths import resolve_track_path

        path = resolve_track_path("_track_template")
        self.assertEqual(path.name, "_track_template")


class TestNextRunNumber(unittest.TestCase):
    def test_increments_from_empty(self) -> None:
        from studio_suno.runs import next_run_number

        track_dir = REPO_ROOT / "02_albums/_album_template/tracks/_track_template"
        n = next_run_number(track_dir)
        self.assertRegex(n, r"^\d{3}$")


if __name__ == "__main__":
    unittest.main()
