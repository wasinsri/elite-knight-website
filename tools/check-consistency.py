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
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", "node_modules", "tools", ".github"}

errors: list[str] = []
warnings: list[str] = []


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


def main() -> int:
    for check in (
        check_cache_version, check_shell, check_consent_gate, check_no_cdn,
        check_classes, check_jsonld, check_paths, check_images,
        check_metadata, check_language_pairs,
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
