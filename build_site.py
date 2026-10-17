from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE_URL = "https://khurram00100.github.io/khanai.technology/"
BRAND = "KhanaI Technologies"

WINPILOT_STORE = "https://apps.microsoft.com/store/detail/9NKN32V0WPDZ?cid=DevShareMCLPCS"
WINHEART_STORE = "https://apps.microsoft.com/detail/9P6M976T1XTS?hl=en-us&gl=IN&ocid=pdpshare"
CLIPVAULT_STORE = "https://apps.microsoft.com/detail/9NV4L13DRKD0?hl=en-us&gl=IN&ocid=pdpshare"
WINPILOT_SCREEN_1 = "https://github.com/user-attachments/assets/4f7a0d00-d85a-42c8-affd-9a7d0c5e8b7e"
WINPILOT_SCREEN_2 = "https://github.com/user-attachments/assets/35ac7216-bd1a-46c2-80d3-5d968f475cba"
WINPILOT_VIDEO = "https://github.com/user-attachments/assets/cf6973bd-cce9-4bb4-be9f-8101fb07d646"


PRODUCTS = [
    {
        "slug": "winpilot",
        "name": "WinPilot AI",
        "label": "Desktop AI · Flagship",
        "status": "Live on Microsoft Store",
        "status_class": "",
        "summary": "A unified Windows AI workspace for chat, documents, image understanding, voice, authentication, and focused productivity workflows.",
        "image": WINPILOT_SCREEN_1,
        "alt": "WinPilot AI desktop workspace screenshot",
        "pills": ["Windows", "Multi-model", "Productivity"],
    },
    {
        "slug": "winheart",
        "name": "WinHeart AI",
        "label": "Windows assistant · Early launch",
        "status": "Free for a limited time",
        "status_class": "",
        "summary": "Diagnose, understand, and work through PC health, repair, change tracking, notes, reports, and privacy controls in one local-first workspace.",
        "image": "winheart-dashboard.png",
        "alt": "WinHeart AI dashboard with system overview and quick actions",
        "pills": ["Windows", "Local-first", "PC health"],
    },
    {
        "slug": "clipvault",
        "name": "ClipVault AI",
        "label": "Private Windows workspace",
        "status": "Live on Microsoft Store",
        "status_class": "",
        "summary": "Capture, search, organise, understand, and protect clipboard history, screenshots, text, links, and files in a private local workspace.",
        "image": "clipvault-home.png",
        "alt": "ClipVault AI home workspace with quick capture and recent clips",
        "pills": ["Windows", "Local storage", "Search"],
    },
    {
        "slug": "winqor",
        "name": "WinQor",
        "label": "Compact AI model family",
        "status": "Releasing soon",
        "status_class": "soon",
        "summary": "An upcoming family of compact AI models planned in 150M, 300M, and 1B parameter editions for different compute and deployment needs.",
        "image": None,
        "alt": "",
        "pills": ["150M", "300M", "1B"],
    },
    {
        "slug": "tradingx",
        "name": "TradingX",
        "label": "AI trading intelligence",
        "status": "Research product",
        "status_class": "soon",
        "summary": "Market intelligence for currencies, gold, and Bitcoin with automated data pipelines and directional machine-learning signals.",
        "image": None,
        "alt": "",
        "pills": ["Forex", "Gold", "Bitcoin"],
    },
]


def nav() -> str:
    return """
<a class="skip-link" href="#main">Skip to content</a>
<div class="site-progress" aria-hidden="true"></div>
<header class="site-nav">
  <div class="container nav-inner">
    <a class="brand" href="index.html" aria-label="KhanaI Technologies home">
      <span class="brand-mark" aria-hidden="true">K</span><span>KhanaI Technologies</span>
    </a>
    <nav class="nav-links" aria-label="Primary navigation">
      <a href="index.html">Home</a>
      <a href="products.html">Products</a>
      <a href="solutions.html">Solutions</a>
      <a href="company.html">Company</a>
      <a href="contact.html">Contact</a>
    </nav>
    <div class="nav-actions">
      <a class="button button-compact nav-cta" href="products.html">Explore products <span class="arrow">↗</span></a>
      <button class="nav-toggle" type="button" aria-label="Open navigation" aria-expanded="false"><span></span></button>
    </div>
  </div>
</header>"""


def footer() -> str:
    return """
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="brand" href="index.html"><span class="brand-mark" aria-hidden="true">K</span><span>KhanaI Technologies</span></a>
        <p>AI engineering company building WinPilot AI, WinHeart AI, ClipVault AI, WinQor, TradingX, voice systems, company AI, automation chatbots, and database intelligence.</p>
      </div>
      <div class="footer-col"><h3>Products</h3><a href="winpilot.html">WinPilot AI</a><a href="winheart.html">WinHeart AI</a><a href="clipvault.html">ClipVault AI</a><a href="winqor.html">WinQor</a><a href="tradingx.html">TradingX</a></div>
      <div class="footer-col"><h3>Company</h3><a href="solutions.html">Solutions</a><a href="company.html">About us</a><a href="company.html#technology">Tech stack</a><a href="contact.html">Contact</a></div>
      <div class="footer-col"><h3>Legal</h3><a href="privacy.html">Privacy Policy</a><a href="terms.html">Terms of Service</a><a href="refund.html">Refund Policy</a><a href="mailto:winpilotai@gmail.com?subject=Issue%20report">Report an issue</a></div>
    </div>
    <div class="footer-bottom"><span>© 2026 KhanaI Technologies. All rights reserved.</span><span>Developed by Shamsheer Khan Khurrum · Hyderabad, India</span></div>
  </div>
</footer>"""


def schema_for_product(name: str, description: str, path: str, install_url: str | None = None) -> dict:
    data = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": name,
        "description": description,
        "url": BASE_URL + path,
        "applicationCategory": "SoftwareApplication",
        "operatingSystem": "Windows",
        "provider": {"@type": "Organization", "name": BRAND, "url": BASE_URL},
    }
    if install_url:
        data["installUrl"] = install_url
    return data


def render(filename: str, title: str, description: str, body: str, schema: dict | None = None) -> None:
    canonical = BASE_URL if filename == "index.html" else BASE_URL + filename
    schema = schema or {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": BRAND,
        "url": BASE_URL,
        "email": "winpilotai@gmail.com",
        "address": {"@type": "PostalAddress", "addressLocality": "Hyderabad", "addressRegion": "Telangana", "addressCountry": "IN"},
    }
    document = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description, quote=True)}">
  <meta name="theme-color" content="#06070a">
  <link rel="canonical" href="{canonical}">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="assets/site.css">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{BRAND}">
  <meta property="og:title" content="{html.escape(title, quote=True)}">
  <meta property="og:description" content="{html.escape(description, quote=True)}">
  <meta property="og:url" content="{canonical}">
  <script type="application/ld+json">{json.dumps(schema, separators=(',', ':'))}</script>
</head>
<body>
{nav()}
<main id="main">{body}</main>
{footer()}
<script src="assets/site.js" defer></script>
</body>
</html>
"""
    (ROOT / filename).write_text(document, encoding="utf-8", newline="\n")


def product_card(product: dict, featured: bool = False) -> str:
    visual = ""
    if product["image"]:
        visual = f'<div class="product-visual"><img src="{product["image"]}" alt="{html.escape(product["alt"], quote=True)}" loading="lazy"></div>'
    else:
        sizes = "".join(f'<span class="tech-tag">{item}</span>' for item in product["pills"])
        visual = f'<div class="product-visual"><div class="model-card card"><div class="card-content"><span class="kicker">Roadmap</span><div class="tag-cloud">{sizes}</div></div></div></div>'
    pills = "".join(f'<span class="pill">{item}</span>' for item in product["pills"])
    featured_class = " featured" if featured else ""
    inner = f"""
      <div>
        <div class="product-topline"><span class="kicker">{product['label']}</span><span class="status {product['status_class']}">{product['status']}</span></div>
        <h3>{product['name']}</h3><p class="tagline">{product['summary']}</p>
        <div class="product-meta">{pills}</div>
        <a class="text-link" href="{product['slug']}.html">Explore {product['name']} <span class="arrow">→</span></a>
      </div>{visual}"""
    return f'<article class="card product-card{featured_class}" data-reveal data-tilt><div class="card-content">{inner}</div></article>'


def feature_card(label: str, title: str, text: str, extra: str = "") -> str:
    return f'<article class="card feature-card" data-reveal><div class="card-content"><div class="label">{label}</div><h3>{title}</h3><p>{text}</p>{extra}</div></article>'


def tags(items: list[str]) -> str:
    return '<div class="tag-cloud">' + "".join(f'<span class="tech-tag">{item}</span>' for item in items) + "</div>"


home_products = "".join(product_card(item, index == 0) for index, item in enumerate(PRODUCTS))

home = f"""
<section class="hero">
  <div class="container">
    <div class="hero-grid">
      <div class="hero-copy" data-reveal>
        <span class="eyebrow">AI engineering company</span>
        <h1>Build with AI.<br><span class="gradient">Ship what works.</span></h1>
        <p>KhanaI Technologies engineers production-grade AI systems including WinPilot AI, WinHeart AI, ClipVault AI, the upcoming WinQor model family, TradingX, voice automation, company AI, chatbots, and database intelligence.</p>
        <div class="hero-actions"><a class="button button-primary" data-magnetic href="products.html">Explore our products <span class="arrow">→</span></a><a class="button" data-magnetic href="{WINPILOT_STORE}" target="_blank" rel="noopener noreferrer">WinPilot on Microsoft Store ↗</a></div>
        <div class="hero-note">Windows-native products · Local-first options · Built from Hyderabad for teams worldwide</div>
      </div>
      <div class="hero-stage" data-reveal>
        <div class="stage-glow"></div>
        <div class="device-frame"><div class="device-bar"><i></i><i></i><i></i></div><img src="{WINPILOT_SCREEN_1}" alt="WinPilot AI desktop workspace"></div>
        <div class="float-card float-card-a"><img src="winheart-dashboard.png" alt="WinHeart AI dashboard"></div>
        <div class="float-card float-card-b"><img src="clipvault-home.png" alt="ClipVault AI home workspace"></div>
      </div>
    </div>
    <div class="proof-strip" data-reveal><div class="proof-item"><strong>5</strong><span>Product lines</span></div><div class="proof-item"><strong>3</strong><span>Windows applications</span></div><div class="proof-item"><strong>4+</strong><span>AI service areas</span></div><div class="proof-item"><strong>Worldwide</strong><span>Remote-first delivery</span></div></div>
  </div>
</section>

<section class="section section-line">
  <div class="container">
    <header class="section-head split" data-reveal><div><span class="kicker">Our products</span><h2>Real software.<br>Clear purpose.</h2></div><p>Five focused product lines spanning Windows productivity, PC health, private clip management, compact AI models, and market intelligence.</p></header>
    <div class="product-grid">{home_products}</div>
  </div>
</section>

<section class="section section-line">
  <div class="container">
    <header class="section-head" data-reveal><span class="kicker">Architecture</span><h2>Built around control,<br>privacy, and deployment.</h2><p>Every system is designed for practical use, with local execution and cloud connectivity selected according to the workflow.</p></header>
    <div class="bento-grid">
      <article class="card bento-card wide tall" data-reveal data-tilt><div class="card-content"><div class="icon-box">01</div><h3>Secure by default</h3><p>AES encryption, HTTPS communication, and deliberate handling of sensitive information across supported workflows.</p></div></article>
      <article class="card bento-card tall" data-reveal data-tilt><div class="card-content"><div class="icon-box">02</div><h3>Local-first</h3><p>Systems can run on your hardware by default. Cloud functionality remains purposeful and explicit.</p></div></article>
      <article class="card bento-card" data-reveal><div class="card-content"><div class="icon-box">03</div><h3>Multi-model</h3><p>GPT, Gemini, Claude, or local models selected per use case.</p></div></article>
      <article class="card bento-card" data-reveal><div class="card-content"><div class="icon-box">04</div><h3>Production focused</h3><p>Products and systems are built for real workflows, not static demonstrations.</p></div></article>
      <article class="card bento-card" data-reveal><div class="card-content"><div class="icon-box">05</div><h3>Cloud optional</h3><p>Cloud sync and connected services are used only where the product supports them.</p></div></article>
      <article class="card bento-card" data-reveal><div class="card-content"><div class="icon-box">06</div><h3>Remote-first</h3><p>Deployed and supported for customers worldwide.</p></div></article>
    </div>
  </div>
</section>

<section class="section section-line">
  <div class="container">
    <header class="section-head split" data-reveal><div><span class="kicker">Solutions</span><h2>Custom AI for real operations.</h2></div><p>We design focused systems for business knowledge, customer conversations, voice workflows, and data access.</p></header>
    <div class="bento-grid">
      <article class="card bento-card" data-reveal><div class="card-content"><div class="icon-box">VA</div><h3>AI Voice Assistants</h3><p>Custom voice-driven systems for hands-free business automation.</p><a class="text-link" href="solutions.html#voice">Explore <span class="arrow">→</span></a></div></article>
      <article class="card bento-card" data-reveal><div class="card-content"><div class="icon-box">CA</div><h3>Company AI</h3><p>Private AI trained on company documents, policies, manuals, and knowledge.</p><a class="text-link" href="solutions.html#company-ai">Explore <span class="arrow">→</span></a></div></article>
      <article class="card bento-card" data-reveal><div class="card-content"><div class="icon-box">CB</div><h3>Automation Chatbots</h3><p>WhatsApp and web automation for leads, bookings, and support.</p><a class="text-link" href="solutions.html#chatbots">Explore <span class="arrow">→</span></a></div></article>
      <article class="card bento-card" data-reveal><div class="card-content"><div class="icon-box">DB</div><h3>AI Database Managers</h3><p>Ask an existing database questions in plain English and receive structured results.</p><a class="text-link" href="solutions.html#database">Explore <span class="arrow">→</span></a></div></article>
    </div>
  </div>
</section>

<section class="section section-line">
  <div class="container">
    <header class="section-head" data-reveal><span class="kicker">Technology</span><h2>A practical stack for<br>models, data, and delivery.</h2></header>
    <div data-reveal>{tags(['Python','GPT-4 (OpenAI)','Gemini (Google)','Claude (Anthropic)','LangChain','Whisper STT','Supabase','FastAPI','Docker','TensorFlow','Scikit-Learn','PostgreSQL','Pinecone','RAG Pipelines','Pandas / NumPy','LSTM','PyAutoGUI','Vosk (Offline STT)'])}</div>
  </div>
</section>

<section class="section section-line">
  <div class="container"><div class="cta-panel" data-reveal><span class="eyebrow">Start a conversation</span><h2>Have a product idea or operational problem?</h2><p>Talk directly with the engineering team about WinPilot AI, WinHeart AI, ClipVault AI, WinQor, TradingX, or a custom AI system.</p><div class="cta-actions"><a class="button button-primary" data-magnetic href="contact.html">Let's build something <span class="arrow">→</span></a><a class="button" href="https://wa.me/916303716492" target="_blank" rel="noopener noreferrer">WhatsApp ↗</a></div></div></div>
</section>
"""


products_page = f"""
<section class="page-hero"><div class="container" data-reveal><span class="eyebrow">Product portfolio</span><h1 class="page-title">Five product lines.<br><span class="gradient-text">One engineering studio.</span></h1><p class="page-lead">Explore the Windows applications, compact model roadmap, and market-intelligence work developed by KhanaI Technologies.</p></div></section>
<section class="section section-line"><div class="container"><div class="product-grid">{home_products}</div></div></section>
<section class="section section-line"><div class="container"><div class="cta-panel" data-reveal><span class="eyebrow">Need help choosing?</span><h2>Find the right product or solution.</h2><p>Tell us what you are trying to improve, automate, diagnose, or organise.</p><div class="cta-actions"><a class="button button-primary" href="contact.html">Talk to the team <span class="arrow">→</span></a></div></div></div></section>
"""


winpilot = f"""
<section class="page-hero"><div class="container" data-reveal><span class="eyebrow">Desktop AI · Flagship product</span><h1 class="page-title">WinPilot AI</h1><p class="page-lead">A unified Windows AI workspace that brings chat, documents, image understanding, authentication, voice, and productivity into one secure desktop experience.</p><div class="page-actions"><a class="button button-primary" data-magnetic href="{WINPILOT_STORE}" target="_blank" rel="noopener noreferrer">Open Microsoft Store ↗</a><a class="button" href="#showcase">See it in action ↓</a></div></div></section>
<section class="section-tight"><div class="container"><div class="media-frame large" data-reveal><img src="{WINPILOT_SCREEN_1}" alt="WinPilot AI desktop workspace"></div></div></section>
<section class="section"><div class="container"><div class="summary-block" data-reveal>Bring everyday AI work into one Windows-native workspace. Chat, analyse PDFs, understand images, manage conversations, organise documents, and choose the model that suits the task.<strong>One desktop for focused AI work.</strong></div></div></section>
<section class="section section-line"><div class="container"><header class="section-head" data-reveal><span class="kicker">Capabilities</span><h2>Designed around real desktop workflows.</h2></header><div class="feature-list">
{feature_card('Workspace','One desktop for AI work','Chat, analyse PDFs, understand images, manage conversations, and organise documents without switching between separate tools.')}
{feature_card('Architecture','Built for Windows','Python and CustomTkinter frontend with FastAPI services, secure API integrations, SQLite/Supabase data, and a multi-AI-ready design.')}
{feature_card('Capabilities','Productivity features','AI chat workspace, conversation history, PDF analysis, image understanding, profile controls, settings, cloud synchronization, and Windows-native packaging.')}
{feature_card('Release','Official showcase','The public release includes the official trailer, screenshots, documentation, and Microsoft Store listing.','<span class="status">Release showcase available</span>')}
</div></div></section>
<section class="section section-line" id="showcase"><div class="container"><header class="section-head" data-reveal><span class="kicker">Official trailer</span><h2>See WinPilot AI in action.</h2></header><div class="media-frame large" data-reveal><video controls preload="metadata" poster="{WINPILOT_SCREEN_2}"><source src="{WINPILOT_VIDEO}" type="video/mp4">Your browser does not support the video element.</video></div></div></section>
<section class="section section-line"><div class="container"><header class="section-head" data-reveal><span class="kicker">Real interface</span><h2>The workspace, exactly as shipped.</h2></header><div class="media-grid"><div class="media-frame" data-reveal><img src="{WINPILOT_SCREEN_1}" alt="WinPilot AI workspace" loading="lazy"><div class="media-caption">AI workspace</div></div><div class="media-frame" data-reveal><img src="{WINPILOT_SCREEN_2}" alt="WinPilot AI interface" loading="lazy"><div class="media-caption">Product interface</div></div></div></div></section>
<section class="section section-line"><div class="container"><header class="section-head" data-reveal><span class="kicker">Settings preview</span><h2>Controls stay visible.</h2><p>Display preview of WinPilot AI configuration. Toggles below are visual only.</p></header>
<div class="settings-shell" data-reveal><aside class="settings-side"><strong>Settings</strong><span>AI Model</span><span>Voice</span><span>Automation</span><span>Privacy</span><span>Appearance</span></aside><div class="settings-panel">
<div class="setting-group"><h3>AI Model</h3><div class="setting-row"><div><strong>Active model</strong><small>Used for command processing</small></div><select class="select-demo" aria-label="Active model"><option>GPT-4 (OpenAI)</option><option>Gemini (Google)</option><option>Claude (Anthropic)</option><option>Local Model (Offline)</option></select></div><div class="setting-row"><div><strong>Fallback model</strong><small>Used if the primary is unavailable</small></div><select class="select-demo" aria-label="Fallback model"><option>Claude</option><option>GPT-4</option><option>Gemini</option><option>Local Model</option></select></div><div class="setting-row"><div><strong>Response length</strong><small>Verbosity of AI responses</small></div><select class="select-demo" aria-label="Response length"><option>Concise</option><option selected>Balanced</option><option>Detailed</option></select></div></div>
<div class="setting-group"><h3>Voice</h3><div class="setting-row"><div><strong>Voice mode</strong><small>Hands-free voice input</small></div><button class="toggle-demo" type="button" role="switch" aria-checked="false" aria-label="Voice mode"></button></div><div class="setting-row"><div><strong>Wake word detection</strong><small>Always-on wake word listening</small></div><button class="toggle-demo" type="button" role="switch" aria-checked="false" aria-label="Wake word detection"></button></div><div class="setting-row"><div><strong>Text-to-speech</strong><small>WinPilot AI speaks responses aloud</small></div><button class="toggle-demo on" type="button" role="switch" aria-checked="true" aria-label="Text-to-speech"></button></div><div class="setting-row"><div><strong>Language</strong><small>Speech recognition language</small></div><select class="select-demo" aria-label="Language"><option>English (US)</option><option>English (UK)</option><option>Arabic</option><option>Urdu</option><option>Hindi</option></select></div></div>
<div class="setting-group"><h3>Automation</h3><div class="setting-row"><div><strong>File system access</strong><small>Create, move, and delete files</small></div><button class="toggle-demo on" type="button" role="switch" aria-checked="true" aria-label="File system access"></button></div><div class="setting-row"><div><strong>Application control</strong><small>Open and close applications</small></div><button class="toggle-demo on" type="button" role="switch" aria-checked="true" aria-label="Application control"></button></div><div class="setting-row"><div><strong>System settings control</strong><small>Volume, display, and network</small></div><button class="toggle-demo" type="button" role="switch" aria-checked="false" aria-label="System settings control"></button></div><div class="setting-row"><div><strong>Workflow automation</strong><small>Multi-step automated sequences</small></div><button class="toggle-demo on" type="button" role="switch" aria-checked="true" aria-label="Workflow automation"></button></div><div class="setting-row"><div><strong>Confirm before executing</strong><small>Ask before destructive actions</small></div><button class="toggle-demo on" type="button" role="switch" aria-checked="true" aria-label="Confirm before executing"></button></div></div>
<div class="setting-group"><h3>Privacy</h3><div class="setting-row"><div><strong>Offline mode</strong><small>Use only local models</small></div><button class="toggle-demo" type="button" role="switch" aria-checked="false" aria-label="Offline mode"></button></div><div class="setting-row"><div><strong>Local model only</strong><small>Disable cloud API calls</small></div><button class="toggle-demo" type="button" role="switch" aria-checked="false" aria-label="Local model only"></button></div><div class="setting-row"><div><strong>Command history</strong><small>Store history locally</small></div><button class="toggle-demo on" type="button" role="switch" aria-checked="true" aria-label="Command history"></button></div><div class="setting-row"><div><strong>Telemetry</strong><small>Anonymous usage data</small></div><button class="toggle-demo" type="button" role="switch" aria-checked="false" aria-label="Telemetry"></button></div></div>
<div class="setting-group"><h3>Appearance</h3><div class="setting-row"><div><strong>Theme</strong><small>Light or dark app interface</small></div><select class="select-demo" aria-label="Theme"><option>Light</option><option selected>Dark</option></select></div><div class="setting-row"><div><strong>Animations</strong><small>Enable UI motion</small></div><button class="toggle-demo on" type="button" role="switch" aria-checked="true" aria-label="Animations"></button></div></div>
</div></div></div></section>
<section class="section section-line"><div class="container"><div class="cta-panel" data-reveal><span class="eyebrow">WinPilot AI</span><h2>One Windows workspace for AI work.</h2><div class="cta-actions"><a class="button button-primary" href="{WINPILOT_STORE}" target="_blank" rel="noopener noreferrer">Open Microsoft Store ↗</a><a class="button" href="contact.html">Ask about WinPilot AI</a></div></div></div></section>
"""


winheart = f"""
<section class="page-hero"><div class="container" data-reveal><span class="eyebrow">Windows assistant · Early launch</span><h1 class="page-title">WinHeart AI</h1><p class="page-lead">Diagnose. Fix. Protect. Bring PC health, guided repair, change tracking, productivity tools, and visible privacy controls into one local-first Windows assistant.</p><div class="page-actions"><a class="button button-primary" data-magnetic href="{WINHEART_STORE}" target="_blank" rel="noopener noreferrer">Open Microsoft Store ↗</a><a class="button" href="WinHeartAI-Setup-1.0.0.exe" download>Direct download ↓</a></div><div class="page-badge"><span class="status">Free for a limited time</span></div></div></section>
<section class="section-tight"><div class="container"><div class="media-frame large" data-reveal><img src="winheart-dashboard.png" alt="WinHeart AI dashboard with system overview"></div></div></section>
<section class="section"><div class="container"><div class="summary-block" data-reveal>WinHeart AI helps you understand what is happening on your PC before you act. Review live system information, run focused checks, compare changes, follow supported repair guidance, keep quick notes, and export diagnosis reports. Online assistance is optional, while local data and privacy controls remain visible.<strong>One place to diagnose issues, review evidence, and make informed fixes.</strong></div></div></section>
<section class="section section-line"><div class="container"><header class="section-head" data-reveal><span class="kicker">Inside WinHeart</span><h2>From a symptom to useful evidence.</h2></header><div class="feature-list">
{feature_card('Diagnosis','Understand your PC','AI Diagnose and System Health bring CPU, RAM, disk, temperature, startup, and network checks into one focused workspace.')}
{feature_card('Repair','Work through supported fixes','PC Repair organises network, Bluetooth, audio, performance, storage, startup, Windows services, and update diagnostics.')}
{feature_card('Control','Keep local data in your hands','Privacy settings cover online assistance, weather access, account visibility, purchase links, and local data export or deletion controls.')}
{feature_card('Daily workspace','Useful tools stay close','Quick Actions, Quick Notes, voice assistance, system overview, and common checks help you move from a question to the right diagnostic.')}
{feature_card('Evidence and history','See what changed','Compare system snapshots, review repair history, and export reports to understand the evidence behind a diagnosis.')}
{feature_card('Availability','Early launch','WinHeart AI is available to download free for a limited time during its early launch.','<span class="status">Free for a limited time · Windows</span>')}
</div></div></section>
<section class="section section-line"><div class="container"><header class="section-head" data-reveal><span class="kicker">Real product screenshots</span><h2>The actual Windows interface.</h2></header><div class="media-grid three"><div class="media-frame" data-reveal><img src="winheart-dashboard.png" alt="WinHeart AI dashboard" loading="lazy"><div class="media-caption">Dashboard and quick actions</div></div><div class="media-frame" data-reveal><img src="winheart-repair.png" alt="WinHeart AI PC Repair screen" loading="lazy"><div class="media-caption">PC Repair diagnostics</div></div><div class="media-frame" data-reveal><img src="winheart-settings.png" alt="WinHeart AI privacy settings screen" loading="lazy"><div class="media-caption">Privacy and local data controls</div></div></div></div></section>
<section class="section section-line"><div class="container"><header class="section-head" data-reveal><span class="kicker">Plans</span><h2>Choose the level that fits.</h2></header><div class="pricing-grid"><article class="card price-card" data-reveal><h3>Free</h3><div class="price">$0 <span>USD</span></div></article><article class="card price-card" data-reveal><h3>Basic</h3><div class="price">$5 <span>USD</span></div></article><article class="card price-card" data-reveal><h3>Pro</h3><div class="price">$9 <span>USD</span></div></article><article class="card price-card" data-reveal><h3>Pro Max</h3><div class="price">$16 <span>USD</span></div></article></div><div class="legal-bar" style="margin-top:1rem" data-reveal><span>Before purchase</span><a href="winheart-privacy.html">Privacy Policy</a><a href="winheart-terms.html">Terms &amp; Conditions</a><a href="winheart-refund.html">Refund Policy</a></div></div></section>
<section class="section section-line"><div class="container"><div class="cta-panel" data-reveal><span class="eyebrow">Limited-time launch offer</span><h2>Download WinHeart AI for Windows.</h2><p>Get WinHeart AI 1.0.0 at no cost during the early launch.</p><div class="cta-actions"><a class="button button-primary" href="{WINHEART_STORE}" target="_blank" rel="noopener noreferrer">Microsoft Store ↗</a><a class="button" href="WinHeartAI-Setup-1.0.0.exe" download>Direct download ↓</a></div></div></div></section>
"""


clipvault = f"""
<section class="page-hero"><div class="container" data-reveal><img src="clipvault-logo.png" alt="ClipVault AI logo" style="width:84px;border-radius:20px;margin-bottom:1.3rem"><span class="eyebrow">Windows workspace · Live now</span><h1 class="page-title">ClipVault AI</h1><p class="page-lead">Capture, search, organise, understand, and protect clipboard history, screenshots, text, links, and files in one intelligent local Windows workspace.</p><div class="page-actions"><a class="button button-primary" data-magnetic href="{CLIPVAULT_STORE}" target="_blank" rel="noopener noreferrer">Download on Microsoft Store ↗</a></div><div class="page-badge"><span class="status">Free for a limited time</span></div></div></section>
<section class="section-tight"><div class="container"><div class="media-frame large" data-reveal><img src="clipvault-home.png" alt="ClipVault AI home workspace with quick capture and recent clips"></div></div></section>
<section class="section"><div class="container"><div class="summary-block" data-reveal>Every day, we copy, capture, and save information. Finding it again should not be difficult. ClipVault AI turns scattered clipboard items and saved content into a structured workspace you can search and manage. Capture effortlessly, extract text, summarize content, find related clips, detect duplicates, and review cleanup suggestions.<strong>ClipVault AI. Capture More. Search Smarter. Stay Organized.</strong></div></div></section>
<section class="section section-line"><div class="container"><header class="section-head" data-reveal><span class="kicker">Capabilities</span><h2>Your information, organised around retrieval.</h2></header><div class="feature-list">
{feature_card('Quick capture','Save what matters fast','Capture screenshots, text, and links with keyboard shortcuts, add files, or send content into Smart Organize.')}
{feature_card('Clipboard','One searchable library','Keep automatic history for text, links, images, and files with search, copy, paste, pinning, saved clips, multiple selection, and a quick queue.')}
{feature_card('Local AI tools','Understand and find clips faster','Use local summaries, similar clip matching, relevant passages, topic suggestions, library insights, and screenshot text recognition.')}
{feature_card('Screenshots','Organise old and new captures','Import older screenshots, scan folders, browse previews, filter by date, app, or tags, and use local text recognition with auto and batch tags.')}
{feature_card('Smart cleanup','Review clutter before removing it','Find exact duplicates, similar images, blank captures, and older unused images with path previews, estimates, selection, and confirmation controls.')}
{feature_card('Privacy and backup','Local controls for your workspace','Use local encrypted content, an app PIN, sensitive-content protection, expiry, ignored-app controls, backups, restore, export, import, retention, and separate workspaces.')}
</div></div></section>
<section class="section section-line"><div class="container"><header class="section-head" data-reveal><span class="kicker">Real product screenshots</span><h2>A private workspace built for everyday capture.</h2></header><div class="media-grid three"><div class="media-frame" data-reveal><img src="clipvault-home.png" alt="ClipVault AI home and recent clips" loading="lazy"><div class="media-caption">Home, quick capture, and recent clips</div></div><div class="media-frame" data-reveal><img src="clipvault-library.png" alt="ClipVault AI links library and clip details" loading="lazy"><div class="media-caption">Searchable clip library</div></div><div class="media-frame" data-reveal><img src="clipvault-features.png" alt="ClipVault AI features for local AI, cleanup, privacy, and backup" loading="lazy"><div class="media-caption">Feature controls</div></div></div></div></section>
<section class="section"><div class="container"><div class="summary-block" data-reveal>The home workspace keeps quick capture, recent clips, folders, details, and smart tools visible together. The library groups screenshots, text, links, and files with search, filters, tags, saved items, and pinning. Feature controls cover local AI, cleanup review, private storage, expiry, scheduled backups, restore, import, export, and separate workspaces.<strong>Your everyday information stays organised, searchable, and under your control.</strong></div></div></section>
<section class="section section-line"><div class="container"><div class="cta-panel" data-reveal><span class="eyebrow">Available now</span><h2>Build a private, searchable library.</h2><div class="cta-actions"><a class="button button-primary" href="{CLIPVAULT_STORE}" target="_blank" rel="noopener noreferrer">Download ClipVault AI free ↗</a></div></div></div></section>
"""


winqor = """
<section class="page-hero"><div class="container" data-reveal><span class="eyebrow">AI model family · Releasing soon</span><h1 class="page-title">WinQor</h1><p class="page-lead">An upcoming family of compact AI models planned in 150 million, 300 million, and 1 billion parameter editions, creating practical choices across different compute budgets and product needs.</p><div class="page-badge"><span class="status soon">Releasing soon</span></div></div></section>
<section class="section"><div class="container"><div class="summary-block" data-reveal>The WinQor roadmap is built around choice. Smaller planned editions target efficient, low-footprint use, while the larger edition is intended for workloads that benefit from additional capacity. Final capabilities, formats, hardware requirements, benchmarks, and release dates will be published closer to availability.<strong>Three planned sizes. One model family. Practical deployment choices.</strong></div></div></section>
<section class="section section-line"><div class="container"><header class="section-head" data-reveal><span class="kicker">Model roadmap</span><h2>Three announced editions.</h2></header><div class="model-grid"><article class="card model-card" data-reveal data-tilt><div class="card-content"><span class="kicker">Compact planned edition</span><div class="model-size">150M</div><p>Intended for lightweight local, edge, and embedded AI scenarios where resource efficiency matters.</p><span class="status soon">Planned</span></div></article><article class="card model-card" data-reveal data-tilt><div class="card-content"><span class="kicker">Balanced planned edition</span><div class="model-size">300M</div><p>Intended to balance footprint and capability for assistants, integrated features, and workflow automation.</p><span class="status soon">Planned</span></div></article><article class="card model-card" data-reveal data-tilt><div class="card-content"><span class="kicker">Largest announced edition</span><div class="model-size">1B</div><p>Intended for richer workloads that can use additional model capacity and context.</p><span class="status soon">Planned</span></div></article></div></div></section>
<section class="section section-line"><div class="container"><div class="cta-panel" data-reveal><span class="eyebrow">Development roadmap</span><h2>More details are coming.</h2><p>Official capabilities, evaluations, deployment formats, system requirements, availability, and release dates will be shared as the launch approaches.</p><div class="cta-actions"><a class="button button-primary" href="contact.html">Ask about WinQor <span class="arrow">→</span></a></div></div></div></section>
"""


tradingx = """
<section class="page-hero"><div class="container" data-reveal><span class="eyebrow">AI trading intelligence</span><h1 class="page-title">TradingX</h1><p class="page-lead">An AI agent that ingests real-time market data and generates directional predictions for currencies, gold, and Bitcoin using machine-learning models and automated data pipelines.</p></div></section>
<section class="section section-line"><div class="container"><header class="section-head" data-reveal><span class="kicker">Decision support</span><h2>Market data into directional signals.</h2><p>TradingX is an informational decision-support tool. It is not financial advice.</p></header><div class="feature-list">
""" + feature_card('Core function','What TradingX does','Continuously ingests live market data, processes it through trained ML models, and outputs directional predictions such as up, down, or hold.','<span class="status soon">Real-time data pipeline</span>') + feature_card('Coverage','Supported assets','Major forex pairs including USD, EUR, GBP, and JPY; gold (XAU/USD); Bitcoin (BTC/USD); and expansion through additional data-source integration.') + feature_card('Performance','Approximately 75% accuracy','Approximately 75% directional accuracy under standard market conditions. This refers to directional correctness, not price-level precision. Results vary by volatility.') + feature_card('Architecture','How it works','Connects to OHLCV market data APIs, preprocesses and normalizes data, runs trained classifiers, and returns a signal with a confidence score.') + feature_card('Technology','Built with','Python, Scikit-Learn, TensorFlow, Pandas, NumPy, LSTM, Random Forest, and Docker.') + feature_card('Important','Risk disclaimer','TradingX does not constitute financial advice. All trading involves risk. Past accuracy does not guarantee future results. For informational purposes only.','<span class="status soon">Cloud / API deployment</span>') + """
</div></div></section>
<section class="section section-line"><div class="container"><div class="cta-panel" data-reveal><span class="eyebrow">TradingX</span><h2>Discuss market-intelligence workflows.</h2><div class="cta-actions"><a class="button button-primary" href="contact.html">Inquire about TradingX <span class="arrow">→</span></a></div></div></div></section>
"""


solutions = """
<section class="page-hero"><div class="container" data-reveal><span class="eyebrow">Business AI systems</span><h1 class="page-title">Solutions built around<br><span class="gradient-text">real operations.</span></h1><p class="page-lead">Four focused service areas for teams that need voice automation, private knowledge, conversational workflows, or natural-language access to business data.</p></div></section>
<section class="section section-line"><div class="container">
<article class="service-section" id="voice"><div data-reveal><span class="kicker">01 · Service</span><h2>AI Voice Assistants</h2><p>Custom voice-driven AI that takes verbal commands, automates workflows, and runs operations hands-free.</p></div><div class="service-copy">""" + feature_card('Overview','What it does','A custom voice assistant tuned to a business listens for commands, understands context, and executes tasks from scheduling to CRM updates and team notifications.') + feature_card('Use cases','Applications','Reception booking, hands-free warehouse inventory logging, field reporting, and executive scheduling workflows.') + feature_card('Technical','How it works','Wake-word detection, real-time speech-to-text, an NLP intent layer, an API action layer, and text-to-speech confirmation.') + feature_card('Technology','Stack','Python, Whisper or Vosk, LangChain, OpenAI or Claude, REST APIs, and pyttsx3.','<span class="status soon">Local or cloud deployment</span>') + """</div></article>
<article class="service-section" id="company-ai"><div data-reveal><span class="kicker">02 · Service</span><h2>Company AI</h2><p>A private assistant built around company documents, policies, manuals, and knowledge.</p></div><div class="service-copy">""" + feature_card('Overview','What it does','A private AI layer over company documents and operational data, designed to answer questions using the organisation’s own knowledge.') + feature_card('Use cases','Applications','Internal helpdesk, customer support, HR onboarding, and sales enablement across product and policy information.') + feature_card('Technical','How it works','Ingest PDF, Word, Notion, or Confluence content; build a vector index; deploy a RAG pipeline; connect web, Slack, Teams, or WhatsApp; and update on schedule.') + feature_card('Technology','Stack','LangChain, Pinecone, embeddings, RAG, FastAPI, and Docker.','<span class="status soon">Private / on-premise deployment</span>') + """</div></article>
<article class="service-section" id="chatbots"><div data-reveal><span class="kicker">03 · Service</span><h2>Automation Chatbots</h2><p>Smart bots for WhatsApp, websites, or apps that capture leads, book appointments, and answer common queries.</p></div><div class="service-copy">""" + feature_card('Overview','What it does','Conversational AI that engages customers, answers questions, qualifies needs, and guides people to the next action.') + feature_card('Use cases','Applications','Appointment booking, e-commerce status and returns, lead qualification, intake, and agency onboarding questionnaires.') + feature_card('Technical','How it works','Connect WhatsApp Business API or a web widget, interpret intent, route flows, integrate calendars or CRMs, and provide optional human handoff.') + feature_card('Technology','Stack','Python, WhatsApp API, LangChain, OpenAI or Claude, FastAPI, and MySQL.','<span class="status soon">Cloud deployment</span>') + """</div></article>
<article class="service-section" id="database"><div data-reveal><span class="kicker">04 · Service</span><h2>AI Database Managers</h2><p>Ask an existing database questions in plain English and receive SQL-backed answers, reports, and data views.</p></div><div class="service-copy">""" + feature_card('Overview','What it does','A natural-language interface over an existing database. AI translates intent into validated SQL and returns clean, formatted results.') + feature_card('Example queries','Use cases','“Show items below reorder level this week”, “Which reps closed the most deals?”, “Generate a monthly P&L summary”, or “Average delivery time by region”.') + feature_card('Technical','How it works','Connect MySQL, PostgreSQL, SQLite, or MSSQL; map schema to model context; validate generated SQL; return tables, charts, or natural language; and schedule reports.') + feature_card('Technology','Stack','Python, LangChain SQL, SQLAlchemy, Pandas, Plotly, and FastAPI.','<span class="status soon">Local or cloud deployment</span>') + """</div></article>
</div></section>
<section class="section section-line"><div class="container"><header class="section-head" data-reveal><span class="kicker">Technology</span><h2>Tools selected for the workflow.</h2><p>Models, orchestration, databases, and deployment choices are matched to the product or business requirement.</p></header><div class="bento-grid"><article class="card bento-card" data-reveal><div class="card-content"><h3>Language models</h3>""" + tags(['GPT-4 (OpenAI)','Gemini (Google)','Claude (Anthropic)','Ollama / Local LLMs','Whisper STT','Vosk (Offline)']) + """</div></article><article class="card bento-card" data-reveal><div class="card-content"><h3>AI pipelines</h3>""" + tags(['LangChain','RAG Pipelines','Pinecone','Chroma DB','Embeddings','LangGraph']) + """</div></article><article class="card bento-card" data-reveal><div class="card-content"><h3>Core engineering</h3>""" + tags(['Python','FastAPI','Flask','PyAutoGUI','SQLAlchemy','pyttsx3']) + """</div></article><article class="card bento-card" data-reveal><div class="card-content"><h3>Machine learning</h3>""" + tags(['TensorFlow / Keras','Scikit-Learn','Pandas','NumPy','LSTM','Random Forest']) + """</div></article><article class="card bento-card" data-reveal><div class="card-content"><h3>Data and deployment</h3>""" + tags(['Supabase','PostgreSQL','MySQL','SQLite','Docker','REST APIs']) + """</div></article><article class="card bento-card" data-reveal><div class="card-content"><h3>Privacy and security</h3>""" + tags(['AES Encryption','HTTPS / TLS','Local-First','Offline LLM','Razorpay']) + """</div></article></div></div></section>
<section class="section section-line"><div class="container"><div class="cta-panel" data-reveal><span class="eyebrow">Custom AI</span><h2>Start with the operational problem.</h2><p>We can map the right workflow, model, interface, integrations, and deployment approach.</p><div class="cta-actions"><a class="button button-primary" href="contact.html">Request a solution <span class="arrow">→</span></a></div></div></div></section>
"""


company = """
<section class="page-hero"><div class="container" data-reveal><span class="eyebrow">Company</span><h1 class="page-title">AI that ships.<br><span class="gradient-text">Not demos.</span></h1><p class="page-lead">KhanaI Technologies is an AI engineering company building production-focused systems—from desktop assistants and private workspaces to market intelligence and business automation.</p></div></section>
<section class="section section-line"><div class="container"><header class="section-head split" data-reveal><div><span class="kicker">About KhanaI Technologies</span><h2>Built directly by the engineering team.</h2></div><p>We design, build, and deploy intelligent systems for teams worldwide, with a focus on practical workflows, clear controls, and usable products.</p></header><div class="feature-list">""" + feature_card('Mission','What drives us','Make capable AI systems accessible to businesses without agency layers or long delivery cycles. Build working products and ship with focus.') + feature_card('Approach','How we work','Models, APIs, interfaces, automation, and deployment are treated as one system and tested together before delivery.') + feature_card('Values','Privacy first','Default to local execution and minimal data collection where the product supports it. Keep user controls visible and understandable.') + feature_card('Company info','Details','Company: KhanaI Technologies. Studio: khan.ai.technologies. Location: Worldwide · Remote-first. Email: winpilotai@gmail.com.','<a class="text-link" href="https://khanaitechnologies.netlify.app/" target="_blank" rel="noopener noreferrer">Previous web presence ↗</a>') + """</div></div></section>
<section class="section section-line"><div class="container"><article class="card founder-card" data-reveal><div class="founder-avatar" aria-hidden="true">SK</div><div><span class="kicker">Founder</span><h2>Shamsheer Khan Khurrum</h2><p><strong>Lead Engineer · KhanaI Technologies</strong></p><p>Founder and lead engineer building production AI systems from the ground up. Every product is designed, engineered, and deployed with a commitment to real-world performance and privacy.</p><p>Creator of WinPilot AI, the multi-model Windows assistant, and TradingX, an AI trading intelligence system covering forex, gold, and Bitcoin.</p>""" + tags(['AI / ML Engineering','NLP & LLMs','Systems Automation','Python','Voice AI','ML Pipelines','Product Builder','Windows Automation']) + """</div></article></div></section>
<section class="section section-line"><div class="container"><header class="section-head" data-reveal><span class="kicker">Why KhanaI Technologies</span><h2>Built for serious product work.</h2></header><div class="bento-grid"><article class="card bento-card" data-reveal><div class="card-content"><div class="icon-box">01</div><h3>Ships working products</h3><p>WinPilot AI and ClipVault AI are live, WinHeart AI is in early launch, and WinQor is on the roadmap.</p></div></article><article class="card bento-card" data-reveal><div class="card-content"><div class="icon-box">02</div><h3>Privacy by design</h3><p>Local-first execution and explicit online features keep data boundaries understandable.</p></div></article><article class="card bento-card" data-reveal><div class="card-content"><div class="icon-box">03</div><h3>Direct engineering</h3><p>Work directly with the engineering team—without agency layers or outsourced handoffs.</p></div></article><article class="card bento-card" data-reveal><div class="card-content"><div class="icon-box">04</div><h3>Model flexibility</h3><p>Cloud and local models can be selected according to the use case.</p></div></article><article class="card bento-card" data-reveal><div class="card-content"><div class="icon-box">05</div><h3>Real-world testing</h3><p>Workflows are tested as complete systems, not only as isolated model benchmarks.</p></div></article><article class="card bento-card" data-reveal><div class="card-content"><div class="icon-box">06</div><h3>Full-stack delivery</h3><p>Models, APIs, interfaces, integrations, and deployment from one team.</p></div></article></div></div></section>
<section class="section section-line" id="technology"><div class="container"><header class="section-head" data-reveal><span class="kicker">Technology</span><h2>From model orchestration to Windows automation.</h2></header>""" + tags(['Python','GPT-4','Gemini','Claude','LangChain','RAG','Whisper','Vosk','FastAPI','Supabase','PostgreSQL','MySQL','SQLite','Docker','TensorFlow','Scikit-Learn','Pandas','NumPy','LSTM','PyAutoGUI']) + """</div></section>
<section class="section section-line"><div class="container"><div class="cta-panel" data-reveal><span class="eyebrow">Work with us</span><h2>Talk directly with the people building the product.</h2><div class="cta-actions"><a class="button button-primary" href="contact.html">Contact KhanaI Technologies <span class="arrow">→</span></a></div></div></div></section>
"""


contact = """
<section class="page-hero"><div class="container" data-reveal><span class="eyebrow">Contact</span><h1 class="page-title">Let's build<br><span class="gradient-text">something useful.</span></h1><p class="page-lead">Ready to deploy AI for your business? Have a question about WinPilot AI, WinHeart AI, ClipVault AI, WinQor, or TradingX? Reach out directly.</p></div></section>
<section class="section section-line"><div class="container"><div class="contact-grid"><div data-reveal><span class="kicker">Get in touch</span><h2 style="font-size:clamp(2rem,5vw,4rem);line-height:1;letter-spacing:-.05em;margin:0">KhanaI Technologies</h2><p>AI engineering company available worldwide, remote-first.</p><div class="contact-methods"><a class="card contact-method" href="https://wa.me/916303716492" target="_blank" rel="noopener noreferrer"><span class="icon-box">WA</span><span><strong>WhatsApp</strong><span>+91 6303716492</span></span></a><a class="card contact-method" href="mailto:winpilotai@gmail.com"><span class="icon-box">@</span><span><strong>Email</strong><span>winpilotai@gmail.com</span></span></a><div class="card contact-method"><span class="icon-box">IN</span><span><strong>Location</strong><span>Hyderabad, India · Worldwide remote-first</span></span></div></div></div><form class="card contact-form" data-contact-form data-reveal><div class="field"><label for="name">Name</label><input id="name" name="name" required placeholder="Your name" autocomplete="name"></div><div class="field"><label for="email">Email</label><input id="email" type="email" name="email" required placeholder="you@company.com" autocomplete="email"></div><div class="field"><label for="message">Message</label><textarea id="message" name="message" required placeholder="Tell us about your project..."></textarea></div><button class="button button-primary" type="submit">Prepare email <span class="arrow">→</span></button></form></div></div></section>
"""


render("index.html", "KhanaI Technologies | AI products and engineering", "KhanaI Technologies builds WinPilot AI, WinHeart AI, ClipVault AI, WinQor, TradingX, and focused AI systems for business.", home)
render("products.html", "Products | KhanaI Technologies", "Explore WinPilot AI, WinHeart AI, ClipVault AI, WinQor, and TradingX.", products_page)
render("winpilot.html", "WinPilot AI | Windows AI workspace", "WinPilot AI brings chat, documents, image understanding, voice, and productivity into one Windows workspace.", winpilot, schema_for_product("WinPilot AI", PRODUCTS[0]["summary"], "winpilot.html", WINPILOT_STORE))
render("winheart.html", "WinHeart AI | Diagnose. Fix. Protect.", "WinHeart AI is a local-first Windows assistant for PC health checks, guided repair, change tracking, notes, reports, and privacy controls.", winheart, schema_for_product("WinHeart AI", PRODUCTS[1]["summary"], "winheart.html", WINHEART_STORE))
render("clipvault.html", "ClipVault AI | Capture more. Search smarter.", "ClipVault AI organises clipboard history, screenshots, text, links, and files in a private local Windows workspace.", clipvault, schema_for_product("ClipVault AI", PRODUCTS[2]["summary"], "clipvault.html", CLIPVAULT_STORE))
render("winqor.html", "WinQor | Compact AI model family", "WinQor is an upcoming compact AI model family planned in 150M, 300M, and 1B parameter editions.", winqor, schema_for_product("WinQor", PRODUCTS[3]["summary"], "winqor.html"))
render("tradingx.html", "TradingX | AI market intelligence", "TradingX processes market data and produces directional signals for currencies, gold, and Bitcoin as an informational decision-support tool.", tradingx, schema_for_product("TradingX", PRODUCTS[4]["summary"], "tradingx.html"))
render("solutions.html", "AI solutions | KhanaI Technologies", "Voice assistants, company AI, automation chatbots, and natural-language database systems built for real operations.", solutions)
render("company.html", "Company | KhanaI Technologies", "Learn about KhanaI Technologies, its products, engineering approach, founder, and technology stack.", company)
render("contact.html", "Contact | KhanaI Technologies", "Contact KhanaI Technologies about products, AI engineering, business automation, or product support.", contact)

error_page = """
<section class="page-hero"><div class="container" data-reveal><span class="eyebrow">404</span><h1 class="page-title">This page moved.</h1><p class="page-lead">The product, solution, or company page you requested could not be found.</p><div class="page-actions"><a class="button button-primary" href="index.html">Return home</a><a class="button" href="products.html">Explore products</a></div></div></section>
"""
render("404.html", "Page not found | KhanaI Technologies", "Return to KhanaI Technologies products and AI engineering services.", error_page)

sitemap_files = ["", "products.html", "winpilot.html", "winheart.html", "clipvault.html", "winqor.html", "tradingx.html", "solutions.html", "company.html", "contact.html", "privacy.html", "terms.html", "refund.html", "winheart-privacy.html", "winheart-terms.html", "winheart-refund.html"]
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(f"  <url><loc>{BASE_URL + path}</loc></url>" for path in sitemap_files) + "\n</urlset>\n"
(ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8", newline="\n")
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}sitemap.xml\n", encoding="utf-8", newline="\n")
print("Generated 10 core pages, 404.html, sitemap.xml, and robots.txt.")
