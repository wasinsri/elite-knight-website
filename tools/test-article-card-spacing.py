#!/usr/bin/env python3
"""Regression check for balanced article-card action spacing."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    css = (ROOT / "assets/site.css").read_text(encoding="utf-8")
    expected_rules = (
        ".ek-site [data-insights-grid] { align-items: start; }",
        ".ek-site [data-insights-grid] .article-card { height: auto; }",
        ".ek-site [data-insights-grid] .article-card > div { flex: none; }",
        ".ek-site [data-insights-grid] .article-card-actions { margin-top: 0; padding-top: 1.5rem; }",
    )
    for rule in expected_rules:
        assert rule in css, f"missing article-card spacing rule: {rule}"
    assert "@media (max-width: 767px) {\n  .ek-site [data-insights-grid]" not in css, (
        "balanced spacing must apply to the desktop three-column card grid"
    )


if __name__ == "__main__":
    main()
