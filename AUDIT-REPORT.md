# Final audit report: AM demo site (7 Oct 2026)

Automated checks ran on all 25 HTML pages (`qa.py`, headless Chromium). Legal compliance has NOT been professionally verified.

## PASS
- **Pages:** Home, About, Services, 11 service pages, Case Studies (+3 demo studies), Pricing, Contact, Privacy, Terms, Cookie, Refund, custom 404.
- **Links:** 0 broken internal links/anchors, 0 empty hrefs, all nav/footer/CTA links resolve; no external links or resources at all.
- **Layout:** no horizontal overflow on any page at 320, 360, 375, 390, 414, 768, 1024, 1280, 1440 and 1920px; no console errors.
- **Navigation:** logo links to `/` (desktop and mobile); mobile menu opens/closes, Esc closes, focus trapped and restored, body scroll locked, closes on link select; CTA in header and menu.
- **Contact:** `tel:` and `mailto:` links; validation, per-field errors, loading state, success/error messages; consent box unticked by default; service preselect via `?service=`.
- **SEO:** unique title, description and canonical on every page; one H1 and no heading skips; Open Graph/Twitter tags; JSON-LD (ProfessionalService, FAQPage, Service, BreadcrumbList); sitemap.xml; robots.txt; 404 is noindex.
- **Branding:** SVG/ICO/PNG favicons, Apple touch icon, web manifest; copyright year auto-updates.
- **Accessibility (checked):** skip link, visible focus, semantic landmarks, labelled form fields with text (not colour-only) errors, reduced-motion support; text/background contrast pairs all 4.5:1 or higher; decorative images have empty alt.
- **Authenticity:** no fake reviews, client logos, awards, certifications, statistics, prices, discounts or urgency; case studies and team cards labelled "Sample"/"Demo"; no guarantee language (explicit "no guaranteed results").
- **Privacy/tracking:** no cookies, analytics, pixels, embeds, maps or external fonts; no keys or secrets in front-end code; only data collected is the minimal form fields.
- **Performance:** ~150 KB fonts, no third-party JS, ~minimal vanilla JS, no raster images on pages (SVG art), lazy-loading not needed.

## NEEDS CONFIGURATION
- Real legal name, domain (`.example` placeholder in canonicals/sitemap), phone, email, privacy/grievance mailbox, address and hours (omitted until supplied), social links (omitted until supplied).
- Contact form endpoint (demo mode transmits nothing and says so).
- Real case studies, team members and testimonials (only when genuine and approved); real image assets with licences if added (none used; fonts are OFL).
- Retention periods, processor list, refund/notice terms, tax and payment methods in the legal pages.
- Confirm business policies stated in copy: account ownership in client's name, ad spend paid directly to platforms, remote service for international clients.
- Brand name trademark check; Open Graph image regenerated if name changes.

## LEGAL REVIEW
- Privacy Policy, Terms, Cookie Policy, Refund Policy are drafts with "LEGAL REVIEW REQUIRED" flags where owner/lawyer decisions are needed.
- Pakistan: status of any dedicated data-protection law, regulator/registration duties, consumer and e-commerce rules, tax treatment: unverified, no laws cited as obligations.
- India DPDP Act 2023 and Rules: notice wording/languages, consent records, withdrawal, children's data, cross-border transfers, grievance officer: flagged, no compliance claimed.
- Governing law/jurisdiction clause (default Pakistan) and liability cap need lawyer confirmation.
- Consent requirements for visitors in each region before adding any analytics/ads.
- Healthcare/sector advertising rules for sample clinic content if reused for real work.

## NOT IMPLEMENTED
- Server-side form handling, spam protection beyond a honeypot, and email delivery.
- Cookie consent banner (not needed today; preferences panel exists, nothing optional is loaded). Must be wired to any future tags.
- Analytics/tag manager/pixels (deliberately none), WebP/AVIF images (no raster images in use), site search, blog, CMS.
- Manual testing on physical devices, screen-reader testing (NVDA/VoiceOver) and a formal WCAG audit.
- Live external-link audit (none exist); real-world Core Web Vitals measurement after hosting.
