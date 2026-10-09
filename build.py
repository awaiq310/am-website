# -*- coding: utf-8 -*-
"""Static site generator for the AM demo. Run: python3 build.py  ->  ./dist"""
import html, json, math, os, shutil, datetime
from content import *
from legal import PRIVACY, TERMS, REFUND, COOKIE_BODY_TOP, COOKIE_SECTIONS, COOKIE_SECTIONS_AFTER, DRAFT, flag

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "dist")
NAME = CONFIG["name"]; SITE = CONFIG["site_url"].rstrip("/")
TODAY = datetime.date(2026, 10, 7).isoformat()
YEAR = datetime.date.today().year
PAGES = []  # (path, indexable)
e = html.escape


def write(path, content):
    fp = os.path.join(OUT, path.lstrip("/"))
    if fp.endswith("/") or fp.endswith("\\"):
        fp = os.path.join(fp, "index.html")
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)


def btn(label, href, kind="primary", arrow=True):
    a = ' <span class="arrow" aria-hidden="true">&rarr;</span>' if arrow else ""
    return f'<a class="btn btn-{kind}" href="{href}">{e(label)}{a}</a>'


def logo(cls="", light=False):
    src = "am-logo-light.svg" if light else "am-logo-dark.svg"
    return (f'<a class="logo {cls}" href="/" aria-label="{e(NAME)}, home">'
            f'<img src="/assets/img/{src}" width="73" height="30" alt="">'
            f'<span class="visually-hidden">{e(NAME)}</span></a>')


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "</script>"


def head(title, desc, path, jsonld=(), noindex=False):
    url = SITE + path
    img = SITE + "/assets/img/og-default.png"
    robots = '<meta name="robots" content="noindex, follow">' if noindex else ""
    canon = "" if noindex else f'<link rel="canonical" href="{url}">'
    return f"""<!doctype html>
<html lang="en-PK">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{robots}{canon}
<meta name="theme-color" content="#14201E">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(NAME)}">
<meta property="og:locale" content="en_PK">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(NAME)}: marketing that turns attention into growth">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{img}">
<link rel="preload" href="/assets/fonts/InterDisplay-Bold.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="/assets/css/style.css">
<script>document.documentElement.classList.add("js")</script>
{''.join(ld(j) for j in jsonld)}
</head>
"""


def header(path):
    def cur(href):
        if href == "/":
            return path == "/"
        return path.startswith(href)
    items = "".join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if cur(h) else ""}>{e(n)}</a></li>' for n, h in NAV)
    mitems = "".join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if cur(h) else ""}>{e(n)}</a></li>' for n, h in NAV)
    return f"""<body>
<a class="skip-link" href="#main">Skip to main content</a>
<header class="site-header">
<div class="container header-inner">
{logo()}
<nav class="nav-desktop" aria-label="Main"><ul>{items}</ul></nav>
<a class="btn btn-primary header-cta" href="/contact/">Book a Strategy Call <span class="arrow" aria-hidden="true">&rarr;</span></a>
<button class="menu-btn" id="menu-btn" type="button" aria-expanded="false" aria-controls="menu-panel"><span class="bars" aria-hidden="true"><span></span></span><span>Menu</span></button>
</div>
</header>
<div class="menu-panel" id="menu-panel" role="dialog" aria-modal="true" aria-label="Main menu">
<div class="menu-top">{logo(light=True)}<button class="menu-close" id="menu-close" type="button">Close</button></div>
<nav aria-label="Mobile"><ul>{mitems}</ul></nav>
<a class="btn btn-primary" href="/contact/">Book a Strategy Call</a>
<div class="menu-contact"><p><a href="tel:{CONFIG['phone_tel']}" aria-label="Call us on {CONFIG['phone_display']}">{CONFIG['phone_display']}</a><br><a href="mailto:{CONFIG['email']}" aria-label="Email us at {CONFIG['email']}">{CONFIG['email']}</a></p></div>
</div>
"""


def footer():
    svc = "".join(f'<li><a href="/services/{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES)
    nav = "".join(f'<li><a href="{h}">{e(n)}</a></li>' for n, h in NAV)
    socials = ""
    if CONFIG["socials"]:
        socials = "<h2 style='margin-top:24px'>Follow</h2><ul>" + "".join(
            f'<li><a href="{u}" rel="noopener noreferrer" target="_blank">{e(n)}<span class="visually-hidden"> (opens in a new tab)</span></a></li>' for n, u in CONFIG["socials"].items()) + "</ul>"
    addr = f"<li>{e(CONFIG['address'])}</li>" if CONFIG["address"] else ""
    hours = f"<li>{e(CONFIG['hours'])}</li>" if CONFIG["hours"] else ""
    return f"""<footer class="site-footer">
<div class="container">
<div class="footer-grid">
<div class="footer-brand">{logo(light=True)}<p>A digital marketing agency based in {e(CONFIG['location'])}, helping businesses grow through strategy, creative work, technology and measurable campaigns.</p></div>
<div class="footer-col"><h2>Navigate</h2><ul>{nav}</ul></div>
<div class="footer-col"><h2>Services</h2><ul>{svc}</ul></div>
<div class="footer-col"><h2>Contact</h2><ul>
<li><a href="tel:{CONFIG['phone_tel']}" aria-label="Call us on {CONFIG['phone_display']}">{CONFIG['phone_display']}</a></li>
<li><a href="mailto:{CONFIG['email']}" aria-label="Email us at {CONFIG['email']}">{CONFIG['email']}</a></li>
<li>{e(CONFIG['location'])}</li>{addr}{hours}</ul>{socials}</div>
</div>
<div class="footer-bottom">
<p>&copy; <span data-year>{YEAR}</span> {e(NAME)}. All rights reserved.</p>
<ul aria-label="Legal"><li><a href="/privacy-policy/">Privacy Policy</a></li><li><a href="/terms-and-conditions/">Terms &amp; Conditions</a></li><li><a href="/cookie-policy/">Cookie Policy</a></li><li><a href="/refund-policy/">Refund Policy</a></li><li><a href="/cookie-policy/#preferences">Cookie preferences</a></li></ul>
</div>
</div>
</footer>
<script src="/assets/js/main.js" defer></script>
</body>
</html>
"""


def breadcrumb(trail):
    li = "".join(f'<li><a href="{h}">{e(n)}</a></li>' for n, h in trail[:-1]) + f'<li aria-current="page">{e(trail[-1][0])}</li>'
    return f'<nav class="breadcrumb" aria-label="Breadcrumb"><ol>{li}</ol></nav>'


def bc_ld(trail):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + h} for i, (n, h) in enumerate(trail)]}


def page(path, title, desc, main, jsonld=(), noindex=False):
    if not noindex:
        PAGES.append(path)
    out = head(title, desc, path, jsonld, noindex) + header(path) + f'<main id="main" tabindex="-1">\n{main}\n</main>\n' + footer()
    write(path, out)


def cta_band(heading="Ready to talk about your growth?", text="Tell us about your business. We will suggest a sensible next step, whether or not we are the right fit."):
    return f"""<section class="on-dark cta-band"><div class="container"><div class="inner reveal">
<div><h2>{e(heading)}</h2><p class="lead" style="margin-top:16px">{e(text)}</p></div>
<div class="btn-row">{btn("Book a Strategy Call", "/contact/")}{btn("Explore Our Services", "/services/", "outline")}</div>
</div></div></section>"""


def hero_svg():
    cx, cy = 260, 270
    p = ['<svg viewBox="0 0 520 540" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">',
         '<rect width="520" height="540" rx="10" fill="#14201E"/>',
         '<g class="spin-slow">']
    for i, r in enumerate([60, 100, 140, 180, 225]):
        accent = i == 2
        p.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{"#E4572E" if accent else "#2F443F"}" stroke-width="{2.2 if accent else 1.5}"/>')
    for rot in (0, 45):
        pts = " ".join(f"{cx + 150 * math.cos(math.radians(rot + 45 + 90 * k)):.1f},{cy + 150 * math.sin(math.radians(rot + 45 + 90 * k)):.1f}" for k in range(4))
        p.append(f'<polygon points="{pts}" fill="none" stroke="#B9C6C1" stroke-opacity=".55" stroke-width="1.4"/>')
    for k in range(24):
        a = math.radians(k * 15)
        p.append(f'<circle cx="{cx + 225 * math.cos(a):.1f}" cy="{cy + 225 * math.sin(a):.1f}" r="{3.2 if k % 6 == 0 else 1.8}" fill="{"#E4572E" if k % 6 == 0 else "#B9C6C1"}"/>')
    p.append("</g>")
    p.append(f'<path d="M{cx} {cy} L{cx + 100} {cy} A100 100 0 0 0 {cx} {cy - 100} Z" fill="#E4572E"/>')
    p.append('<path d="M70 450 L190 372 L272 400 L440 150" fill="none" stroke="#F5F1E8" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>')
    p.append('<circle cx="440" cy="150" r="11" fill="#F5F1E8"/><circle cx="440" cy="150" r="5" fill="#C2431F"/>')
    p.append("</svg>")
    return "".join(p)


def svc_cards():
    return '<div class="service-grid">' + "".join(
        f'<a class="service-item reveal" href="/services/{s["slug"]}/"><span class="idx">{i + 1:02d}</span><h3>{e(s["name"])}</h3><p>{e(s["short"])}</p><span class="go">Learn more <span aria-hidden="true">&rarr;</span><span class="visually-hidden"> about {e(s["name"])}</span></span></a>'
        for i, s in enumerate(SERVICES)) + "</div>"


def faq_html(items):
    return '<div class="faq reveal">' + "".join(
        f'<details><summary>{e(q)}</summary><div class="answer"><p>{e(a)}</p></div></details>' for q, a in items) + "</div>"


def cases_cards(h=3):
    return '<div class="cs-grid">' + "".join(
        f'<a class="cs-card reveal" href="/case-studies/{c["slug"]}/"><div class="cs-card-industry" aria-hidden="true">{e(c["industry"])}</div><h{h}>{e(c["name"])}</h{h}><p>{e(c["summary"])}</p><ul class="meta"><li>{e(c["industry"])}</li></ul><span class="go" style="margin-top:14px">Read more <span aria-hidden="true">&rarr;</span><span class="visually-hidden">: {e(c["name"])}</span></span></a>'
        for c in CASES) + "</div>"


# ---------------------------------------------------------------- pages
def build_home():
    org = {"@context": "https://schema.org", "@type": "ProfessionalService", "name": NAME, "url": SITE + "/",
           "logo": SITE + "/assets/img/logo-mark.svg", "image": SITE + "/assets/img/og-default.png",
           "description": "Digital marketing agency based in Pakistan offering strategy, social media, SEO, paid media, content, branding, web design, lead generation, automation and analytics.",
           "areaServed": ["PK", "Worldwide"], "address": {"@type": "PostalAddress", "addressCountry": "PK"}}
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]}
    SVC_GROUPS = [
        ("Advertising & Media",    ["digital-marketing", "google-ads-ppc", "meta-ads", "lead-generation"]),
        ("Content & Brand",        ["social-media-marketing", "content-marketing", "branding"]),
        ("Technical & Growth",     ["seo", "website-design", "marketing-automation", "analytics-cro"]),
    ]
    def svc_grouped():
        out = []
        for group_name, slugs in SVC_GROUPS:
            items = "".join(
                f'<a class="service-item reveal" href="/services/{s["slug"]}/"><span class="idx">{i+1:02d}</span><h3>{e(s["name"])}</h3><p>{e(s["short"])}</p><span class="go">Learn more <span aria-hidden="true">&rarr;</span><span class="visually-hidden"> about {e(s["name"])}</span></span></a>'
                for i, slug in enumerate(slugs) for s in [SVC[slug]]
            )
            out.append(f'<div class="svc-group"><p class="svc-group-label">{e(group_name)}</p><div class="service-grid">{items}</div></div>')
        return "".join(out)
    why = "".join(f'<div class="feature reveal"><h3>{e(t)}</h3><p>{e(d)}</p></div>' for t, d in WHY)
    steps = "".join(f"<li class='reveal'><h3>{e(t)}</h3><p>{e(d)}</p></li>" for t, d in PROCESS)
    inds = "".join(f"<li>{e(i)}</li>" for i in INDUSTRIES)
    meas = "".join(f'<div class="measure reveal"><h3>{e(t)}</h3><p>{e(d)}</p></div>' for t, d in MEASURES)
    strip = "".join(f'<li><span class="num">{n}</span><div>{e(t)}<span>{e(d)}</span></div></li>' for n, t, d in PRINCIPLES)
    main = f"""
<section class="hero"><div class="container hero-grid">
<div>
<p class="eyebrow eyebrow-long">Digital marketing agency in Pakistan</p>
<h1>Marketing That Turns Attention Into <em>Growth.</em></h1>
<p class="lead">We help businesses grow through strategy, creative marketing, technology and measurable campaigns, from first idea to the numbers that show what is working.</p>
<div class="btn-row">{btn("Book a Strategy Call", "/contact/")}{btn("Explore Our Services", "/services/", "outline")}</div>
<p class="hero-note">Based in Pakistan. Working with local businesses, startups, e-commerce brands and international clients.</p>
</div>
<div class="hero-visual">{hero_svg()}</div>
</div></section>

<section class="strip" aria-label="How we work"><div class="container"><ul>{strip}</ul></div></section>

<section class="section" id="services"><div class="container">
<div class="section-head reveal"><p class="eyebrow">Services</p><h2>Everything you need to be found, chosen and remembered.</h2><p>Eleven connected services, so strategy, creative, media and measurement work as one.</p></div>
{svc_grouped()}
<div class="btn-row">{btn("View All Services", "/services/", "outline")}</div>
</div></section>

<section class="section bg-white"><div class="container split split-wide">
<div class="reveal"><p class="eyebrow">Why choose us</p><h2>A calmer, more accountable way to do marketing.</h2><p class="lead">No inflated promises. A clear plan, honest reporting and a team that stays close to the work.</p></div>
<div class="feature-list cols-2">{why}</div>
</div></section>

<section class="section on-dark"><div class="container">
<div class="section-head reveal"><p class="eyebrow">Our process</p><h2>From first conversation to continuous improvement.</h2></div>
<ol class="steps five">{steps}</ol>
</div></section>

<section class="section"><div class="container split">
<div class="reveal"><p class="eyebrow">Industries</p><h2>Built around how different businesses grow.</h2><p class="lead">Each sector has its own buyers, regulations and rhythms. We plan accordingly.</p></div>
<ul class="tag-list reveal">{inds}</ul>
</div></section>

<section class="section bg-paper2"><div class="container">
<div class="section-head reveal"><p class="eyebrow">Case studies</p><h2>How we approach real problems.</h2><p>These are sample projects that show our method. They are demonstrations, not real clients or results.</p></div>
{cases_cards()}
<div class="btn-row">{btn("See All Case Studies", "/case-studies/", "outline")}</div>
</div></section>

<section class="section on-dark"><div class="container">
<div class="section-head reveal"><p class="eyebrow">Results</p><h2>What we measure, and report to you.</h2><p>We agree the measures that matter before work begins. Typical examples are below. We never promise specific numbers.</p></div>
<div class="measure-grid">{meas}</div>
</div></section>

<section class="section"><div class="container">
<div class="section-head reveal"><p class="eyebrow">FAQ</p><h2>Questions we are often asked.</h2></div>
{faq_html(FAQS)}
</div></section>
{cta_band()}
"""
    page("/", f"Digital Marketing Agency in Pakistan | {NAME}",
         "Pakistan-based digital marketing agency for businesses and startups. Strategy, SEO, social media, Google and Meta Ads, branding and web design with clear reporting.",
         main, [org, faq])


def build_about():
    vals = [("Clarity", "We explain what we are doing, why, and what it costs, in plain language."),
            ("Accountability", "Agreed measures, regular reviews and named owners for every piece of work."),
            ("Craft", "Careful design, writing and engineering, because details shape trust."),
            ("Curiosity", "We study your customers and market before we recommend anything."),
            ("Respect for your budget", "Every rupee should have a reason, and we will tell you when something is not worth doing.")]
    v = "".join(f'<div class="feature reveal"><h3>{e(t)}</h3><p>{e(d)}</p></div>' for t, d in vals)
    team = "".join(f'<div class="cs-card reveal"><span class="badge badge-demo">Sample profile</span><h3>{e(r)}</h3><p>{e(d)}</p></div>' for r, d in [
        ("Strategy lead", "Leads discovery, planning and the monthly review with clients."),
        ("Creative and design lead", "Guides brand, visual direction and campaign creative."),
        ("Performance and analytics lead", "Owns paid media, tracking and reporting.")])
    trail = [("Home", "/"), ("About", "/about/")]
    main = f"""
<section class="page-hero"><div class="container">{breadcrumb(trail)}<p class="eyebrow">About us</p><h1>A marketing partner built around evidence, not hype.</h1>
<p class="lead">{e(NAME)} is a digital marketing agency based in {e(CONFIG['location'])}. We work with local businesses, startups, e-commerce brands and international clients.</p></div></section>

<section class="section"><div class="container split">
<div class="reveal"><p class="eyebrow">Our story</p><h2>Marketing should be judged by what it does for the business.</h2></div>
<div class="reveal"><p>We started from a simple frustration: too much marketing is judged by activity. Reports celebrate impressions and followers while owners still wonder where their enquiries come from.</p>
<p>So we built an agency around a different habit. Agree what success means. Set up measurement first. Make decisions from evidence. Say clearly when something is not working.</p>
<p>We are based in Pakistan, and we understand the way local customers discover, compare and buy, from WhatsApp conversations and mobile-first browsing to cash on delivery and mobile wallets. We also work with international clients who want a thoughtful, responsive partner.</p></div>
</div></section>

<section class="section bg-white"><div class="container split">
<div class="reveal"><p class="eyebrow">Mission</p><h2>Help businesses grow with marketing they can understand and trust.</h2></div>
<div class="reveal"><p class="eyebrow">Vision</p><h2>Make honest, measurable marketing the normal standard.</h2></div>
</div></section>

<section class="section"><div class="container">
<div class="section-head reveal"><p class="eyebrow">Values</p><h2>How we work, every day.</h2></div>
<div class="feature-list cols-2">{v}</div>
</div></section>

<section class="section on-dark"><div class="container split">
<div class="reveal"><p class="eyebrow">Marketing philosophy</p><h2>Attention is only the start.</h2></div>
<div class="reveal"><p class="lead">Attention matters only if it leads to understanding, trust and action. We design each step of that journey, from the first impression to the follow-up message, and we measure where people drop out.</p>
<p>Great creative and sound strategy are not opposites. The strongest campaigns combine a clear idea, the right audience and a reliable way to learn from the results.</p></div>
</div></section>

<section class="section light-steps"><div class="container">
<div class="section-head reveal"><p class="eyebrow">Strategy approach</p><h2>Five steps, repeated and refined.</h2></div>
<ol class="steps five">{''.join(f"<li class='reveal'><h3>{e(t)}</h3><p>{e(d)}</p></li>" for t, d in PROCESS)}</ol>
</div></section>

<section class="section bg-paper2"><div class="container">
<div class="section-head reveal"><p class="eyebrow">Team</p><h2>The people behind your work.</h2><p>Roles we staff on every engagement. Individual team profiles are added here when real team members are confirmed.</p></div>
<div class="cs-grid">{team}</div>

</div></section>
{cta_band()}
"""
    page("/about/", f"About {NAME} | Digital Marketing Agency in Pakistan",
         f"Learn how {NAME}, a Pakistan-based digital marketing agency, works: our story, mission, values, philosophy and strategy approach.",
         main, [bc_ld(trail)])


def build_services():
    trail = [("Home", "/"), ("Services", "/services/")]
    blocks = "".join(f"""<section class="svc-block reveal" id="{s['slug']}"><div><p class="eyebrow">{i + 1:02d}</p><h2>{e(s['name'])}</h2></div>
<div><p class="lead">{e(s['short'])}</p><ul class="checklist two">{''.join(f'<li>{e(d)}</li>' for d in s['deliverables'][:4])}</ul>
<p style="margin-top:22px"><a class="text-link" href="/services/{s['slug']}/">Explore {e(s['name'])} <span aria-hidden="true">&rarr;</span></a></p></div></section>""" for i, s in enumerate(SERVICES))
    chips = "".join(f'<li><a href="#{s["slug"]}">{e(s["name"])}</a></li>' for s in SERVICES)
    main = f"""
<section class="page-hero"><div class="container">{breadcrumb(trail)}<p class="eyebrow">Services</p><h1>Marketing services that work together.</h1>
<p class="lead">Choose a single service or a connected programme. Every engagement starts with strategy and ends with clear reporting. We do not guarantee specific results.</p>
<ul class="side-nav" style="margin-top:28px" aria-label="Jump to a service">{chips}</ul></div></section>
<section class="section-tight"><div class="container">{blocks}</div></section>
{cta_band("Not sure which service you need?", "Book a strategy call and we will help you work out where to start.")}
"""
    page("/services/", f"Services: Marketing, SEO, Ads & Web Design | {NAME}",
         "SEO, social media, Google Ads, Meta Ads, content, branding, web design, lead generation, automation and analytics services from a Pakistan-based agency.",
         main, [bc_ld(trail)])


def build_service(s):
    trail = [("Home", "/"), ("Services", "/services/"), (s["name"], f"/services/{s['slug']}/")]
    proc = "".join(f"<li><h3>{e(t)}</h3><p>{e(d)}</p></li>" for t, d in s["process"])
    rel = "".join(f'<li><a href="/services/{r}/">{e(SVC[r]["name"])}</a></li>' for r in s["related"])
    sch = {"@context": "https://schema.org", "@type": "Service", "name": s["name"], "serviceType": s["name"],
           "description": s["desc"], "provider": {"@type": "ProfessionalService", "name": NAME, "url": SITE + "/"},
           "areaServed": ["PK", "Worldwide"], "url": SITE + f"/services/{s['slug']}/"}
    main = f"""
<section class="page-hero"><div class="container">{breadcrumb(trail)}<p class="eyebrow">{e(s['name'])}</p><h1>{e(s['hero'])}</h1>
<p class="lead">{e(s['short'])}</p><div class="btn-row">{btn("Book a Strategy Call", "/contact/?service=" + s['slug'])}{btn("View Pricing", "/pricing/", "outline")}</div></div></section>
<section class="section-tight"><div class="container">
<section class="svc-block reveal"><h2>The problem</h2><p>{e(s['problem'])}</p></section>
<section class="svc-block reveal"><h2>Our solution</h2><p>{e(s['solution'])}</p></section>
<section class="svc-block reveal light-steps"><h2>Our process</h2><ol class="steps">{proc}</ol></section>
<section class="svc-block reveal"><h2>Deliverables</h2><ul class="checklist two">{''.join(f'<li>{e(d)}</li>' for d in s['deliverables'])}</ul></section>
<section class="svc-block reveal"><h2>Ideal customer</h2><ul class="checklist">{''.join(f'<li>{e(d)}</li>' for d in s['ideal'])}</ul></section>
<section class="svc-block reveal"><h2>A note on results</h2><p>We do not guarantee specific results. Outcomes depend on your market, offer, budget and competition. We agree measures and targets with you, report honestly and recommend what to do next.</p></section>
<section class="svc-block reveal"><h2>Related services</h2><ul class="side-nav">{rel}</ul></section>
</div></section>
{cta_band(f"Talk to us about {s['name']}.", "Tell us about your business and goals. We will recommend a sensible next step.")}
"""
    page(f"/services/{s['slug']}/", s["title"], s["desc"], main, [bc_ld(trail), sch])


def build_cases():
    trail = [("Home", "/"), ("Case Studies", "/case-studies/")]
    main = f"""
<section class="page-hero"><div class="container">{breadcrumb(trail)}<p class="eyebrow">Case studies</p><h1>How we approach real marketing problems.</h1>
<p class="lead">Real-world projects showing our strategy, execution and results across different industries.</p></div></section>
<section class="section"><div class="container">
{cases_cards(2)}
</div></section>
{cta_band()}
"""
    page("/case-studies/", f"Sample Case Studies | {NAME}",
         "Sample case studies showing how a Pakistan-based digital marketing agency plans branding, SEO, paid media and lead generation projects. Demonstrations only.",
         main, [bc_ld(trail)])


def build_case(c):
    trail = [("Home", "/"), ("Case Studies", "/case-studies/"), (c["name"], f"/case-studies/{c['slug']}/")]
    rows = [("Project", f"<p>{e(c['name'])}</p>"), ("Industry", f"<p>{e(c['industry'])}</p>"),
            ("Challenge", f"<p>{e(c['challenge'])}</p>"), ("Strategy", f"<p>{e(c['strategy'])}</p>"),
            ("Execution", "<ul class='checklist'>" + "".join(f"<li>{e(x)}</li>" for x in c["execution"]) + "</ul>"),
            ("Tools and platforms", "<ul class='tag-list'>" + "".join(f"<li>{e(x)}</li>" for x in c["tools"]) + "</ul>"),
            ("Results", "<p><strong>No results are claimed.</strong> This is a demonstration, so there is no real performance data. In a real case study this section reports verified figures supplied by the client. We would report measures such as:</p><ul class='checklist'>" + "".join(f"<li>{e(x)}</li>" for x in c["report"]) + "</ul>")]
    blocks = "".join(f'<section class="cs-block reveal"><h2>{t}</h2><div>{b}</div></section>' for t, b in rows)
    svcs = "".join(f'<li><a href="/services/{x}/">{e(SVC[x]["name"])}</a></li>' for x in c["services"])
    main = f"""
<section class="page-hero"><div class="container">{breadcrumb(trail)}<h1>{e(c['name'])}</h1>
<p class="lead">{e(c['summary'])}</p></div></section>
<section class="section-tight"><div class="container">
<div class="cs-detail">{blocks}</div>
<div class="cs-block reveal"><h2>Services involved</h2><ul class="side-nav">{svcs}</ul></div>
</div></section>
{cta_band("Want a plan like this for your business?", "Book a strategy call and we will talk through your goals and the best first step.")}
"""
    page(f"/case-studies/{c['slug']}/", f"Demo Case Study: {c['industry']} | {NAME}",
         f"Illustrative demo case study in {c['industry'].lower()}. It shows our approach and is not a real client or result.", main, [bc_ld(trail)])


def build_pricing():
    trail = [("Home", "/"), ("Pricing", "/pricing/")]
    plans = [
        ("Starter", "For businesses getting started with focused, well-measured marketing.",
         ["Strategy session and written plan", "One or two priority channels", "Tracking and reporting set-up", "Monthly performance summary", "Email support"]),
        ("Growth", "For businesses ready to run several channels together.",
         ["Everything in Starter", "Three or more connected channels", "Content and creative production", "Landing page and conversion improvements", "Monthly review call"]),
        ("Performance", "For teams that want deeper optimisation and systems.",
         ["Everything in Growth", "Advanced paid media management", "Conversion rate optimisation programme", "Marketing automation and CRM workflows", "Detailed reporting and quarterly strategy review"])]
    cards = "".join(f'<div class="plan reveal"><h2>{n}</h2><p>{e(d)}</p><div class="price">Request Custom Pricing<small>Quoted in PKR (&#8360;) for Pakistan-based clients</small></div><ul class="checklist">{"".join(f"<li>{e(x)}</li>" for x in f)}</ul>{btn("Book a Strategy Call", "/contact/?plan=" + n.lower())}</div>' for n, d, f in plans)
    main = f"""
<section class="page-hero"><div class="container">{breadcrumb(trail)}<p class="eyebrow">Pricing</p><h1>Pricing shaped around your goals.</h1>
<p class="lead">Every business is different, so we price after a conversation. We quote in Pakistani rupees (&#8360;) for Pakistan-based clients and agree currency with international clients.</p></div></section>
<section class="section"><div class="container">
<div class="plan-grid">{cards}</div>

</div></section>
<section class="section bg-white"><div class="container split">
<div class="reveal"><p class="eyebrow">What affects your price</p><h2>Clear scope, clear proposal.</h2><p class="lead">We will never invent urgency or discounts. You get a written proposal that you can compare, question and take your time over.</p></div>
<ul class="checklist reveal"><li>The channels and number of campaigns involved</li><li>The amount and complexity of creative, content or development work</li><li>Reporting depth and meeting frequency</li><li>Whether the work is a one-off project or an ongoing retainer</li><li>Tools, integrations and data set-up required</li></ul>
</div></section>
<section class="section"><div class="container">
<div class="section-head reveal"><p class="eyebrow">FAQ</p><h2>Pricing questions.</h2></div>
{faq_html([FAQS[2], FAQS[3], FAQS[1]])}
</div></section>
{cta_band("Request a proposal that fits your budget.", "Tell us what you want to achieve. We will respond with a clear scope and fee.")}
"""
    page("/pricing/", f"Pricing | Digital Marketing Plans in PKR | {NAME}",
         "Starter, Growth and Performance digital marketing plans scoped to your goals. Request custom pricing in PKR. No fake discounts, no pressure.",
         main, [bc_ld(trail)])


def build_contact():
    trail = [("Home", "/"), ("Contact", "/contact/")]
    svc_opts = "".join(f'<option value="{s["slug"]}">{e(s["name"])}</option>' for s in SERVICES)
    c = CONFIG
    addr = f'<li><h3>Office address</h3><p>{e(c["address"])}</p></li>' if c["address"] else ""
    hours = f'<li><h3>Business hours</h3><p>{e(c["hours"])}</p></li>' if c["hours"] else ""
    main = f"""
<section class="page-hero"><div class="container">{breadcrumb(trail)}<p class="eyebrow">Contact</p><h1>Tell us what you want to achieve.</h1>
<p class="lead">Send an inquiry and a member of our team will reply. We only ask for what we need.</p></div></section>
<section class="section"><div class="container split split-wide" style="--x:0">
<div class="reveal">
<h2 style="font-size:1.6rem">Send an inquiry</h2>
<form id="contact-form" class="form-grid" novalidate data-endpoint="{e(c['form_endpoint'])}" aria-describedby="form-note">
<p id="form-note" class="hint" style="margin:0;color:var(--muted)">Fields marked <span class="req" aria-hidden="true" style="color:var(--accent)">*</span><span class="visually-hidden">with an asterisk</span> are required.</p>
<div class="two">
<div class="field"><label for="f-name">Full name <span class="req" aria-hidden="true">*</span><span class="visually-hidden">(required)</span></label><input id="f-name" name="name" type="text" autocomplete="name" required aria-describedby="name-error"><p class="field-error" id="name-error"></p></div>
<div class="field"><label for="f-email">Business email <span class="req" aria-hidden="true">*</span><span class="visually-hidden">(required)</span></label><input id="f-email" name="email" type="email" autocomplete="email" required aria-describedby="email-error"><p class="field-error" id="email-error"></p></div>
</div>
<div class="two">
<div class="field"><label for="f-phone">Phone number <span class="opt">(optional)</span></label><input id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" aria-describedby="phone-hint phone-error"><span class="hint" id="phone-hint">For example +92 300 1234567</span><p class="field-error" id="phone-error"></p></div>
<div class="field"><label for="f-company">Company <span class="opt">(optional)</span></label><input id="f-company" name="company" type="text" autocomplete="organization"></div>
</div>
<div class="field"><label for="f-website">Website <span class="opt">(optional)</span></label><input id="f-website" name="website" type="text" inputmode="url" autocomplete="url" aria-describedby="website-error"><p class="field-error" id="website-error"></p></div>
<div class="two">
<div class="field"><label for="f-service">Service <span class="req" aria-hidden="true">*</span><span class="visually-hidden">(required)</span></label><select id="f-service" name="service" required aria-describedby="service-error"><option value="">Choose a service</option>{svc_opts}<option value="not-sure">Not sure yet</option></select><p class="field-error" id="service-error"></p></div>
<div class="field"><label for="f-budget">Budget range <span class="opt">(optional)</span></label><select id="f-budget" name="budget"><option value="">Prefer to discuss</option><option>Under &#8360;100,000</option><option>&#8360;100,000 to &#8360;300,000</option><option>&#8360;300,000 to &#8360;750,000</option><option>Over &#8360;750,000</option><option>International budget (currency to be discussed)</option></select><span class="hint">Monthly or per project, whichever applies.</span></div>
</div>
<div class="field"><label for="f-message">Project details <span class="req" aria-hidden="true">*</span><span class="visually-hidden">(required)</span></label><textarea id="f-message" name="message" required aria-describedby="message-error"></textarea><p class="field-error" id="message-error"></p></div>
<div class="hp" aria-hidden="true"><label for="f-hp">Leave this field empty</label><input id="f-hp" name="company_site" type="text" tabindex="-1" autocomplete="off"></div>
<div class="field consent-field"><div class="consent"><input id="f-consent" name="consent" type="checkbox" required aria-describedby="consent-error"><label for="f-consent" id="consent-label">I agree that {e(NAME)} may use the information I provide to respond to my inquiry. See our <a href="/privacy-policy/">Privacy Policy</a>.</label></div><p class="field-error" id="consent-error"></p></div>
<div id="form-status" class="form-status" tabindex="-1"></div>
<div><button class="btn btn-primary" id="submit-btn" type="submit"><span class="spinner" aria-hidden="true"></span><span class="label">Send Inquiry</span></button></div>
</form>
</div>
<aside class="reveal" aria-label="Contact details">
<h2 style="font-size:1.6rem">Contact details</h2>
<ul class="contact-list">
<li><h3>Phone</h3><p><a href="tel:{c['phone_tel']}" aria-label="Call us on {c['phone_display']}">{c['phone_display']}</a></p></li>
<li><h3>Email</h3><p><a href="mailto:{c['email']}" aria-label="Email us at {c['email']}">{c['email']}</a></p></li>
<li><h3>Location</h3><p>{e(c['location'])}. Serving clients locally and internationally.</p></li>
{addr}{hours}
</ul>

</aside>
</div></section>
"""
    page("/contact/", f"Contact {NAME} | Book a Strategy Call",
         "Contact our Pakistan-based digital marketing team. Send an inquiry or book a strategy call to discuss SEO, paid media, branding, web design and lead generation.",
         main, [bc_ld(trail)])


def toc_and_sections(sections):
    toc = '<nav class="toc" aria-label="On this page"><strong>On this page</strong><ol>' + "".join(f'<li><a href="#{i}">{e(h)}</a></li>' for i, h, _ in sections) + "</ol></nav>"
    body = "".join(f'<section id="{i}"><h2>{e(h)}</h2>{b}</section>' for i, h, b in sections)
    return toc + body


def legal_page(path, title, h1, desc, sections, intro="", extra_after=""):
    trail = [("Home", "/"), (h1, path)]
    main = f"""
<section class="page-hero"><div class="container">{breadcrumb(trail)}<p class="eyebrow">Legal</p><h1>{e(h1)}</h1><p class="lead">Last updated: {CONFIG['updated']}</p></div></section>
<section class="section-tight"><div class="container"><div class="prose">{DRAFT}{intro}{toc_and_sections(sections)}{extra_after}</div></div></section>
"""
    page(path, title, desc, main, [bc_ld(trail)])


def build_cookies():
    prefs = """
<section id="preferences"><h2>Your cookie preferences</h2>
<p>No optional cookies or trackers are used on this site today, so nothing is switched on. The choices below are stored only on your device, are not pre-selected, and would be respected if optional tools were added later.</p>
<form class="cookie-prefs" id="cookie-prefs-form">
<div class="toggle-row"><div><label for="c-necessary">Necessary</label><small>Always on. Currently none are set.</small></div><input id="c-necessary" type="checkbox" checked disabled></div>
<div class="toggle-row"><div><label for="c-analytics">Analytics</label><small>Not in use on this site.</small></div><input id="c-analytics" name="analytics" type="checkbox"></div>
<div class="toggle-row"><div><label for="c-marketing">Marketing</label><small>Not in use on this site.</small></div><input id="c-marketing" name="marketing" type="checkbox"></div>
<div style="margin-top:18px"><button class="btn btn-dark" type="submit">Save preferences</button></div>
<p id="cookie-prefs-msg" role="status" tabindex="-1" style="margin:16px 0 0;font-weight:500"></p>
</form></section>"""
    secs = COOKIE_SECTIONS + COOKIE_SECTIONS_AFTER
    legal_page("/cookie-policy/", f"Cookie Policy | {NAME}", "Cookie Policy",
               f"How {NAME} uses cookies and similar technologies. This site uses no analytics or advertising cookies, and you can manage your preferences at any time.",
               secs, intro=COOKIE_BODY_TOP, extra_after=prefs)


def build_404():
    main = f"""
<section class="notfound"><div class="container">
<p class="big" aria-hidden="true">404</p>
<h1>404 &mdash; Page Not Found</h1>
<p class="lead">The page you are looking for may have moved, or the address may have been typed incorrectly. Here are some useful places to go next.</p>
<div class="btn-row">{btn("Back to Home", "/")}{btn("View Services", "/services/", "outline")}{btn("Contact Us", "/contact/", "outline")}</div>
</div></section>
"""
    page("/404.html", f"404: Page Not Found | {NAME}", "The page you requested could not be found. Return to the home page, view our services or contact us.", main, noindex=True)


def build_misc():
    urls = "".join(f"<url><loc>{SITE}{p}</loc><lastmod>{TODAY}</lastmod></url>" for p in PAGES)
    write("/sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    write("/robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    write("/site.webmanifest", json.dumps({"name": NAME, "short_name": NAME, "start_url": "/", "display": "browser", "background_color": "#F5F1E8", "theme_color": "#14201E",
        "icons": [{"src": "/assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=2))


if __name__ == "__main__":
    if os.path.exists(OUT):
        shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(OUT, exist_ok=True)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"))
    shutil.copy(os.path.join(ROOT, "favicon.ico"), OUT)
    shutil.copy(os.path.join(ROOT, "favicon.svg"), OUT)
    build_home(); build_about(); build_services()
    for s in SERVICES: build_service(s)
    build_cases()
    for c in CASES: build_case(c)
    build_pricing(); build_contact()
    legal_page("/privacy-policy/", f"Privacy Policy | {NAME}", "Privacy Policy", f"How {NAME} collects, uses and protects personal information, your rights, and our approach to data minimisation. Draft pending legal review.", PRIVACY)
    legal_page("/terms-and-conditions/", f"Terms & Conditions | {NAME}", "Terms & Conditions", f"Terms for using the {NAME} website and our digital marketing services. Draft pending legal review.", TERMS)
    build_cookies()
    legal_page("/refund-policy/", f"Refund Policy | {NAME}", "Refund Policy", f"How refunds and cancellations work for {NAME} services. Draft pending the owner's decisions and legal review.", REFUND)
    build_404(); build_misc()
    print("Built", len(PAGES), "indexable pages ->", OUT)
