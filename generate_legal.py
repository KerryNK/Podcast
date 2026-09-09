import re

with open("index.html", "r") as f:
    content = f.read()

head_match = re.search(r'(<head>.*?</head>)', content, re.DOTALL)
header_match = re.search(r'(<header.*?</header>)', content, re.DOTALL)
footer_match = re.search(r'(<footer.*?</footer>)', content, re.DOTALL)
script_match = re.search(r'(<script>.*?</script>)', content, re.DOTALL)

head = head_match.group(1) if head_match else ""
# Add some CSS for legal pages
legal_css = """
  .legal-page { padding: 120px 0 60px; min-height: 80vh; }
  .legal-content { max-width: 800px; margin: 0 auto; background: var(--mocha-deep); padding: 40px; border-radius: 12px; }
  .legal-content h1 { font-family: 'Fraunces', serif; font-size: 36px; margin-bottom: 8px; color: var(--gold); }
  .legal-content .last-updated { font-size: 14px; color: var(--cream-dim); margin-bottom: 32px; }
  .legal-content h2 { font-size: 20px; margin: 32px 0 12px; color: var(--cream); font-weight: 600; }
  .legal-content p { line-height: 1.6; color: var(--cream-dim); margin-bottom: 16px; }
  .legal-content a { color: var(--gold); text-decoration: underline; }
"""
head = head.replace('</style>', legal_css + '\n</style>')

header = header_match.group(1) if header_match else ""
# Remove the active state from "Home" link if we want, or just leave it
header = header.replace('href="#about"', 'href="index.html#about"')
header = header.replace('href="#episodes"', 'href="index.html#episodes"')
header = header.replace('href="#subscribe"', 'href="index.html#subscribe"')

footer = footer_match.group(1) if footer_match else ""
footer = footer.replace('href="#" style="margin-right:12px;">Privacy', 'href="privacy.html" style="margin-right:12px;">Privacy')
footer = footer.replace('href="#" style="margin-left:12px;">Terms', 'href="terms.html" style="margin-left:12px;">Terms')

script = script_match.group(1) if script_match else ""

def legal_page(title, date_label, sections):
    section_markup = "\n".join(
        f'<h2>{heading}</h2>\n{content}' for heading, content in sections
    )
    return f"""
<section class="legal-page">
  <div class="wrap">
    <div class="legal-content">
      <h1>{title}</h1>
      <div class="last-updated">{date_label}</div>
      {section_markup}
      <p class="legal-footer">&copy; 2026 Kerry Yaps Podcast<br>Nairobi, Kenya</p>
    </div>
  </div>
</section>
"""

email = '<a href="mailto:kerryyapspodcast@gmail.com">kerryyapspodcast@gmail.com</a>'
privacy_body = legal_page("Privacy Policy", "Last Updated: September 9, 2026", [
    ("1. What Information We Collect", """
      <p>When you interact with the Kerry Yaps Podcast website and related services, we may collect:</p>
      <h3>Information you voluntarily provide</h3>
      <ul><li>Name and email address when you subscribe via Typeform</li><li>Details you include in guest pitches, Yap submissions, or messages</li></ul>
      <h3>Technical information collected automatically</h3>
      <ul><li>IP address, browser type, device information, pages visited (via our hosting provider and analytics tools)</li></ul>
      <p>We do not sell your personal information to third parties.</p>"""),
    ("2. How We Use Your Information", """
      <p>We use your information to:</p>
      <ul><li>Review and respond to guest pitches and Yap submissions</li><li>If you submit a Yap, collect the message, preferred credit name or handle, and optional contact details you provide</li><li>Where you give permission, feature a Yap on the website, social media, show notes, or in podcast discussions</li><li>Send occasional updates, new episode alerts, and relevant content (only if you opt in)</li><li>Improve the Site and podcast, including understanding which pages or episodes are popular</li><li>Prevent abuse and ensure the security of our systems</li></ul>
      <p>Our legal basis under Kenya's <strong>Data Protection Act, 2019</strong> includes your <strong>consent</strong> (for emails and submissions) and <strong>legitimate interests</strong> (for security and improvement of our services).</p>"""),
    ("3. Third-Party Services", """
      <p>Our website and podcast rely on third-party services, which may collect data according to their own policies:</p>
      <ul><li><strong>Spotify</strong> - for audio embedding and distribution</li><li><strong>Typeform</strong> - for email collection and guest pitches</li><li><strong>Hosting/analytics providers</strong> - for site performance and usage data</li></ul>
      <p>We encourage you to review the privacy policies of these providers. We do not control their data practices.</p>"""),
    ("4. Data Retention", """
      <p>We keep your personal information only as long as necessary:</p>
      <ul><li>Email subscribers: until you unsubscribe or request deletion</li><li>Guest pitches and Yaps: typically up to 12 months after last contact, unless you request deletion</li><li>Technical logs: as required for security and analytics (often up to 12 months)</li></ul>"""),
    ("5. Your Rights (Kenya DPA 2019)", f"""
      <p>Under the Data Protection Act, 2019, you have the right to:</p>
      <ul><li>Access your personal data</li><li>Request correction of inaccurate data</li><li>Request deletion of your data</li><li>Object to or restrict certain processing</li><li>Withdraw consent, including unsubscribing from emails</li></ul>
      <p>To exercise any right, email: {email}. We will respond within a reasonable time (typically within 14 days).</p>"""),
    ("6. Data Security", '<p>We take reasonable technical and organizational measures to protect your information against unauthorized access, alteration, or destruction. However, no data transmission over the internet is 100% secure.</p>'),
    ("7. Changes to This Privacy Policy", '<p>We may update this Privacy Policy from time to time. The updated version will be posted on this page with a revised "Last Updated" date.</p>'),
    ("8. Contact", f'<p>If you have any questions or wish to be removed from our mailing list, please contact us at {email}.</p>'),
])

terms_body = legal_page("Terms of Service", "Effective Date: September 9, 2026", [
    ("1. Acceptance of these Terms", '<p>By accessing or using the website, listening to episodes of Kerry Yaps Podcast, submitting a guest pitch, sending a Yap, or otherwise interacting with our content, you agree to be bound by these Terms of Service. If you do not agree, do not use the Site or our content.</p>'),
    ("2. Who we are", '<p>Kerry Yaps Podcast is a podcast hosted by Kerry Namayan in Nairobi, Kenya. The Site and podcast are for informational and entertainment purposes only.</p>'),
    ("3. Intellectual Property", '<p>All content on the Site and in the podcast including episodes, audio, text, graphics, logos, taglines, and artwork is owned by Kerry Yaps Podcast or licensed to us and protected by Kenyan and international copyright and intellectual property laws.</p><p>You may not reproduce, distribute, modify, create derivative works from, publicly display, or use any content for commercial purposes without our prior written permission.</p>'),
    ("4. User-Generated Content (Yaps &amp; Guest Pitches)", '<p>By submitting a Yap, guest pitch, message, or any other content through the Site or forms:</p><ul><li>You grant us a non-exclusive, royalty-free, worldwide license to display, edit (for clarity, length, or format), reproduce, and share your submission on the Site, social media, podcast promotions, or related channels.</li><li>You represent that your submission is original, does not infringe any third-party rights, and is not unlawful, defamatory, harassing, or spam.</li><li>We may reject, edit, or remove any submission at our sole discretion without notice or liability.</li></ul>'),
    ("Yap Wall Submissions", '<p>Yap submissions are not published automatically. We may review, edit for clarity or length, publish with the credit you choose, publish anonymously, decline, or remove a submission at our discretion.</p><p>Do not submit confidential information, personal data about another person without permission, unlawful content, threats, harassment, or content that infringes another person\'s rights. You may request removal of a published Yap by emailing <a href="mailto:kerryyapspodcast@gmail.com">kerryyapspodcast@gmail.com</a> with the relevant page or post link.</p>'),
    ("5. Prohibited Conduct", '<p>You agree not to:</p><ul><li>Use the Site or content for any unlawful purpose</li><li>Attempt to interfere with the Site\'s operation or security</li><li>Impersonate any person or entity</li><li>Submit false, misleading, or offensive content</li><li>Harass, threaten, or abuse others through submissions</li></ul>'),
    ("6. Disclaimer - No Professional Advice", '<p>The Site and podcast episodes are for general informational and entertainment purposes only. Nothing contained in the Site or episodes constitutes professional, financial, legal, career, technical, medical, or any other kind of advice.</p><p>This section is supplemented by our <a href="disclaimer.html">General Disclaimer</a>, which forms part of these Terms.</p>'),
    ("7. Limitation of Liability", '<p>The Site and podcast are provided "as is" and "as available" without warranties of any kind. To the fullest extent permitted by law, Kerry Yaps Podcast shall not be liable for any direct, indirect, incidental, special, consequential, or punitive damages arising from use of or inability to use the Site or podcast, content errors or omissions, unauthorized access, or third-party conduct or content.</p>'),
    ("8. Governing Law", '<p>These Terms are governed by and construed in accordance with the laws of the Republic of Kenya. Any disputes arising from or related to these Terms or the Site shall be resolved exclusively in the courts of Nairobi, Kenya.</p>'),
    ("9. Changes to these Terms", '<p>We may update these Terms from time to time. The updated version will be posted on this page with a revised effective date. Your continued use of the Site after changes constitutes acceptance of the revised Terms.</p>'),
    ("10. Contact", f'<p>If you have any questions about these Terms, please email {email}.</p>'),
])

disclaimer_body = legal_page("General Disclaimer", "Effective Date: September 9, 2026", [
    ("For Informational and Entertainment Purposes Only", '<p>All content provided by Kerry Yaps Podcast including podcast episodes, trailer, website, Yap walls, guest pitches, and any related materials is intended solely for general information and entertainment.</p><p>Nothing on the Site, in the Podcast, or in any associated communications constitutes professional advice of any kind, including career, professional, business, financial, investment, legal, technical, health, medical, or psychological advice.</p><p>Always consult qualified professionals before making decisions that affect your life, career, finances, health, or legal position.</p>'),
    ("Opinions &amp; Statements", '<p>The views, opinions, stories, and statements expressed by the host (Kerry Namayan) and any guests are their own personal views and do not necessarily reflect the official policy, position, or endorsement of any organization, employer, affiliate, sponsor, or third party.</p>'),
    ("No Guarantee of Accuracy or Completeness", '<p>While we strive to provide accurate and up-to-date information, we make no representations or warranties of any kind regarding the accuracy, completeness, timeliness, reliability, or usefulness of any content. The Podcast and Site may contain errors or omissions.</p>'),
    ("External Links &amp; Third-Party Content", '<p>The Site and Podcast may contain links to external websites, platforms (e.g., Spotify, YouTube, Riverside.fm), or third-party content. We do not control, endorse, or assume responsibility for the accuracy, privacy practices, availability, or content of those external sites or services.</p>'),
    ("No Liability", '<p>To the fullest extent permitted by law, Kerry Yaps Podcast, Kerry Namayan, and any affiliates disclaim all liability for any loss, damage, or injury arising from the use of or reliance on any content provided through the Podcast or Site.</p>'),
    ("Governing Law", '<p>This Disclaimer is governed by the laws of the Republic of Kenya.</p>'),
    ("Contact", f'<p>For any questions regarding this Disclaimer, email {email}.</p>'),
])

dmca_body = legal_page("DMCA / Copyright Infringement Notice", "Effective Date: September 9, 2026", [
    ("Notice", '<p>Kerry Yaps Podcast respects the intellectual property rights of others and expects the same from our users, guests, and visitors. We comply with the Digital Millennium Copyright Act (DMCA) and other applicable copyright laws.</p><p>If you believe that any content on our website, podcast episodes, social media posts, or other materials infringes your copyright, please send a written DMCA takedown notice to our designated agent.</p>'),
    ("Designated Copyright Agent", f'<p>Name: Kerry Namayan<br>Email: {email}<br>Subject line: "DMCA Takedown Notice"</p>'),
    ("Required Information in Your Notice", '<p>To be effective, your notice must include all of the following:</p><ol><li>A physical or electronic signature of the copyright owner or an authorized representative.</li><li>Identification of the copyrighted work claimed to have been infringed.</li><li>Identification of the allegedly infringing material, including its exact URL or location.</li><li>Your contact information (name, address, telephone number, and email address).</li><li>A good-faith belief that the use is not authorized by the copyright owner, its agent, or the law.</li><li>A statement under penalty of perjury that the information is accurate and that you are authorized to act.</li></ol>'),
    ("What Happens Next", '<ul><li>We will expeditiously remove or disable access to the allegedly infringing material.</li><li>We may notify the user who posted the material and provide an opportunity to submit a counter-notice.</li><li>We may forward your notice to the alleged infringer if required.</li></ul>'),
    ("Counter-Notice", '<p>If your content was removed and you believe it was removed in error, you may submit a counter-notice following DMCA rules. We will forward it to the complainant and may restore the content after 10-14 business days unless the complainant files a court action.</p>'),
    ("Repeat Infringers", '<p>We reserve the right to terminate access to our services for users who are repeat infringers in appropriate circumstances.</p>'),
    ("Contact", f'<p>All DMCA notices and counter-notices should be sent only to {email}. Do not send general inquiries to this address.</p><p>This notice complies with the requirements of 17 U.S.C. section 512(c)(3). Submitting a false or bad-faith notice may result in liability under applicable law.</p>'),
])

def generate_html(body_content):
    return f"""<!DOCTYPE html>
<html lang="en">
{head}
<body>
{header}
{body_content}
{footer}
{script}
</body>
</html>
"""

for filename, body in {
  "privacy.html": privacy_body,
  "terms.html": terms_body,
  "disclaimer.html": disclaimer_body,
  "dmca.html": dmca_body,
}.items():
  with open(filename, "w") as f:
    f.write(generate_html(body))
