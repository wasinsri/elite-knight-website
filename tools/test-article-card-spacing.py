#!/usr/bin/env python3
"""Regression check for equal-height article cards within each grid row."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    css = (ROOT / "assets/site.css").read_text(encoding="utf-8")
    expected_rules = (
        ".ek-site [data-insights-grid] { align-items: stretch; }",
        ".ek-site [data-insights-grid] .article-card { height: 100%; }",
        ".ek-site [data-insights-grid] .article-card > div { flex: 1; }",
        ".ek-site [data-insights-grid] .article-card-actions { margin-top: auto; padding-top: 1.5rem; }",
    )
    for rule in expected_rules:
        assert rule in css, f"missing article-card spacing rule: {rule}"
    assert ".ek-site [data-insights-grid] { align-items: start; }" not in css, (
        "article cards must stretch to the tallest card in each row"
    )


if __name__ == "__main__":
    main()
