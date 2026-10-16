#!/usr/bin/env python3
"""Generate the static KhanaI Technologies site from products.json and templates."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from string import Template
from typing import Any


ROOT = Path(__file__).resolve().parent
TEMPLATES = ROOT / "templates"
DATA_FILE = ROOT / "products.json"
TODO_RE = re.compile(r"\{\{TODO:[^}]+\}\}")


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def is_todo(value: Any) -> bool:
    return isinstance(value, str) and bool(TODO_RE.search(value))


def render_template(template_name: str, **values: str) -> str:
    source = (TEMPLATES / template_name).read_text(encoding="utf-8")
    return Template(source).substitute(values)


def write_output(name: str, content: str) -> None:
    (ROOT / name).write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")


def status_label(product: dict[str, Any]) -> str:
    return "Live" if product["status"] == "live" else "Releasing soon"


def valid_url(value: Any) -> bool:
    return isinstance(value, str) and bool(value) and not is_todo(value)


def product_policy_cards(products: list[dict[str, Any]]) -> str:
    cards = []
    for product in products:
        slug = esc(product["slug"])
        name = esc(product["name"])
        cards.append(
            f'<article class="card legal-section"><h3>{name}</h3>'
            f'<div class="legal-links"><a href="{slug}-privacy.html">Privacy</a>'
            f'<a href="{slug}-terms.html">Terms</a>'
            f'<a href="{slug}-refund.html">Refunds</a></div></article>'
        )
    return "\n".join(cards)


def footer(company: dict[str, Any], products: list[dict[str, Any]]) -> str:
    product_groups = []
    for product in products:
        slug = esc(product["slug"])
        name = esc(product["name"])
        product_groups.append(
            f'<div class="footer-product"><strong><a href="{slug}.html">{name}</a></strong>'
            f'<div><a href="{slug}-privacy.html">Privacy</a>'
            f'<a href="{slug}-terms.html">Terms</a>'
            f'<a href="{slug}-refund.html">Refunds</a></div></div>'
        )
    return (
        '<footer class="site-footer"><div class="footer-inner">'
        f'<strong>{esc(company["name"])}</strong>'
        '<div class="footer-products">' + "".join(product_groups) + '</div>'
        '<div class="footer-bottom">'
        f'<span>© 2026 {esc(company["name"])}</span>'
        '<span><a href="privacy.html">Privacy</a> · '
        '<a href="terms.html">Terms</a> · <a href="refund.html">Refunds</a></span>'
        '</div></div></footer>'
    )


def og_image_tag(company: dict[str, Any], image: str | None) -> str:
    if not image:
        return ""
    url = company["base_url"] + image
    return f'  <meta property="og:image" content="{esc(url)}">\n'


def base_page(
    *,
    company: dict[str, Any],
    products: list[dict[str, Any]],
    filename: str,
    title: str,
    description: str,
    content: str,
    json_ld: dict[str, Any],
    og_type: str = "website",
    image: str | None = None,
) -> str:
    canonical = company["base_url"] if filename == "index.html" else company["base_url"] + filename
    return render_template(
        "base.html",
        title=esc(title),
        meta_description=esc(description),
        canonical_url=esc(canonical),
        og_title=esc(title),
        og_description=esc(description),
        og_type=esc(og_type),
        og_image=og_image_tag(company, image),
        json_ld=json.dumps(json_ld, ensure_ascii=False, separators=(",", ":")),
        content=content,
        footer=footer(company, products),
    )


def organization_ld(company: dict[str, Any]) -> dict[str, Any]:
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": company["name"],
        "url": company["base_url"],
        "email": company["contact_email"],
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Hyderabad",
            "addressRegion": "Telangana",
            "addressCountry": "IN",
        },
    }


def software_ld(company: dict[str, Any], product: dict[str, Any]) -> dict[str, Any]:
    data: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": product["name"],
        "description": product["description"],
        "url": company["base_url"] + product["slug"] + ".html",
        "applicationCategory": "SoftwareApplication",
        "provider": {
            "@type": "Organization",
            "name": company["name"],
            "url": company["base_url"],
        },
    }
    if product["slug"] in {"winpilot", "winheart", "clipvault"}:
        data["operatingSystem"] = "Windows"
    if valid_url(product.get("store_url")):
        data["installUrl"] = product["store_url"]
    if valid_url(product.get("download_url")):
        data["downloadUrl"] = company["base_url"] + product["download_url"]
    return data


def index_content(company: dict[str, Any], products: list[dict[str, Any]]) -> str:
    pills = []
    cards = []
    for product in products:
        slug = esc(product["slug"])
        name = esc(product["name"])
        pills.append(f'    <a href="{slug}.html">{name}</a>')
        image = ""
        if product["screenshots"]:
            first = product["screenshots"][0]
            image = (
                f'<img src="{esc(first["src"])}" alt="{esc(first["alt"])}" '
                'loading="lazy">'
            )
        features = "".join(f"<li>{esc(item)}</li>" for item in product["features"][:3])
        cards.append(
            f'<article class="card product-card">{image}<div class="card-body">'
            f'<span class="status status-{esc(product["status"])}">{esc(status_label(product))}</span>'
            f'<h3><a class="stretched" href="{slug}.html">{name}</a></h3>'
            f'<p>{esc(product["tagline"])}</p><ul>{features}</ul></div></article>'
        )
    return render_template(
        "index.html",
        contact_email=esc(company["contact_email"]),
        whatsapp_url=esc(company["whatsapp_url"]),
        location=esc(company["location"]),
        product_pills="\n".join(pills),
        product_cards="\n".join(cards),
    )


def pricing_section(product: dict[str, Any]) -> str:
    pricing = product["pricing"]
    if is_todo(pricing):
        return (
            '<section class="section"><div class="container"><div class="section-head">'
            '<span class="eyebrow">Pricing</span><h2>Pricing has not been announced</h2>'
            '<p class="lead">TradingX is releasing soon. Pricing will be published before it becomes available.</p>'
            '</div></div></section>'
        )
    if isinstance(pricing, dict) and "plans" in pricing:
        currency = pricing.get("currency", "")
        cards = []
        for plan in pricing["plans"]:
            period = f' / {esc(plan["period"])}' if plan.get("period") else ""
            cards.append(
                '<article class="card price-card">'
                f'<h3>{esc(plan["name"])}</h3>'
                f'<span class="price">${esc(plan["price"])} {esc(currency)}</span>'
                f'<span class="muted">{period}</span></article>'
            )
        return (
            '<section class="section"><div class="container"><div class="section-head">'
            f'<span class="eyebrow">Pricing</span><h2>{esc(product["name"])} plans</h2></div>'
            f'<div class="grid pricing">{"".join(cards)}</div></div></section>'
        )
    summary = esc(pricing.get("summary", "")) if isinstance(pricing, dict) else ""
    return (
        '<section class="section"><div class="narrow"><span class="eyebrow">Pricing</span>'
        f'<h2>{summary}</h2><p class="lead">No charge applies while the product is offered free.</p>'
        '</div></section>'
    )


def screenshots_section(product: dict[str, Any]) -> str:
    if not product["screenshots"]:
        return ""
    figures = []
    for shot in product["screenshots"]:
        figures.append(
            '<figure><img '
            f'src="{esc(shot["src"])}" alt="{esc(shot["alt"])}" loading="lazy">'
            f'<figcaption>{esc(shot["alt"])}</figcaption></figure>'
        )
    return (
        '<section class="section"><div class="container"><div class="section-head">'
        '<span class="eyebrow">Screenshots</span><h2>Real product screens</h2></div>'
        f'<div class="grid screenshots">{"".join(figures)}</div></div></section>'
    )


def product_content(product: dict[str, Any]) -> str:
    buttons = []
    if valid_url(product.get("store_url")):
        buttons.append(
            f'<a class="button" href="{esc(product["store_url"])}" target="_blank" '
            'rel="noopener noreferrer">Open Microsoft Store</a>'
        )
    if valid_url(product.get("download_url")):
        buttons.append(
            f'<a class="button" href="{esc(product["download_url"])}" download>Download for Windows</a>'
        )
    if not buttons:
        buttons.append('<span class="tag">Releasing soon</span>')
    features = "\n".join(
        f'<article class="card feature-card"><h3>{esc(feature)}</h3></article>'
        for feature in product["features"]
    )
    return render_template(
        "product.html",
        status=esc(product["status"]),
        status_label=esc(status_label(product)),
        name=esc(product["name"]),
        tagline=esc(product["tagline"]),
        description=esc(product["description"]),
        cta_buttons="\n".join(buttons),
        feature_cards=features,
        screenshots_section=screenshots_section(product),
        pricing_section=pricing_section(product),
        slug=esc(product["slug"]),
    )


def section(title: str, *paragraphs: str, bullets: list[str] | None = None) -> str:
    content = "".join(f"<p>{p}</p>" for p in paragraphs)
    if bullets:
        content += "<ul>" + "".join(f"<li>{item}</li>" for item in bullets) + "</ul>"
    return f'<section class="card legal-section"><h2>{title}</h2>{content}</section>'


def product_legal_body(product: dict[str, Any], kind: str, company: dict[str, Any]) -> str:
    slug = product["slug"]
    if slug == "winheart":
        return (TEMPLATES / f"winheart-{kind}-body.html").read_text(encoding="utf-8").strip()

    app = esc(product["name"])
    email_link = f'<a href="mailto:{esc(company["contact_email"])}">{esc(company["contact_email"])}</a>'

    if kind == "privacy":
        extra = ""
        if slug == "winpilot":
            extra = (
                section(
                    "Storage and AI providers",
                    "Chat history is stored locally in encrypted format. If optional cloud synchronization is enabled, chat data may be stored using Supabase over HTTPS.",
                    "Messages may be sent to the selected AI provider, which may include Google Gemini, OpenAI ChatGPT, or Anthropic Claude. Those providers apply their own privacy policies.",
                )
                + section(
                    "Voice, payments, and permissions",
                    "Voice recognition may be processed locally using offline models such as Vosk. Audio is not stored permanently by WinPilot AI.",
                    "Razorpay processes payments. WinPilot AI does not store full card numbers, CVV codes, or bank credentials. The app may request microphone, file-system, and internet access for documented features.",
                )
            )
        elif slug == "clipvault":
            extra = section(
                "Local controls",
                "Current product materials describe local encrypted content, app PIN protection, sensitive-content controls, expiry and clipboard clearing, ignored-app controls, local backups, restore, export, import, retention controls, and separate workspaces.",
            )
        return (
            extra
            + section("Your choices", f"Use the controls available in {app} to manage stored information. Contact {email_link} for support or deletion questions.")
            + section("Changes", "Material updates to this policy will be published on this page with a revised date.")
        )

    if kind == "terms":
        special = ""
        if slug == "tradingx":
            special = section(
                "Trading and financial disclaimer",
                "TradingX provides AI-generated market analysis and directional signals for informational and research purposes only. It is not financial advice.",
                "Users are responsible for their own financial decisions. Past prediction performance does not guarantee future results, and all trading involves risk.",
            )
        return (
            section("Acceptance", f"By accessing or using {app}, you agree to these terms and the linked privacy and refund policies.")
            + section("Authorised use", f"Use {app} only for lawful purposes. Do not reverse engineer, resell, misuse, or redistribute the product without written permission.")
            + section("Software and AI limitations", "Software and AI outputs may be incomplete or inaccurate. Review outputs before acting, keep appropriate backups, and do not rely on the product as a substitute for professional legal, medical, financial, or technical advice.")
            + special
            + section("Availability and updates", f"{app} may be updated as the product develops. Features may change, be suspended, or be discontinued.")
            + section("Governing law and support", f"These terms are governed by the laws of {esc(company['governing_law'])}. Questions may be sent to {email_link}.")
        )

    if slug == "tradingx":
        return section(
            "No charges before release",
            "TradingX is marked releasing soon and is not currently offered for purchase through this website. No product charge or refund applies before a paid release is announced.",
        )

    pricing = product["pricing"]
    free_note = ""
    if isinstance(pricing, dict) and pricing.get("is_free"):
        free_note = section(
            "Current free offer",
            f"{app} is currently offered free for a limited time. No charge applies while the product is downloaded and used under that free offer.",
        )
    elif isinstance(pricing, dict) and any(plan.get("price") == 0 for plan in pricing.get("plans", [])):
        free_note = section(
            "Free plan",
            f"The {app} Free plan has no charge, so there is no payment to refund for that plan.",
        )
    store_note = ""
    if valid_url(product.get("store_url")):
        store_note = section(
            "Microsoft Store purchases",
            "If a paid purchase is made through Microsoft Store, Microsoft processes the transaction. Eligibility, request steps, timing, and any refund are governed by Microsoft’s then-current refund policy and Store terms.",
        )
    return (
        free_note
        + store_note
        + section("Support", f"For product or purchase questions, contact {email_link} and include the Store order reference when applicable.")
    )


LEGAL_TITLES = {
    "privacy": ("Privacy Policy", "This policy explains the information the product may handle and the choices available to users."),
    "terms": ("Terms & Conditions", "These terms apply when you access, install, purchase, or use the product."),
    "refund": ("Refund Policy", "This policy explains when charges exist and which provider handles refund requests."),
}


def product_legal_content(product: dict[str, Any], kind: str, company: dict[str, Any]) -> str:
    title, intro = LEGAL_TITLES[kind]
    if product["slug"] == "winheart":
        intros = {
            "privacy": "This policy explains the information WinHeart AI handles while it diagnoses, repairs, and protects a Windows PC.",
            "terms": "These terms apply to the purchase, installation, and use of WinHeart AI.",
            "refund": "This policy applies to WinHeart AI digital licences sold by KhanaI Technologies.",
        }
        intro = intros[kind]
        if kind == "refund":
            title = "Refund & Cancellation Policy"
    data_items = [esc(item) for item in product["data_collected"] if not is_todo(item)]
    data_collected_section = ""
    if kind == "privacy" and product["slug"] != "winheart":
        if data_items:
            data_collected_section = section(
                "Information handled",
                f"{esc(product['name'])} may handle the following information when you use the relevant features:",
                bullets=data_items,
            )
        else:
            data_collected_section = section(
                "Before release",
                f"{esc(product['name'])} is not publicly available. Its data practices will be published before release.",
            )
    return render_template(
        "legal.html",
        app_name=esc(product["name"]),
        policy_title=esc(title),
        policy_intro=esc(intro),
        last_updated=esc(company["last_updated"]),
        effective_date=esc(company["last_updated"]),
        governing_law=esc(company["governing_law"]),
        contact_email=esc(company["contact_email"]),
        data_collected_section=data_collected_section,
        legal_body=product_legal_body(product, kind, company),
        data_collected=esc(", ".join(item for item in product["data_collected"] if not is_todo(item))),
        slug=esc(product["slug"]),
    )


def company_legal_body(kind: str, company: dict[str, Any]) -> tuple[str, str, str]:
    email = f'<a href="mailto:{esc(company["contact_email"])}">{esc(company["contact_email"])}</a>'
    if kind == "privacy":
        return (
            "Privacy Policy",
            "This company-level notice explains how the static KhanaI Technologies website handles contact and directs visitors to product-specific policies.",
            section("Website use", "This static website does not include an account system or server-side contact form. Email and WhatsApp links open the visitor’s chosen service, whose own privacy terms apply.")
            + section("Product data", "Each product has a dedicated privacy policy describing the information it handles. Use the product links below for the policy that applies to you.")
            + section("Contact", f"Questions about this notice may be sent to {email}.")
            + section("Changes", "Material updates will be published on this page with a revised last-updated date."),
        )
    if kind == "terms":
        return (
            "Terms & Conditions",
            "These company-level terms apply to use of the KhanaI Technologies website. Product-specific terms are linked below.",
            section("Website information", "Website content is provided for general product and company information. Product availability, features, pricing, and policies are stated on the relevant product pages.")
            + section("Responsible use", "Do not misuse the website, attempt unauthorized access, or use KhanaI Technologies products for unlawful activity.")
            + section("AI and market information", "AI outputs may be incomplete or inaccurate and should be independently reviewed. TradingX information is not financial advice, and all trading involves risk.")
            + section("Intellectual property", "KhanaI Technologies product names, software, code, designs, and site materials remain protected by applicable intellectual-property laws.")
            + section("Governing law", f"These terms are governed by the laws of {esc(company['governing_law'])}. Questions may be sent to {email}."),
        )
    return (
        "Refund Policy",
        "Refund handling depends on the product, whether a charge was made, and which payment provider processed it.",
        section("Free products and plans", "When a product or plan is provided free of charge, no payment has been collected and there is no charge to refund.")
        + section("Microsoft Store purchases", "For paid purchases processed through Microsoft Store, Microsoft’s then-current refund policy and Store terms determine eligibility and processing.")
        + section("Other payment providers", "For purchases processed outside Microsoft Store, the applicable product-specific refund page explains the eligibility and request process.")
        + section("Product policies", "Use the links below to read the policy for the product you downloaded or purchased."),
    )


def company_legal_content(kind: str, company: dict[str, Any], products: list[dict[str, Any]]) -> str:
    title, intro, body = company_legal_body(kind, company)
    return render_template(
        "company-legal.html",
        policy_title=esc(title),
        policy_intro=esc(intro),
        last_updated=esc(company["last_updated"]),
        governing_law=esc(company["governing_law"]),
        contact_email=esc(company["contact_email"]),
        legal_body=body,
        product_policy_cards=product_policy_cards(products),
    )


def build_sitemap(company: dict[str, Any], products: list[dict[str, Any]]) -> str:
    files = ["", "privacy.html", "terms.html", "refund.html"]
    for product in products:
        slug = product["slug"]
        files.extend([f"{slug}.html", f"{slug}-privacy.html", f"{slug}-terms.html", f"{slug}-refund.html"])
    urls = "\n".join(
        f"  <url><loc>{html.escape(company['base_url'] + filename)}</loc></url>" for filename in files
    )
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n'


def main() -> None:
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    company = data["company"]
    products = data["products"]

    slugs = [product["slug"] for product in products]
    if len(products) != 4 or len(set(slugs)) != 4:
        raise ValueError("products.json must contain exactly four products with unique slugs")
    for product in products:
        if product["status"] not in {"live", "soon"}:
            raise ValueError(f"Invalid status for {product['slug']}")

    index = base_page(
        company=company,
        products=products,
        filename="index.html",
        title="KhanaI Technologies | AI products and engineering",
        description="KhanaI Technologies builds WinPilot AI, WinHeart AI, ClipVault AI, and TradingX.",
        content=index_content(company, products),
        json_ld=organization_ld(company),
    )
    write_output("index.html", index)

    for product in products:
        filename = product["slug"] + ".html"
        first_image = product["screenshots"][0]["src"] if product["screenshots"] else None
        page = base_page(
            company=company,
            products=products,
            filename=filename,
            title=f"{product['name']} | KhanaI Technologies",
            description=f"{product['name']}: {product['description']}",
            content=product_content(product),
            json_ld=software_ld(company, product),
            og_type="website",
            image=first_image,
        )
        write_output(filename, page)

        for kind in ("privacy", "terms", "refund"):
            legal_filename = f"{product['slug']}-{kind}.html"
            legal_title = LEGAL_TITLES[kind][0]
            legal_page = base_page(
                company=company,
                products=products,
                filename=legal_filename,
                title=f"{product['name']} {legal_title} | KhanaI Technologies",
                description=f"{legal_title} for {product['name']} by KhanaI Technologies.",
                content=product_legal_content(product, kind, company),
                json_ld=software_ld(company, product),
            )
            write_output(legal_filename, legal_page)

    for kind in ("privacy", "terms", "refund"):
        title = LEGAL_TITLES[kind][0]
        write_output(
            f"{kind}.html",
            base_page(
                company=company,
                products=products,
                filename=f"{kind}.html",
                title=f"{title} | KhanaI Technologies",
                description=f"Company-level {title.lower()} and product policy links for KhanaI Technologies.",
                content=company_legal_content(kind, company, products),
                json_ld=organization_ld(company),
            ),
        )

    write_output(
        "404.html",
        base_page(
            company=company,
            products=products,
            filename="404.html",
            title="Page not found | KhanaI Technologies",
            description="The requested KhanaI Technologies page could not be found.",
            content=render_template("404.html"),
            json_ld=organization_ld(company),
        ),
    )
    write_output("sitemap.xml", build_sitemap(company, products))
    write_output("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {company['base_url']}sitemap.xml")

    print(f"Generated {1 + len(products) * 4 + 3 + 1} HTML pages, sitemap.xml, and robots.txt.")


if __name__ == "__main__":
    main()
