# -*- coding: utf-8 -*-
"""QA crawler: links, anchors, assets, metadata, headings, overflow at many widths, menu and form behaviour.
Usage: python3 qa.py   (serves ./dist on a local port)"""
import http.server, threading, socketserver, os, re, sys, json, functools
from urllib.parse import urljoin, urlparse
from html.parser import HTMLParser
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__)); DIST = os.path.join(ROOT, "dist")
PORT = 8765; BASE = f"http://127.0.0.1:{PORT}"


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=DIST, **k)
    def log_message(self, *a): pass
    def send_error(self, code, message=None, explain=None):
        if code == 404 and os.path.exists(os.path.join(DIST, "404.html")):
            body = open(os.path.join(DIST, "404.html"), "rb").read()
            self.send_response(404); self.send_header("Content-Type", "text/html"); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
        else: super().send_error(code, message, explain)


socketserver.TCPServer.allow_reuse_address = True
srv = socketserver.ThreadingTCPServer(("127.0.0.1", PORT), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()

pages = []
for dp, _, fs in os.walk(DIST):
    for f in fs:
        if f.endswith(".html"):
            rel = os.path.relpath(os.path.join(dp, f), DIST)
            pages.append("/" if rel == "index.html" else "/" + rel.replace("index.html", "") if rel.endswith("index.html") else "/" + rel)
pages.sort()
problems = []
def bad(msg): problems.append(msg); print("FAIL", msg)

import urllib.request, urllib.error
def status(url):
    try: return urllib.request.urlopen(url).status
    except urllib.error.HTTPError as e: return e.code

class P(HTMLParser):
    def __init__(s): super().__init__(); s.links=[]; s.ids=set(); s.imgs=[]; s.h=[]; s.title=""; s.meta={}; s.canon=None; s._t=None; s.scripts=[]; s.buf=""
    def handle_starttag(s, t, a):
        a = dict(a)
        if "id" in a: s.ids.add(a["id"])
        if t == "a": s.links.append(a.get("href"))
        if t == "img": s.imgs.append(a)
        if t in ("h1","h2","h3","h4"): s.h.append(int(t[1]))
        if t == "title": s._t = True
        if t == "meta" and a.get("name"): s.meta[a["name"]] = a.get("content","")
        if t == "meta" and a.get("property"): s.meta[a["property"]] = a.get("content","")
        if t == "link" and a.get("rel") == "canonical": s.canon = a.get("href")
        if t == "script" and a.get("src"): s.scripts.append(a["src"])
        if t == "link" and a.get("href","").startswith("http") and a.get("rel") != "canonical": s.scripts.append(a["href"])
    def handle_endtag(s, t):
        if t == "title": s._t = False
    def handle_data(s, d):
        if s._t: s.title += d

parsed = {}
for p in pages:
    parsed[p] = P(); parsed[p].feed(open(os.path.join(DIST, p.lstrip("/") + ("index.html" if p.endswith("/") else "")), encoding="utf-8").read() if p != "/" else open(os.path.join(DIST, "index.html"), encoding="utf-8").read())

print("Pages:", len(pages))
titles, descs, canons = {}, {}, {}
checked = {}
for p, d in parsed.items():
    if d.h.count(1) != 1: bad(f"{p}: h1 count {d.h.count(1)}")
    for a, b in zip(d.h, d.h[1:]):
        if b - a > 1: bad(f"{p}: heading jump h{a}->h{b}")
    t = d.title.strip()
    if not t or t.lower() in ("home", "untitled", "page"): bad(f"{p}: generic title")
    if len(t) > 62: bad(f"{p}: title {len(t)} chars: {t}")
    titles.setdefault(t, []).append(p)
    ds = d.meta.get("description", "")
    if not ds: bad(f"{p}: no description")
    if len(ds) > 165: bad(f"{p}: description {len(ds)} chars")
    descs.setdefault(ds, []).append(p)
    if p != "/404.html":
        if not d.canon: bad(f"{p}: no canonical")
        canons.setdefault(d.canon, []).append(p)
    for k in ("og:title", "og:description", "og:image", "og:url", "twitter:card"):
        if k not in d.meta: bad(f"{p}: missing {k}")
    for im in d.imgs:
        if "alt" not in im: bad(f"{p}: img without alt attribute {im}")
    for s in d.scripts:
        if urlparse(s).netloc: bad(f"{p}: external resource {s}")
    for href in d.links:
        if not href or href.strip() in ("#", ""): bad(f"{p}: empty href"); continue
        if href.startswith(("tel:", "mailto:")): continue
        if href.startswith("http"):
            bad(f"{p}: external link {href} (verify manually)"); continue
        u = urlparse(href)
        tgt = u.path or p
        key = tgt
        if key not in checked: checked[key] = status(BASE + tgt)
        if checked[key] != 200: bad(f"{p}: broken link {href} -> {checked[key]}")
        if u.fragment:
            tp = parsed.get(tgt if tgt in parsed else tgt)
            if tp is None or u.fragment not in tp.ids: bad(f"{p}: missing anchor {href}")
for k, v in titles.items():
    if len(v) > 1: bad(f"duplicate title {k}: {v}")
for k, v in descs.items():
    if len(v) > 1: bad(f"duplicate description: {v}")
for k, v in canons.items():
    if len(v) > 1: bad(f"duplicate canonical {k}: {v}")
# assets referenced in CSS/HTML exist
for a in ["/assets/css/style.css", "/assets/js/main.js", "/favicon.ico", "/favicon.svg", "/site.webmanifest", "/sitemap.xml", "/robots.txt", "/assets/img/og-default.png", "/assets/img/apple-touch-icon.png"]:
    if status(BASE + a) != 200: bad(f"missing asset {a}")
sm = open(os.path.join(DIST, "sitemap.xml")).read()
for p in pages:
    if p != "/404.html" and p not in sm: bad(f"{p} missing from sitemap")
print("static checks done:", len(problems), "problems")

widths = [320, 360, 375, 390, 414, 768, 1024, 1280, 1440, 1920]
OVER = """() => { const w = document.documentElement.clientWidth; const bad = [];
 document.querySelectorAll('body *').forEach(el => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
   if (cs.position === 'fixed' || el.closest('.menu-panel') || el.closest('.table-wrap') || el.closest('.hp') || el.closest('.skip-link') || el.closest('.visually-hidden')) return;
   if (r.width && r.right > w + 1) bad.push(el.tagName + '.' + el.className + ' right=' + Math.round(r.right)); });
 return {sw: document.documentElement.scrollWidth, cw: w, bad: bad.slice(0,4)}; }"""
with sync_playwright() as pw:
    br = pw.chromium.launch()
    os.makedirs("/tmp/qa-shots", exist_ok=True)
    for w in widths:
        ctx = br.new_context(viewport={"width": w, "height": 800}, device_scale_factor=1)
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        for p in pages:
            pg.goto(BASE + p, wait_until="load")
            pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))")
            r = pg.evaluate(OVER)
            if r["sw"] > r["cw"] or r["bad"]: bad(f"overflow {p} @{w}: scrollWidth {r['sw']} > {r['cw']} {r['bad']}")
        if errs: bad(f"console errors @{w}: {errs[:3]}")
        if w in (320, 390, 1440):
            for p in ["/", "/services/seo/", "/contact/", "/pricing/", "/404.html"]:
                pg.goto(BASE + p, wait_until="load"); pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))")
                pg.screenshot(path=f"/tmp/qa-shots/{w}-{p.strip('/').replace('/','_') or 'home'}.png", full_page=True)
        ctx.close()
    print("overflow checks done")
    # mobile menu
    ctx = br.new_context(viewport={"width": 375, "height": 700}); pg = ctx.new_page()
    pg.goto(BASE + "/"); btn = pg.locator("#menu-btn")
    assert btn.get_attribute("aria-expanded") == "false"
    btn.click(); pg.wait_for_timeout(350)
    if btn.get_attribute("aria-expanded") != "true": bad("menu did not open")
    if not pg.locator("#menu-panel").is_visible(): bad("menu panel not visible")
    if pg.evaluate("getComputedStyle(document.body).overflow") != "hidden": bad("body scroll not locked")
    if pg.evaluate("document.activeElement.id") != "menu-close": bad("focus not moved into menu")
    pg.keyboard.press("Escape"); pg.wait_for_timeout(350)
    if pg.locator("#menu-panel").is_visible(): bad("Escape did not close menu")
    if pg.evaluate("document.activeElement.id") != "menu-btn": bad("focus not restored")
    btn.click(); pg.wait_for_timeout(300); pg.locator("#menu-panel nav a", has_text="Pricing").click(); pg.wait_for_url("**/pricing/")
    if pg.locator("#menu-panel").is_visible(): bad("menu still open after navigation")
    # logo
    pg.goto(BASE + "/services/seo/"); pg.locator(".site-header .logo").click(); pg.wait_for_url(BASE + "/")
    # desktop nav
    ctx.close(); ctx = br.new_context(viewport={"width": 1440, "height": 900}); pg = ctx.new_page()
    pg.goto(BASE + "/");
    if pg.locator("#menu-btn").is_visible(): bad("hamburger visible on desktop")
    for n in ["About", "Services", "Case Studies", "Pricing", "Contact"]:
        pg.goto(BASE + "/"); pg.locator(".nav-desktop a", has_text=n).click(); pg.wait_for_load_state()
    # form
    pg.goto(BASE + "/contact/"); pg.locator("#submit-btn").click()
    if pg.locator("#name-error").inner_text() == "": bad("form: no name error on empty submit")
    if "Something went wrong" not in pg.locator("#form-status").inner_text(): bad("form: error status missing")
    if pg.locator("#f-consent").is_checked(): bad("consent pre-checked")
    pg.fill("#f-name", "Test User"); pg.fill("#f-email", "bad"); pg.fill("#f-phone", "12"); pg.fill("#f-message", "short")
    pg.locator("#submit-btn").click()
    for fid in ("email-error", "phone-error", "message-error", "service-error", "consent-error"):
        if not pg.locator("#" + fid).inner_text(): bad(f"form: {fid} empty")
    pg.fill("#f-email", "test@example.com"); pg.fill("#f-phone", "+92 300 1234567"); pg.fill("#f-message", "We want help with our search presence.")
    pg.select_option("#f-service", "seo"); pg.check("#f-consent"); pg.locator("#submit-btn").click(); pg.wait_for_timeout(1200)
    st = pg.locator("#form-status").inner_text()
    if "Thanks! Your inquiry has been received" not in st: bad("form: no success message: " + st)
    pg.goto(BASE + "/contact/?service=meta-ads")
    if pg.input_value("#f-service") != "meta-ads": bad("service preselect failed")
    # year
    yr = pg.locator("[data-year]").first.inner_text()
    import datetime
    if yr != str(datetime.date.today().year): bad("year mismatch " + yr)
    # cookie prefs
    pg.goto(BASE + "/cookie-policy/");
    if pg.locator("#c-analytics").is_checked() or pg.locator("#c-marketing").is_checked(): bad("optional cookie toggles pre-selected")
    br.close()
print("\nTOTAL PROBLEMS:", len(problems))
for p in problems: print(" -", p)
srv.shutdown()
