#!/usr/bin/env python3
"""Pre-publish consistency checks for the Elite Knight static site.

Turns the manual checklist in AGENTS.md into something a machine runs.
Usage:  python3 tools/check-consistency.py
Exit code 0 = clean, 1 = at least one error. Warnings never fail the build.
"""

from __future__ import annotations

import html
import json
import os
import re
import sys
from argparse import ArgumentParser
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", "node_modules", "tools", ".github"}

errors: list[str] = []
warnings: list[str] = []


parser = ArgumentParser(description="Check the Elite Knight static site.")
parser.add_argument(
    "--article",
    nargs=2,
    metavar=("THAI_ARTICLE", "ENGLISH_ARTICLE"),
    help="Validate one new Thai/English article pair for editorial length and FAQ parity.",
)
ARGS = parser.parse_args()


def err(page: str, msg: str) -> None:
    errors.append(f"{page}: {msg}")


def warn(page: str, msg: str) -> None:
    warnings.append(f"{page}: {msg}")


def html_files() -> list[str]:
    out = []
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f.endswith(".html"):
                out.append(os.path.relpath(os.path.join(base, f), ROOT))
    return sorted(out)


PAGES = html_files()
SOURCES = {p: open(os.path.join(ROOT, p), encoding="utf-8").read() for p in PAGES}
CSS_PATH = os.path.join(ROOT, "assets", "site.css")
CSS = open(CSS_PATH, encoding="utf-8").read()


# 1. one cache-busting version across the whole site -------------------------
def check_cache_version() -> None:
    versions = defaultdict(list)
    for page, src in SOURCES.items():
        for asset, version in re.findall(r"(site\.css|site\.js)\?v=([^\"']+)", src):
            versions[version].append(f"{page} ({asset})")
    if len(versions) > 1:
        summary = "; ".join(f"{v} in {len(f)} refs" for v, f in versions.items())
        err("site", f"more than one asset cache version in use: {summary}")


# 2. shared page shell -------------------------------------------------------
def check_shell() -> None:
    for page, src in SOURCES.items():
        if src.count("data-cookie-banner") != 1:
            err(page, f"expected exactly 1 cookie banner, found {src.count('data-cookie-banner')}")
        if src.count("data-mobile-menu-button") != 1:
            err(page, f"expected exactly 1 mobile menu button, found {src.count('data-mobile-menu-button')}")
        icons = len(re.findall(r'<link rel="(?:icon|apple-touch-icon)"', src))
        if icons != 3:
            err(page, f"expected 3 favicon declarations, found {icons}")
        if "skip-link" not in src:
            err(page, "missing skip link to #main-content")
        if "hreflang" not in src:
            err(page, "missing hreflang alternates")
        if not re.search(r'<link rel="canonical"', src):
            err(page, "missing canonical link")


# 3. analytics must stay behind cookie consent -------------------------------
def check_consent_gate() -> None:
    for page, src in SOURCES.items():
        if "googletagmanager" not in src:
            continue
        if "let analyticsLoaded" not in src or "ekCookieConsent" not in src:
            err(page, "analytics is not behind the cookie-consent gate")
        if re.search(r"<script[^>]+src=\"https://www\.googletagmanager\.com", src):
            err(page, "loads gtag.js directly instead of after consent")


# 4. no runtime Tailwind compiler --------------------------------------------
def check_no_cdn() -> None:
    for page, src in SOURCES.items():
        if "cdn.tailwindcss.com" in src:
            err(page, "loads the Tailwind CDN compiler (utilities belong in assets/site.css)")


# 5. every utility class used is actually defined -----------------------------
COMPONENT_PREFIXES = (
    "ek-", "article-", "accordion-", "brand-", "footer-", "nav-", "share-",
    "cookie-", "lang-", "map-", "mint-", "page-", "section-", "skip-", "social-",
    "soft-", "data-mesh", "glass-", "table-wrap", "active", "sr-only",
)


def check_classes() -> None:
    defined = set()
    for m in re.finditer(r"\.((?:\\.|[A-Za-z0-9_-])+)", CSS):
        defined.add(m.group(1).replace("\\", ""))
    used: Counter[str] = Counter()
    for src in SOURCES.values():
        for attr in re.findall(r'class="([^"]*)"', src):
            for token in attr.split():
                used[token] += 1
    missing = sorted(c for c in used if c not in defined and not c.startswith(COMPONENT_PREFIXES))
    for c in missing:
        err("assets/site.css", f'class "{c}" is used {used[c]}x in HTML but has no rule')


# 6. structured data ----------------------------------------------------------
def check_jsonld() -> None:
    for page, src in SOURCES.items():
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', src, re.S):
            try:
                json.loads(block)
            except Exception as exc:  # noqa: BLE001
                err(page, f"invalid JSON-LD: {exc}")


# 7. relative links and asset paths resolve -----------------------------------
def check_paths() -> None:
    for page, src in SOURCES.items():
        base = os.path.dirname(os.path.join(ROOT, page))
        for attr in re.findall(r'(?:href|src)="([^"#][^"]*)"', src):
            if attr.startswith(("http://", "https://", "mailto:", "tel:", "data:", "//", "#")):
                continue
            target = attr.split("?")[0].split("#")[0]
            if not target:
                continue
            resolved = os.path.normpath(os.path.join(base, target))
            if not os.path.exists(resolved):
                err(page, f"broken relative path: {attr}")


# 8. images ------------------------------------------------------------------
def check_images() -> None:
    for page, src in SOURCES.items():
        for tag in re.findall(r"<img[^>]*>", src):
            if "alt=" not in tag:
                err(page, f"image without alt text: {tag[:70]}")
            if "loading=" not in tag and "fetchpriority" not in tag and "brand-mark" not in tag:
                warn(page, f"image is neither lazy nor marked high priority: {tag[:70]}")


# 9. metadata length ----------------------------------------------------------
def check_metadata() -> None:
    for page, src in SOURCES.items():
        m = re.search(r"<title>(.*?)</title>", src, re.S)
        if not m:
            err(page, "missing <title>")
        else:
            title = html.unescape(m.group(1)).strip()
            if len(title) > 60:
                warn(page, f"title is {len(title)} chars (Google truncates past ~60): {title}")
        d = re.search(r'<meta name="description" content="(.*?)">', src, re.S)
        if not d:
            err(page, "missing meta description")
        elif page not in ("404.html", "en/404.html"):
            desc = html.unescape(d.group(1)).strip()
            if len(desc) < 110:
                warn(page, f"meta description is only {len(desc)} chars (aim for 140-160)")


# 10. bilingual pairing -------------------------------------------------------
def check_language_pairs() -> None:
    for page, src in SOURCES.items():
        th_only = len(re.findall(r'data-th="[^"]*"', src)) - len(re.findall(r'data-en="[^"]*"', src))
        if th_only:
            err(page, f"data-th / data-en are unbalanced by {th_only}")


# 11. new article editorial length and FAQ parity ---------------------------
def article_source(page: str) -> str | None:
    if page not in SOURCES:
        err("article validation", f"article file does not exist: {page}")
        return None
    return SOURCES[page]


def strip_tags(value: str) -> str:
    return re.sub(r"\s+", "", html.unescape(re.sub(r"<[^>]+>", " ", value)))


def attribute_value(attrs: str, name: str) -> str | None:
    match = re.search(rf'\b{name}="([^"]*)"', attrs, re.S)
    return html.unescape(match.group(1)) if match else None


def visible_tag_values(source: str, tag: str, language: str) -> list[str]:
    values: list[str] = []
    for match in re.finditer(rf"<{tag}\b([^>]*)>(.*?)</{tag}>", source, re.S | re.I):
        attrs, inner = match.groups()
        value = attribute_value(attrs, f"data-{language}")
        values.append(value if value is not None else html.unescape(re.sub(r"<[^>]+>", " ", inner)))
    return values


def editorial_characters(source: str, language: str) -> int:
    """Count rendered editorial copy, excluding navigation, actions, and footer UI."""
    article = re.search(r"<article\b[^>]*>(.*?)</article>", source, re.S | re.I)
    if not article:
        return 0
    editorial = article.group(1)
    editorial = re.sub(r'<section\b[^>]*class="[^"]*article-cta[^"]*"[^>]*>.*?</section>', "", editorial, flags=re.S | re.I)
    editorial = re.sub(r'<nav\b[^>]*class="[^"]*ek-related[^"]*"[^>]*>.*?</nav>', "", editorial, flags=re.S | re.I)
    editorial = re.sub(r'<(?:nav|script|style)\b[^>]*>.*?</(?:nav|script|style)>', "", editorial, flags=re.S | re.I)
    text = []
    for tag in ("h1", "h2", "h3", "h4", "h5", "h6", "p", "summary"):
        text.extend(visible_tag_values(editorial, tag, language))
    return len(re.sub(r"\s+", "", " ".join(text)))


def faq_page_questions(source: str) -> list[str] | None:
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', source, re.S):
        try:
            data = json.loads(block)
        except json.JSONDecodeError:
            continue
        nodes = data.get("@graph", []) if isinstance(data, dict) else data
        if isinstance(nodes, dict):
            nodes = [nodes]
        for node in nodes:
            if node.get("@type") == "FAQPage":
                entities = node.get("mainEntity", [])
                return [item.get("name", "") for item in entities]
    return None


def check_article_page(page: str, language: str) -> None:
    source = article_source(page)
    if source is None:
        return

    visible_questions = [strip_tags(value) for value in visible_tag_values(source, "summary", language)]
    schema_questions = faq_page_questions(source)
    if len(visible_questions) != 5:
        err(page, f"expected exactly 5 visible FAQ items, found {len(visible_questions)}")
    if schema_questions is None:
        err(page, "missing FAQPage JSON-LD")
    elif len(schema_questions) != 5:
        err(page, f"FAQPage JSON-LD must have exactly 5 questions, found {len(schema_questions)}")
    elif visible_questions != [re.sub(r"\s+", "", question) for question in schema_questions]:
        err(page, "visible FAQ questions do not match FAQPage JSON-LD")

    character_count = editorial_characters(source, language)
    if not 4000 <= character_count <= 6500:
        err(page, f"visible editorial content is {character_count} characters; expected 4,000-6,500")
    else:
        print(f"  article  {page}: {character_count} visible editorial characters, 5 FAQs")


def check_article_pair() -> None:
    if not ARGS.article:
        return
    thai_page, english_page = [os.path.normpath(page) for page in ARGS.article]
    check_article_page(thai_page, "th")
    check_article_page(english_page, "en")


def main() -> int:
    for check in (
        check_cache_version, check_shell, check_consent_gate, check_no_cdn,
        check_classes, check_jsonld, check_paths, check_images,
        check_metadata, check_language_pairs, check_article_pair,
    ):
        check()

    print(f"checked {len(PAGES)} HTML files")
    for w in warnings:
        print(f"  warning  {w}")
    for e in errors:
        print(f"  ERROR    {e}")
    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
