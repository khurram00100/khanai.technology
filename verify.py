#!/usr/bin/env python3
"""Verify generated static pages using only the Python standard library."""

from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parent
TODO_RE = re.compile(r"\{\{TODO:[^}]+\}\}")
REQUIRED_PRODUCT_FIELDS = {
    "slug",
    "name",
    "tagline",
    "status",
    "store_url",
    "download_url",
    "description",
    "features",
    "screenshots",
    "pricing",
    "data_collected",
}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []
        self.ids: set[str] = set()
        self.missing_alt: list[str] = []
        self.title_parts: list[str] = []
        self.in_title = False
        self.meta_description: str | None = None
        self.canonical: str | None = None
        self.json_ld_parts: list[str] = []
        self.in_json_ld = False
        self.external_dependencies: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if data.get("id"):
            self.ids.add(str(data["id"]))
        if tag == "a" and data.get("href"):
            self.links.append(("href", str(data["href"])))
        if tag in {"img", "script", "source"} and data.get("src"):
            self.links.append(("src", str(data["src"])))
        if tag == "link" and data.get("href"):
            rel = str(data.get("rel", ""))
            href = str(data["href"])
            self.links.append(("href", href))
            if rel == "canonical":
                self.canonical = href
            if rel == "stylesheet" and urlsplit(href).scheme in {"http", "https"}:
                self.external_dependencies.append(href)
        if tag == "script":
            script_type = str(data.get("type", ""))
            if script_type == "application/ld+json":
                self.in_json_ld = True
            src = data.get("src")
            if src and urlsplit(str(src)).scheme in {"http", "https"}:
                self.external_dependencies.append(str(src))
        if tag == "img" and "alt" not in data:
            self.missing_alt.append(str(data.get("src", "<unknown>")))
        if tag == "meta" and data.get("name") == "description":
            self.meta_description = str(data.get("content", ""))
        if tag == "title":
            self.in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False
        if tag == "script" and self.in_json_ld:
            self.in_json_ld = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)
        if self.in_json_ld:
            self.json_ld_parts.append(data)

    @property
    def title(self) -> str:
        return "".join(self.title_parts).strip()

    @property
    def json_ld(self) -> str:
        return "".join(self.json_ld_parts).strip()


def is_external(ref: str) -> bool:
    split = urlsplit(ref)
    return split.scheme in {"http", "https", "mailto", "tel", "data"} or ref.startswith("//")


def target_for(page: Path, ref: str) -> tuple[Path, str]:
    split = urlsplit(ref)
    path_part = unquote(split.path)
    if not path_part:
        return page, split.fragment
    if path_part.startswith("/"):
        target = ROOT / path_part.lstrip("/")
    else:
        target = page.parent / path_part
    return target.resolve(), split.fragment


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict-todos", action="store_true", help="Fail on TODO markers in source data too")
    args = parser.parse_args()

    failures: list[str] = []
    warnings: list[str] = []
    pages = sorted(ROOT.glob("*.html"))
    parsed: dict[Path, PageParser] = {}

    if not pages:
        failures.append("No generated HTML pages found")

    for page in pages:
        text = page.read_text(encoding="utf-8")
        page_parser = PageParser()
        page_parser.feed(text)
        parsed[page.resolve()] = page_parser

        if not page_parser.title:
            failures.append(f"{page.name}: missing <title>")
        if not page_parser.meta_description:
            failures.append(f"{page.name}: missing meta description")
        if not page_parser.canonical:
            failures.append(f"{page.name}: missing canonical URL")
        if page_parser.missing_alt:
            failures.append(f"{page.name}: image(s) missing alt text: {', '.join(page_parser.missing_alt)}")
        if page_parser.external_dependencies:
            failures.append(f"{page.name}: external script/stylesheet dependency: {', '.join(page_parser.external_dependencies)}")
        if TODO_RE.search(text):
            failures.append(f"{page.name}: contains an unfilled TODO marker")
        if "khanaitechnologies" in text or "khanai.technologies" in text:
            failures.append(f"{page.name}: contains an inconsistent company spelling")
        if page_parser.json_ld:
            try:
                json.loads(page_parser.json_ld)
            except json.JSONDecodeError as exc:
                failures.append(f"{page.name}: invalid JSON-LD: {exc}")
        else:
            failures.append(f"{page.name}: missing JSON-LD")

    titles: dict[str, str] = {}
    descriptions: dict[str, str] = {}
    canonicals: dict[str, str] = {}
    for page, page_parser in parsed.items():
        for label, value, seen in (
            ("title", page_parser.title, titles),
            ("meta description", page_parser.meta_description or "", descriptions),
            ("canonical", page_parser.canonical or "", canonicals),
        ):
            if value in seen:
                failures.append(f"{page.name}: duplicate {label} also used by {seen[value]}")
            else:
                seen[value] = page.name

    for page, page_parser in parsed.items():
        for attr, ref in page_parser.links:
            if not ref or ref.startswith("#"):
                if ref.startswith("#") and ref[1:] and ref[1:] not in page_parser.ids:
                    failures.append(f"{page.name}: missing same-page anchor {ref}")
                continue
            if is_external(ref):
                continue
            target, fragment = target_for(page, ref)
            try:
                target.relative_to(ROOT.resolve())
            except ValueError:
                failures.append(f"{page.name}: internal {attr} escapes site root: {ref}")
                continue
            if not target.exists():
                failures.append(f"{page.name}: broken internal {attr}: {ref}")
                continue
            if fragment and target.suffix.lower() == ".html":
                target_parser = parsed.get(target)
                if target_parser is None:
                    text = target.read_text(encoding="utf-8")
                    target_parser = PageParser()
                    target_parser.feed(text)
                    parsed[target] = target_parser
                if fragment not in target_parser.ids:
                    failures.append(f"{page.name}: missing anchor #{fragment} in {target.name}")

    data = json.loads((ROOT / "products.json").read_text(encoding="utf-8"))
    products = data.get("products", [])
    if len(products) != 4:
        failures.append("products.json must contain exactly four products")
    for product in products:
        missing = REQUIRED_PRODUCT_FIELDS - set(product)
        if missing:
            failures.append(f"products.json {product.get('slug', '<unknown>')}: missing fields {sorted(missing)}")
    source_text = (ROOT / "products.json").read_text(encoding="utf-8")
    source_todos = TODO_RE.findall(source_text)
    if source_todos:
        message = "products.json unresolved source fields: " + ", ".join(sorted(set(source_todos)))
        if args.strict_todos:
            failures.append(message)
        else:
            warnings.append(message)

    for public_file in [ROOT / "sitemap.xml", ROOT / "robots.txt", ROOT / "assets" / "site.css"]:
        if not public_file.exists():
            failures.append(f"Missing required file: {public_file.relative_to(ROOT)}")
        elif TODO_RE.search(public_file.read_text(encoding="utf-8")):
            failures.append(f"{public_file.name}: contains an unfilled TODO marker")

    for warning in warnings:
        print(f"WARNING: {warning}")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        print(f"Verification failed with {len(failures)} issue(s).")
        return 1
    print(f"Verification passed for {len(pages)} HTML pages. Internal links, image alt text, metadata, JSON-LD, and public TODO markers are clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
