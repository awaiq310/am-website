# AM: demo agency website

Static site (no framework, no third-party scripts). "AM" is a fictional demo brand.

## Edit and rebuild
- Business details, nav and all copy: `content.py` (CONFIG at the top). Legal drafts: `legal.py`.
- Templates and pages: `build.py`. Styles: `assets/css/style.css`. Behaviour: `assets/js/main.js`.
- `python3 build.py` regenerates `dist/` (the deployable folder). `python3 qa.py` runs the link/overflow/form checks (needs Playwright).
- Preview locally: `cd dist && python3 -m http.server 8000`. Links are root-absolute (`/about/`), so serve from a domain root; opening files directly will not load CSS.
- Host `dist/` on any static host and configure it to serve `404.html` for missing pages.

## Before launch
1. Set real name, domain, phone, email, privacy email, address/hours, socials in `CONFIG`; rebuild.
2. Connect the form: set `form_endpoint` to a processor (e.g. a form service or your own API). Until then the form runs in demo mode and transmits nothing.
3. Have a lawyer review `legal.py` pages (Pakistan, and India DPDP if serving Indian users).
4. Replace demo case studies and sample team cards with real, approved content. Add testimonials only when genuine.
5. Run a trademark/name check on the brand; update `og-default.png`/logo if the name changes.
6. Re-audit cookies/trackers if you add analytics or ad pixels (add consent gating first).

Fonts: Inter (SIL OFL), self-hosted from `assets/fonts` (licence file included).
