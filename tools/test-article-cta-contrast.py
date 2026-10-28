#!/usr/bin/env python3
"""Regression check for legible article CTA text and buttons."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    css = (ROOT / "assets/site.css").read_text(encoding="utf-8")
    expected_rules = (
        ".ek-site .article-cta > a:first-of-type { background: #2dd4bf; border: 1px solid #5eead4; color: #073b37; }",
        ".ek-site .article-cta > a:first-of-type:hover { background: #5eead4; color: #062f2c; }",
        ".ek-site .article-cta > a:last-of-type { background: #fff; border: 1px solid #fff; color: #0d4f48; }",
        ".ek-site .article-cta > a:last-of-type:hover { background: #ccfbf1; border-color: #ccfbf1; color: #064e3b; }",
    )
    for rule in expected_rules:
        assert rule in css, f"missing article CTA contrast rule: {rule}"


if __name__ == "__main__":
    main()
