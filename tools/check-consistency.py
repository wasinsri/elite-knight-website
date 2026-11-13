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
from html.parser import HTMLParser
from urllib.parse import parse_qs, unquote, urlparse

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
            if target.startswith("/"):
                # root-relative (used by 404.html, which is served for any missing path)
                resolved = os.path.normpath(os.path.join(ROOT, target.lstrip("/")))
            else:
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


# 11. article layout ---------------------------------------------------------
class ArticleTagBalanceParser(HTMLParser):
    VOID_ELEMENTS = {
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr",
    }

    def __init__(self) -> None:
        super().__init__()
        self.stack: list[str] = []
        self.mismatches: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in self.VOID_ELEMENTS:
            self.stack.append(tag)

    def handle_endtag(self, tag: str) -> None:
        if not self.stack or self.stack[-1] != tag:
            expected = self.stack[-1] if self.stack else "no open tag"
            self.mismatches.append(f"closed </{tag}> while expecting </{expected}>")
            return
        self.stack.pop()


class ArticleStructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.stack: list[tuple[str, set[str]]] = []
        self.article_depth: int | None = None
        self.direct_content_divs = 0
        self.cta_outside_prose = False
        self.faq_outside_prose = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        classes = set((values.get("class") or "").split())
        if tag == "article":
            self.article_depth = len(self.stack)
        elif self.article_depth is not None:
            if tag == "div" and len(self.stack) == self.article_depth + 1:
                self.direct_content_divs += 1
            inside_prose = any("article-prose" in ancestor_classes for _, ancestor_classes in self.stack)
            if tag == "section" and "article-cta" in classes and not inside_prose:
                self.cta_outside_prose = True
            if tag == "details" and not inside_prose:
                self.faq_outside_prose = True
        if tag not in ArticleTagBalanceParser.VOID_ELEMENTS:
            self.stack.append((tag, classes))

    def handle_endtag(self, tag: str) -> None:
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()
        if tag == "article":
            self.article_depth = None


def check_article_layout() -> None:
    """Keep every localized article on the shared readable article shell."""
    article_pages = [
        page for page in PAGES
        if page.startswith(("articles/", "en/articles/"))
    ]
    required_outer_classes = {"mx-auto", "max-w-4xl", "px-5", "py-16", "lg:px-8"}
    required_share_classes = {"mb-10", "flex", "flex-wrap", "gap-3"}

    for page in article_pages:
        src = SOURCES[page]
        tag_parser = ArticleTagBalanceParser()
        tag_parser.feed(src)
        if tag_parser.mismatches or tag_parser.stack:
            detail = tag_parser.mismatches[0] if tag_parser.mismatches else f"unclosed <{tag_parser.stack[-1]}>"
            err(page, f"unbalanced HTML tags: {detail}")

        structure_parser = ArticleStructureParser()
        structure_parser.feed(src)
        if structure_parser.direct_content_divs != 1:
            err(page, f"expected 1 top-level article content wrapper, found {structure_parser.direct_content_divs}")
        if structure_parser.cta_outside_prose:
            err(page, "article CTA must remain inside article-prose")
        if structure_parser.faq_outside_prose:
            err(page, "article FAQ must remain inside article-prose")

        article_match = re.search(r"<article\b[^>]*>(.*?)</article>", src, re.S | re.I)
        if not article_match:
            err(page, "missing <article> content wrapper")
            continue

        article = article_match.group(1)
        if article.count("max-w-4xl") != 2:
            err(page, "article must use max-w-4xl only for the hero and outer content wrapper")
        hero_match = re.search(
            r'<header\b[^>]*class="[^"]*\bpage-hero\b[^"]*"[^>]*>.*?</header>',
            article,
            re.S | re.I,
        )
        if not hero_match:
            err(page, "missing article page hero")
            continue

        hero = hero_match.group(0)
        after_hero = article[hero_match.end():]
        outer_match = re.match(r'\s*<div\b[^>]*class="([^"]*)"', after_hero, re.S | re.I)
        outer_classes = set(outer_match.group(1).split()) if outer_match else set()
        if not required_outer_classes.issubset(outer_classes):
            err(page, "article body must start with the standard max-w-4xl py-16 content wrapper")

        prose_matches = list(re.finditer(r'class="([^"]*\barticle-prose\b[^"]*)"', after_hero))
        if len(prose_matches) != 1:
            err(page, f"expected exactly 1 article-prose wrapper, found {len(prose_matches)}")
        elif "space-y-6" not in prose_matches[0].group(1).split():
            err(page, "article-prose wrapper must include space-y-6")

        share_count = article.count('class="share-button"')
        if share_count != 3:
            err(page, f"expected exactly 3 article share buttons, found {share_count}")
        if 'class="share-button"' in hero:
            err(page, "article share buttons must be below the hero")

        share_wrapper = re.search(
            r'<div\b[^>]*class="([^"]*)"[^>]*>\s*<a\b[^>]*class="share-button"',
            after_hero,
            re.S | re.I,
        )
        share_classes = set(share_wrapper.group(1).split()) if share_wrapper else set()
        if not required_share_classes.issubset(share_classes):
            err(page, "share buttons must use the standard mb-10 flex-wrap wrapper")
        if prose_matches and share_wrapper and share_wrapper.start() > prose_matches[0].start():
            err(page, "share buttons must appear before article-prose")

        language = "en" if page.startswith("en/") else "th"
        if src.count('class="ek-takeaways"') != 1:
            err(page, "expected exactly 1 key-takeaways panel")
        if src.count('class="ek-toc"') != 1:
            err(page, "expected exactly 1 article table of contents")
        if src.count("ek-related") != 1:
            err(page, "expected exactly 1 related-articles section")
        else:
            related = re.search(
                r'<nav\b[^>]*class="[^"]*\bek-related\b[^"]*"[^>]*>(.*?)</nav>',
                article,
                re.S | re.I,
            )
            related_links = re.findall(r'<a\b[^>]*href="([^"]+)"', related.group(1), re.I) if related else []
            if len(related_links) != 3:
                err(page, f"related-articles section must contain exactly 3 links, found {len(related_links)}")
            if any(href.startswith(("http://", "https://")) for href in related_links):
                err(page, "related-articles links must stay internal")

        cta = re.search(
            r'<section\b[^>]*class="[^"]*\barticle-cta\b[^"]*"[^>]*>(.*?)</section>',
            article,
            re.S | re.I,
        )
        if not cta:
            err(page, "missing article CTA")
        else:
            cta_links = re.findall(r'<a\b[^>]*href="([^"]+)"', cta.group(1), re.I)
            if len(cta_links) != 2 or not any("contact.html" in href for href in cta_links):
                err(page, "article CTA must contain one service link and one contact link")

        if "Data · AI · Governance" not in src:
            err(page, "header brand is missing the standard Data · AI · Governance tagline")

        footer_match = re.search(r'<footer\b[^>]*>(.*?)</footer>', src, re.S | re.I)
        footer = footer_match.group(1) if footer_match else ""
        footer_markers = (
            'data-th="บริษัท เอลีท ไนท์ จำกัด"',
            'data-en="Elite Knight Co., Ltd."',
            'data-th="เกี่ยวกับเรา"',
            'data-en="About"',
            'data-th="เปิดบริการ: จันทร์ - ศุกร์ 9.00 - 17.30 น."',
            'data-en="Office hours: Monday - Friday, 9:00 AM - 5:30 PM"',
            'https://www.linkedin.com/company/elite-knight/',
            'https://www.facebook.com/ek.co.th',
            'tel:+66636641555',
            'mailto:info@ek.co.th',
        )
        for marker in footer_markers:
            if marker not in footer:
                err(page, f"standard article footer is missing: {marker}")

        canonical_match = re.search(r'<link rel="canonical" href="([^"]+)"', src)
        canonical = canonical_match.group(1) if canonical_match else ""
        share_hrefs = []
        for anchor in re.findall(r'<a\b[^>]*\bclass="[^"]*\bshare-button\b[^"]*"[^>]*>', article, re.I):
            href_match = re.search(r'\bhref="([^"]+)"', anchor, re.I)
            if href_match:
                share_hrefs.append(href_match.group(1))
        for share_href in share_hrefs:
            query = parse_qs(urlparse(html.unescape(share_href)).query)
            shared_url = query.get("url", query.get("u", [""]))[0]
            if unquote(shared_url) != canonical:
                err(page, "article share button URL does not match the canonical URL")
                break

        for match in re.finditer(
            rf'<(?P<tag>[a-z][a-z0-9]*)\b(?P<attrs>[^>]*\bdata-{language}="(?P<value>[^"]*)"[^>]*)>'
            rf'(?P<inner>[^<]*)</(?P=tag)>',
            src,
            re.S | re.I,
        ):
            expected = re.sub(r"\s+", " ", html.unescape(match.group("value"))).strip()
            actual = re.sub(r"\s+", " ", html.unescape(match.group("inner"))).strip()
            if actual != expected:
                err(page, f"visible {language.upper()} text does not match its data-{language} value: {actual[:55]}")

        if language == "en":
            for href in re.findall(r'<a\b[^>]*href="([^"]+\.html(?:#[^"]*)?)"', article, re.I):
                if href.startswith(("http://", "https://")):
                    continue
                resolved = os.path.relpath(
                    os.path.normpath(os.path.join(ROOT, os.path.dirname(page), href.split("#")[0])),
                    ROOT,
                )
                if not resolved.startswith("en/"):
                    err(page, f"English article links to a Thai page: {href}")
            header = src[:src.find("<main")]
            for anchor in re.findall(r'<a\b[^>]*href="[^"]+"[^>]*>', header, re.I):
                if "data-lang-button" in anchor:
                    continue
                href_match = re.search(r'href="([^"]+\.html(?:#[^"]*)?)"', anchor, re.I)
                if not href_match:
                    continue
                href = href_match.group(1)
                resolved = os.path.relpath(
                    os.path.normpath(os.path.join(ROOT, os.path.dirname(page), href.split("#")[0])),
                    ROOT,
                )
                if not resolved.startswith("en/"):
                    err(page, f"English article header links to a Thai page: {href}")


def check_article_metadata() -> None:
    """Require complete social, language, and Article metadata on every article."""
    article_pages = [page for page in PAGES if page.startswith(("articles/", "en/articles/"))]
    expected_author = "https://www.ek.co.th/about.html#wasin-srisawat"
    expected_publisher = "https://www.ek.co.th/#organization"
    sitemap = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()

    for page in article_pages:
        src = SOURCES[page]
        for meta in ("twitter:image", "og:image:alt", "og:locale", "og:locale:alternate"):
            if not re.search(rf'<meta (?:name|property)="{re.escape(meta)}" content="[^"]+"', src):
                err(page, f"missing {meta} metadata")

        canonical_match = re.search(r'<link rel="canonical" href="([^"]+)"', src)
        canonical = canonical_match.group(1) if canonical_match else ""
        thai_canonical = canonical.replace("/en/articles/", "/articles/")
        x_default = re.search(r'<link rel="alternate" hreflang="x-default" href="([^"]+)"', src)
        if not x_default or x_default.group(1) != thai_canonical:
            err(page, "x-default hreflang must point to the Thai canonical URL")
        if canonical and f"<loc>{canonical}</loc>" not in sitemap:
            err(page, "canonical URL is missing from sitemap.xml")

        article_schema = None
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', src, re.S):
            try:
                data = json.loads(block)
            except json.JSONDecodeError:
                continue
            nodes = data.get("@graph", []) if isinstance(data, dict) else []
            for node in nodes:
                if node.get("@type") in ("Article", "BlogPosting"):
                    article_schema = node
                    break
            if article_schema:
                break
        if not article_schema:
            err(page, "missing Article or BlogPosting JSON-LD")
            continue
        if not article_schema.get("image"):
            err(page, "Article JSON-LD is missing image")
        if article_schema.get("author", {}).get("@id") != expected_author:
            err(page, "Article JSON-LD author must identify Wasin Srisawat")
        if article_schema.get("publisher", {}).get("@id") != expected_publisher:
            err(page, "Article JSON-LD publisher must identify Elite Knight")


# 12. new article editorial length and FAQ parity ---------------------------
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
        check_metadata, check_language_pairs, check_article_layout,
        check_article_metadata,
        check_article_pair,
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
