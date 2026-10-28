#!/usr/bin/env python3
"""Regression check for the featured Insight image filling its desktop grid cell."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    css = (ROOT / "assets/site.css").read_text(encoding="utf-8")
    expected = (
        ':where(.ek-site) [aria-labelledby="featured-insight"] '
        '> div > .article-card > img { align-self: stretch; aspect-ratio: auto; '
        'height: 100%; object-fit: cover; }'
    )
    assert expected in css, "featured Insight image must fill the desktop grid cell"


if __name__ == "__main__":
    main()
