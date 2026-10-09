# -*- coding: utf-8 -*-
"""Draft legal pages. These are templates for review by a qualified lawyer; they are not legal advice
and are not a claim of compliance with any law."""
from content import CONFIG as C

N = C["name"]; LN = C["legal_name"]; PE = C["privacy_email"]; EM = C["email"]; UPD = C["updated"]


def flag(text, label="LEGAL REVIEW REQUIRED"):
    return f'<div class="legal-flag"><strong>{label}:</strong> {text}</div>'


def ul(items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


DRAFT = flag("This page is a draft prepared for the business owner. It has not been reviewed by a lawyer and is not legal advice. It does not claim compliance with any law. Have a qualified lawyer in Pakistan (and, if you serve Indian users, India) review and adapt it before launch.", "DRAFT: LEGAL REVIEW REQUIRED")

PRIVACY = [
 ("who-we-are", "Who we are", f"""
<p>This Privacy Policy explains how {LN} (trading as {N}, &ldquo;we&rdquo;, &ldquo;us&rdquo;) handles personal information collected through this website. We are a digital marketing agency based in {C['location']}.</p>
<p>For privacy questions or requests, email <a href="mailto:{PE}">{PE}</a>.</p>
{flag("Confirm the legal entity name, registration type and the person or role responsible for privacy matters. Add registered details only once they are real and verified.")}"""),
 ("data-we-collect", "Information we collect", f"""
<p>We collect only what we need to respond to you and to run this website.</p>
<h3>Information you give us</h3>
{ul(["<strong>Contact form:</strong> full name, business email address, company name, service of interest and project details. Phone number, website address and budget range are optional.",
     "<strong>Emails, calls and messages</strong> you send us directly, including anything you choose to include in them."])}
<h3>Information collected automatically</h3>
{ul(["Basic technical information that web servers receive when you visit any website, such as IP address, browser type, pages requested and time of request. These server logs are handled by our hosting provider for security and reliability.",
     "This website does not use analytics, advertising pixels or tracking cookies at the time of writing. See our <a href=\"/cookie-policy/\">Cookie Policy</a>."])}
<h3>Information we ask you not to send</h3>
<p>Please do not send national identity card (CNIC) numbers, passport numbers, passwords, payment card details or other sensitive personal information through the contact form or by email. We do not need them to respond to an inquiry.</p>"""),
 ("why-we-use-it", "Why we use your information and our legal basis", f"""
{ul(["To respond to your inquiry and prepare a proposal, which is a step you ask us to take before entering a contract.",
     "To communicate with you about the services you have asked about.",
     "To keep this website and our systems secure and working.",
     "To meet legal and accounting obligations if you become a client."])}
<p>We rely on your consent where you tick the consent box on the contact form. You may withdraw it at any time (see &ldquo;Your rights&rdquo;). We do not use your inquiry details for unrelated marketing without a separate, clear choice from you. We do not sell personal information.</p>
{flag("The lawful bases available depend on the laws that apply to you and to us. A lawyer should confirm which bases to state for Pakistan, India and any other regions served.")}"""),
 ("data-minimisation", "Data minimisation", """
<p>We ask only for the details needed to understand and answer your inquiry. Fields that are not essential are marked optional. We do not collect CNIC or passport numbers, payment card details, passwords or sensitive personal data through this website.</p>"""),
 ("retention", "How long we keep information", f"""
<p>We keep inquiry details only for as long as needed to respond and, if no engagement follows, for a limited period afterwards in case you contact us again. If you become a client, we keep records for as long as needed to deliver services and meet legal, tax and accounting requirements. We delete or anonymise information we no longer need.</p>
{flag("Insert the actual retention periods the business will follow (for example, a fixed number of months for unsuccessful inquiries) and confirm any minimum record-keeping periods under Pakistani tax and company law.")}"""),
 ("security", "Security", """
<p>We use reasonable technical and organisational measures to protect personal information, including encrypted connections (HTTPS), restricted access to inquiry data and the use of reputable service providers. No system is completely secure, and we cannot guarantee absolute security. If we become aware of a security incident affecting your personal information, we will take appropriate steps, including notifying you or authorities where the law requires it.</p>"""),
 ("processors", "Service providers and third parties", f"""
<p>We may share personal information with service providers who help us run the website and handle inquiries, only to the extent needed for those services and under appropriate terms. These may include website hosting, form processing, email, calendar scheduling and customer-relationship-management providers. We do not allow them to use your information for their own marketing.</p>
<p>We may also disclose information where required by law or to protect our legal rights.</p>
{flag("List the actual providers used at launch (hosting, form handler, email, CRM, calendar) and what each receives. The demo form is not connected to any provider yet. Confirm data-processing terms and where each provider stores data.", "NEEDS CONFIGURATION / LEGAL REVIEW REQUIRED")}"""),
 ("analytics", "Analytics and advertising", """
<p>At the time of writing, this website does not use Google Analytics, Google Tag Manager, Meta Pixel, LinkedIn Insight Tag, heatmaps or other advertising or analytics tools. If we add any, we will update this policy and our Cookie Policy and, where required, ask for your consent before they run.</p>"""),
 ("cookies", "Cookies", """
<p>See our <a href="/cookie-policy/">Cookie Policy</a> for details of the cookies and similar storage used on this website and how to manage your preferences.</p>"""),
 ("your-rights", "Your rights", f"""
<p>Depending on where you live, you may have rights to:</p>
{ul(["ask whether we hold personal information about you and request a copy;", "ask us to correct inaccurate or incomplete information;", "ask us to delete your information;", "withdraw consent you have given, at any time, without affecting what we did before you withdrew;", "object to or ask us to limit certain uses; and", "complain to a regulator or, where applicable, use our grievance contact below."])}
<p>To exercise a right, email <a href="mailto:{PE}">{PE}</a> from the address you used with us so we can verify your request. We will respond within a reasonable time.</p>
{flag("State the response time the business can honour and confirm which rights apply under the laws relevant to your users.")}"""),
 ("deletion", "Deleting your information", f"""
<p>You can ask us to delete your personal information at any time by emailing <a href="mailto:{PE}">{PE}</a>. We will delete it unless we must keep it for a legal reason, in which case we will tell you what we are keeping and why. Information held by our service providers will be deleted according to their processes.</p>"""),
 ("transfers", "International transfers", f"""
<p>We are based in {C['location']}. Some service providers may store or process information in other countries. Where we transfer personal information across borders, we intend to use providers that protect it appropriately.</p>
{flag("Confirm where each provider stores data, whether any restrictions on cross-border transfers apply under Pakistani or Indian law, and whether contractual safeguards are needed.")}"""),
 ("children", "Children", """
<p>Our services are for businesses and are not directed at children. We do not knowingly collect personal information from anyone under 18. If you believe a child has sent us information, please contact us and we will delete it.</p>"""),
 ("pakistan", "Pakistan legal context", f"""
<p>We aim to handle personal information responsibly and in line with laws that apply to us in Pakistan.</p>
{flag("Pakistan has had a long-running effort to adopt a dedicated personal data protection law, and its status, scope and any regulator or registration requirements must be checked on the date of launch. Other laws and sector rules (for example on electronic transactions, cybercrime and consumer protection, and obligations that depend on business structure) may also apply. We have not listed specific legal duties here because they must be confirmed by a Pakistani lawyer. Do not state that the business is compliant with any specific law until that review is complete.")}"""),
 ("india", "Users in India (Digital Personal Data Protection Act)", f"""
<p>If you are in India, we aim to give you a clear notice of what we collect and why, to ask for your consent through an unticked consent box, to let you withdraw consent as easily as you gave it, to collect only what is needed, and to give you a way to raise concerns (see &ldquo;Contact and grievances&rdquo;). We do not knowingly process the personal data of children.</p>
{flag("India's Digital Personal Data Protection Act, 2023 and its Rules may apply when personal data of people in India is processed in connection with offering services to them. A qualified lawyer should check the current status of the Rules and decide on: the wording and language of the notice (including availability in Indian languages where required), consent records, retention and erasure, children's data, cross-border transfer conditions, appointing any required contact or officer, breach notification, and whether any obligations beyond this notice apply. This page does not claim DPDP compliance.")}"""),
 ("contact", "Contact and grievances", f"""
<p>For questions, requests or complaints about how we handle personal information, email <a href="mailto:{PE}">{PE}</a>. We will acknowledge your message and respond within a reasonable time. If you are not satisfied, you may also contact the relevant data-protection authority in your country where one exists.</p>
{flag("Name the person or role responsible for privacy and grievance handling and add a monitored mailbox. Replace the demonstration address with a real one.", "NEEDS CONFIGURATION")}"""),
 ("updates", "Changes to this policy", f"""
<p>We may update this policy as our services or the law change. The date at the top shows when it was last revised. Material changes will be highlighted on this page. Last updated: {UPD}.</p>"""),
]

TERMS = [
 ("acceptance", "About these terms", f"""
<p>These Terms &amp; Conditions govern your use of this website and, together with a written proposal or services agreement, our services. {LN} (trading as {N}) is based in {C['location']}. By using this website you agree to these terms. If you do not agree, please do not use it.</p>"""),
 ("website-use", "Using this website", f"""
<p>You may use this website for lawful purposes only. You must not attempt to gain unauthorised access to the site or its systems, interfere with its operation, introduce malicious code, scrape it in a way that harms performance, or use it to send unlawful or misleading content. We may suspend access to protect the site or others.</p>"""),
 ("ip", "Intellectual property", f"""
<p>The content of this website, including text, design, graphics and code, is owned by or licensed to {N} and protected by intellectual property laws. You may view and share links to pages for personal or internal business use. You may not copy, republish or sell our content without written permission.</p>
<p>Ownership of work we create for you is set out in your proposal or services agreement. Unless stated otherwise there, we may keep our pre-existing tools, templates and methods, and you receive rights to the final deliverables once all fees due have been paid.</p>
{flag("Confirm the intellectual-property position for client work (assignment versus licence, portfolio rights, third-party assets and fonts).")}"""),
 ("services", "Our services", """
<p>Descriptions of services on this website are general. The scope, deliverables, timelines, responsibilities and fees for each project are set out in a written proposal or agreement. We will perform services with reasonable skill and care.</p>
<p><strong>No guaranteed results.</strong> Marketing outcomes depend on many factors outside our control, including competition, market conditions, your offer, your budget and changes made by advertising and search platforms. We do not guarantee rankings, traffic, leads, sales or return on investment.</p>"""),
 ("responsibilities", "Your responsibilities", """
<p>To deliver services well, you agree to provide accurate information, timely feedback, approvals and access to relevant accounts and materials. You are responsible for ensuring you have the right to use any content, images, trademarks or data you give us, and that your products, services and claims comply with the law and with platform rules.</p>"""),
 ("payments", "Fees and payments", f"""
<p>Fees, currency, payment schedule and any deposit are stated in your proposal or invoice. Fees quoted for clients in Pakistan are in Pakistani rupees (₨) unless agreed otherwise. Advertising spend paid to platforms such as Google or Meta is separate from our fees and is paid by you directly to the platform unless the proposal says otherwise. Applicable taxes are added where required. Late payment may result in work being paused. See our <a href="/refund-policy/">Refund Policy</a>.</p>
{flag("Confirm tax treatment (for example sales tax on services and withholding), accepted payment methods, late-payment terms and whether the business invoices foreign clients in other currencies.")}"""),
 ("third-parties", "Third-party services", """
<p>Our work often involves third-party platforms and tools, such as advertising networks, analytics, hosting, payment providers and social networks. These are governed by their own terms and policies, and we are not responsible for their availability, changes or decisions (for example, an ad account suspension or an algorithm change). This website may link to external sites we do not control.</p>"""),
 ("disclaimers", "Disclaimers", """
<p>This website and its content are provided &ldquo;as is&rdquo; for general information and are not professional, legal, tax or financial advice. We try to keep information accurate and current, but do not warrant that it is complete or error-free, or that the site will be uninterrupted.</p>"""),
 ("liability", "Limitation of liability", f"""
<p>To the extent permitted by law, {N} is not liable for indirect or consequential loss, loss of profit, revenue, data or goodwill arising from use of this website or our services. Our total liability for any claim relating to a service is limited to the fees paid for that service in the period set out in the services agreement. Nothing in these terms excludes liability that cannot lawfully be excluded.</p>
{flag("Have a lawyer set the liability cap and exclusions appropriate to the agency's contracts and insurance.")}"""),
 ("termination", "Termination", """
<p>Either party may end a services engagement by written notice as set out in the proposal or agreement. We may suspend or end work if invoices are unpaid, if you ask us to do something unlawful or against platform rules, or if the working relationship becomes unworkable. Fees for work done up to termination remain payable. Provisions that by nature survive termination (such as intellectual property, payment and liability) continue to apply.</p>"""),
 ("governing-law", "Governing law and disputes", f"""
<p>These terms are intended to be governed by the laws of Pakistan, and disputes will be handled by the courts or other forum stated in the services agreement. We encourage you to contact us first so we can try to resolve any concern informally.</p>
{flag("The governing-law, jurisdiction and dispute-resolution (for example arbitration) clause is a default only. The business owner and a Pakistani lawyer must confirm it, particularly for international clients.")}"""),
 ("changes", "Changes to these terms", f"""
<p>We may update these terms from time to time. The revised version applies from the date it is posted. Last updated: {UPD}.</p>"""),
 ("contact", "Contact", f"""
<p>Questions about these terms: <a href="mailto:{EM}">{EM}</a>.</p>"""),
]

REFUND = [
 ("overview", "Overview", f"""
<p>This policy explains how refunds and cancellations work for services bought from {N}. Marketing and creative work is delivered in stages and involves time, expertise and third-party costs, so refunds depend on the type of service and how much work has been done. The specific terms for your project are stated in your proposal; if they differ from this page, the proposal applies.</p>
{flag("This policy needs the owner's decisions on deposits, notice periods, money-back conditions and dispute handling. It is not a statement of consumer-law rights, which cannot be limited by contract. A lawyer should review it against Pakistani consumer and contract law.")}"""),
 ("ad-spend", "Advertising spend", """
<p>Money you pay to advertising platforms such as Google or Meta goes to those platforms. We cannot refund it, and refunds depend on the platform's own policies. Where we place spend on your behalf, the proposal explains how this is handled.</p>"""),
 ("retainers", "Monthly retainers", """
<p>Monthly services are billed in advance or as stated in the proposal. You can cancel by giving written notice as described in your proposal. Work completed and fees for the current period are not refundable once the work for that period has started, except where we have failed to deliver agreed work and cannot put that right.</p>"""),
 ("projects", "Fixed-scope projects", """
<p>Projects such as branding or website design are billed in milestones. A deposit, where charged, reserves our time and starts the work. If you cancel, fees for completed milestones and work already carried out are payable. We will refund any amount paid for work we have not started, less costs we have already incurred with third parties.</p>"""),
 ("our-failure", "If we do not deliver", """
<p>If we fail to deliver work agreed in the proposal, we will first try to correct it within a reasonable time. If we cannot, we will discuss an appropriate remedy with you, which may include a partial or full refund of the fees for the affected work.</p>"""),
 ("not-covered", "What is not refundable", """
<p>We do not refund fees because a campaign or project did not reach a target that was not guaranteed in writing, because market conditions changed, or because a third-party platform changed its rules or restricted an account for reasons outside our control. Delays caused by late approvals, content or access from your side are also not grounds for refund.</p>"""),
 ("how-to-request", "How to request a refund", f"""
<p>Email <a href="mailto:{EM}">{EM}</a> with your invoice number and the reason for your request. We will acknowledge it, review the work delivered and reply in writing. Approved refunds are paid by the original payment method or another agreed method within a reasonable time.</p>
{flag("State the real response and payment times and the payment methods used.", "NEEDS CONFIGURATION")}"""),
 ("updates", "Changes to this policy", f"""<p>We may update this policy. The version in force on the date of your proposal applies to that project. Last updated: {UPD}.</p>"""),
]

COOKIE_BODY_TOP = f"""
{flag("This policy is based on an audit of this demonstration build. Re-run the audit and update this page before launch and whenever tools are added. Legal advice is needed on consent requirements for the countries your visitors are in.")}
"""

COOKIE_SECTIONS = [
 ("what", "What cookies are", """
<p>Cookies are small text files stored on your device by websites. Similar technologies, such as local storage, work in comparable ways. This page explains what this website stores and how you can control it.</p>"""),
 ("audit", "What this website actually uses", """
<p>We audited this website's code. At the time of writing it uses <strong>no cookies</strong> and <strong>no third-party scripts</strong>. Fonts are hosted on our own server, so your browser does not contact a font provider. There are no embedded videos, maps, social feeds or chat widgets.</p>
<div class="table-wrap"><table>
<thead><tr><th scope="col">Item</th><th scope="col">Type</th><th scope="col">Purpose</th><th scope="col">Duration</th></tr></thead>
<tbody>
<tr><td><code>am_cookie_prefs</code></td><td>Local storage (set only if you save preferences below)</td><td>Remembers your cookie choices on this device</td><td>Until you clear your browser data</td></tr>
</tbody></table></div>"""),
 ("categories", "Cookie categories", """
<h3>Necessary</h3><p>Needed for the site to work or to remember your own choices. Do not require consent. None are currently set.</p>
<h3>Analytics</h3><p>Would measure how visitors use the site (for example Google Analytics). <strong>Not in use.</strong> If introduced, they will only run after you opt in.</p>
<h3>Marketing</h3><p>Would be used for advertising and remarketing (for example Meta Pixel or LinkedIn Insight Tag). <strong>Not in use.</strong> If introduced, they will only run after you opt in.</p>
<h3>Third-party</h3><p>Set by external services embedded in pages. <strong>None are used.</strong></p>"""),
 ("consent", "Why there is no cookie banner", """
<p>A consent banner is only needed when optional cookies or trackers are used. Because none are, this demo shows no banner and does not load anything that would need consent. If optional tools are added later, the site should block them until a visitor opts in, with choices that are not pre-selected, as shown in the preferences panel below.</p>
<div class="legal-flag"><strong>LEGAL REVIEW REQUIRED:</strong> Confirm consent obligations for your audience (for example visitors in Pakistan, India and any other regions) before adding analytics or advertising tags.</div>"""),
]

COOKIE_SECTIONS_AFTER = [
 ("manage", "Managing cookies in your browser", """
<p>You can block or delete cookies in your browser settings. Look for &ldquo;Cookies&rdquo; or &ldquo;Site data&rdquo; in the privacy or security section of Chrome, Safari, Firefox, Edge or your mobile browser. Blocking necessary storage may affect parts of a site.</p>"""),
 ("changes", "Changes to this policy", f"""<p>We will update this policy if we add or remove any cookie or tracking technology. Last updated: {UPD}. For how we handle personal information more broadly, see our <a href="/privacy-policy/">Privacy Policy</a>.</p>"""),
]
