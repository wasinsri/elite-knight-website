#!/usr/bin/env python3
"""Verify every article CTA ends with a localized contact button."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
CTA_PATTERN = re.compile(r'<section class="article-cta\b.*?</section>', re.DOTALL)
LINK_PATTERN = re.compile(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', re.DOTALL)


def main() -> None:
    failures: list[str] = []
    article_groups = (
        (ROOT / "articles", "../contact.html", "ติดต่อเรา"),
        (ROOT / "en" / "articles", "../contact.html", "Contact us"),
    )

    for directory, expected_href, expected_label in article_groups:
        for article in sorted(directory.glob("*.html")):
            match = CTA_PATTERN.search(article.read_text(encoding="utf-8"))
            if not match:
                failures.append(f"{article.relative_to(ROOT)}: missing article CTA")
                continue

            links = LINK_PATTERN.findall(match.group(0))
            contact_links = [(href, label) for href, label in links if href.endswith("contact.html")]
            if len(contact_links) != 1:
                failures.append(
                    f"{article.relative_to(ROOT)}: expected one contact button, found {len(contact_links)}"
                )
                continue

            href, label = contact_links[0]
            visible_label = re.sub(r"<[^>]+>", "", label).strip()
            if href != expected_href:
                failures.append(
                    f"{article.relative_to(ROOT)}: contact button links to {href}, expected {expected_href}"
                )
            if visible_label != expected_label:
                failures.append(
                    f"{article.relative_to(ROOT)}: contact label is {visible_label!r}, expected {expected_label!r}"
                )
            if not links or links[-1] != contact_links[0]:
                failures.append(f"{article.relative_to(ROOT)}: contact button must be the final CTA action")

    if failures:
        raise AssertionError("\n".join(failures))


if __name__ == "__main__":
    main()
