from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parent
CORE_PAGES = {
    "index.html",
    "products.html",
    "winpilot.html",
    "winheart.html",
    "clipvault.html",
    "winqor.html",
    "tradingx.html",
    "solutions.html",
    "company.html",
    "contact.html",
}
LEGAL_PAGES = {
    "privacy.html",
    "terms.html",
    "refund.html",
    "winheart-privacy.html",
    "winheart-terms.html",
    "winheart-refund.html",
}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []
        self.assets: list[str] = []
        self.images_without_alt: list[str] = []
        self.titles: list[str] = []
        self.meta_descriptions = 0
        self.canonicals = 0
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "a" and values.get("href"):
            self.links.append(values["href"] or "")
        if tag == "img":
            src = values.get("src", "") or ""
            self.assets.append(src)
            if not (values.get("alt") or "").strip():
                self.images_without_alt.append(src or "<missing src>")
        if tag in {"script", "source"} and values.get("src"):
            self.assets.append(values["src"] or "")
        if tag == "link" and values.get("href"):
            rel = (values.get("rel") or "").lower()
            if "canonical" in rel:
                self.canonicals += 1
            else:
                self.assets.append(values["href"] or "")
        if tag == "meta" and (values.get("name") or "").lower() == "description":
            if (values.get("content") or "").strip():
                self.meta_descriptions += 1
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title and data.strip():
            self.titles.append(data.strip())


def local_target(source: Path, value: str) -> Path | None:
    if not value or value.startswith(("#", "mailto:", "tel:", "javascript:")):
        return None
    # Cloudflare email-obfuscation URLs can remain in preserved legacy legal pages.
    if value.startswith("/cdn-cgi/"):
        return None
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc:
        return None
    path = unquote(parsed.path)
    if not path:
        return None
    if path.startswith("/"):
        return ROOT / path.lstrip("/")
    return (source.parent / path).resolve()


def main() -> int:
    errors: list[str] = []
    all_pages = sorted(ROOT.glob("*.html"))
    missing_pages = (CORE_PAGES | LEGAL_PAGES) - {page.name for page in all_pages}
    if missing_pages:
        errors.append(f"Missing required pages: {', '.join(sorted(missing_pages))}")

    titles: dict[str, str] = {}
    for page in all_pages:
        text = page.read_text(encoding="utf-8")
        if "{{TODO:" in text:
            errors.append(f"{page.name}: unfilled TODO marker")
        parser = PageParser()
        parser.feed(text)
        if parser.images_without_alt:
            errors.append(f"{page.name}: missing alt text for {parser.images_without_alt}")
        for value in parser.links + parser.assets:
            target = local_target(page, value)
            if target is not None and not target.exists():
                errors.append(f"{page.name}: missing local target {value}")
        if page.name in CORE_PAGES:
            if len(parser.titles) != 1:
                errors.append(f"{page.name}: expected one title")
            else:
                titles[page.name] = parser.titles[0]
            if parser.meta_descriptions != 1:
                errors.append(f"{page.name}: expected one meta description")
            if parser.canonicals != 1:
                errors.append(f"{page.name}: expected one canonical URL")

    if len(set(titles.values())) != len(titles):
        errors.append("Core page titles are not unique")

    required_media = {
        "winheart-dashboard.png",
        "winheart-repair.png",
        "winheart-settings.png",
        "clipvault-logo.png",
        "clipvault-home.png",
        "clipvault-library.png",
        "clipvault-features.png",
        "WinHeartAI-Setup-1.0.0.exe",
    }
    for item in sorted(required_media):
        if not (ROOT / item).exists():
            errors.append(f"Missing protected product asset: {item}")

    if (ROOT / "CNAME").exists():
        errors.append("CNAME must not exist until a custom domain is purchased")

    combined = "\n".join(page.read_text(encoding="utf-8") for page in all_pages)
    for token in (
        "4f7a0d00-d85a-42c8-affd-9a7d0c5e8b7e",
        "35ac7216-bd1a-46c2-80d3-5d968f475cba",
        "cf6973bd-cce9-4bb4-be9f-8101fb07d646",
        "9NKN32V0WPDZ",
        "9P6M976T1XTS",
        "9NV4L13DRKD0",
    ):
        if token not in combined:
            errors.append(f"Required product media or Store reference missing: {token}")

    if errors:
        print("Verification failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Verified {len(all_pages)} HTML pages: links, assets, alt text, SEO, and product media are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
