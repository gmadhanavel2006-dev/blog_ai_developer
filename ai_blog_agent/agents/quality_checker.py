"""
Quality guard for the NightWriter AI system.

Before any draft is saved, it is run through two checks:
1. Word count — must meet the minimum for that category.
2. Duplicate check — the topic must not match any existing published/draft title.

If either check fails, the workflow logs a warning and falls back gracefully.
"""

import os
import re


MIN_WORD_COUNT = 300  # Absolute floor — anything below this is always rejected.


def count_words(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def _existing_titles(base_dir: str) -> set:
    """Collect all existing titles from drafts and published folders."""
    titles = set()
    for folder in ("drafts", "published"):
        folder_path = os.path.join(base_dir, "blog", folder)
        if not os.path.isdir(folder_path):
            continue
        for filename in os.listdir(folder_path):
            if filename.endswith(".md"):
                # Strip date suffix and extension
                stem = filename.replace(".md", "")
                # Remove trailing _YYYYMMDD
                stem = re.sub(r"_\d{8}$", "", stem)
                titles.add(stem.lower())
    return titles


def _title_to_slug(title: str) -> str:
    slug = "".join(c if c.isalnum() or c == " " else "" for c in title)
    slug = slug.replace(" ", "_")
    return slug[:50].lower()


class QualityChecker:
    def __init__(self, base_dir: str = "."):
        self.base_dir = base_dir

    def check_word_count(self, content: str, category: dict) -> bool:
        """Return True if content meets the minimum word count for this category."""
        words = count_words(content)
        # Parse the lower bound from e.g. "700-900"
        word_range = category.get("word_count", "300-500")
        try:
            minimum = int(word_range.split("-")[0])
        except (ValueError, IndexError):
            minimum = MIN_WORD_COUNT

        effective_min = max(minimum // 2, MIN_WORD_COUNT)  # Allow 50% tolerance

        if words < effective_min:
            print(
                f"[Quality Guard] WARN: Content too short ({words} words; minimum {effective_min}). "
                "Draft rejected."
            )
            return False
        print(f"[Quality Guard] OK: Word count {words} words.")
        return True

    def check_duplicate(self, title: str) -> bool:
        """Return True (= is duplicate) if a very similar title already exists."""
        slug = _title_to_slug(title)
        existing = _existing_titles(self.base_dir)

        # Check for exact slug match
        if slug in existing:
            print(f"[Quality Guard] DUPLICATE: '{slug}' already exists. Skipping save.")
            return True

        # Check for high-similarity (80%+ word overlap)
        slug_words = set(slug.split("_"))
        for existing_slug in existing:
            existing_words = set(existing_slug.split("_"))
            if len(slug_words) == 0:
                continue
            overlap = len(slug_words & existing_words) / len(slug_words)
            if overlap >= 0.8:
                print(
                    f"[Quality Guard] NEAR-DUPLICATE: {int(overlap*100)}% overlap "
                    f"with '{existing_slug}'. Skipping save."
                )
                return True

        print("[Quality Guard] OK: No duplicate found. Proceeding.")
        return False

    def validate(self, title: str, content: str, category: dict) -> dict:
        """
        Run all quality checks. Returns a dict:
          {"ok": bool, "word_count_ok": bool, "duplicate": bool}
        """
        duplicate     = self.check_duplicate(title)
        word_count_ok = self.check_word_count(content, category)

        ok = (not duplicate) and word_count_ok
        return {
            "ok":            ok,
            "word_count_ok": word_count_ok,
            "duplicate":     duplicate,
        }
