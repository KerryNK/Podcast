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

privacy_body = """
<section class="legal-page">
  <div class="wrap">
    <div class="legal-content">
      <h1>Privacy Policy</h1>
      <div class="last-updated">Last Updated: August 2026</div>

      <h2>1. What Information We Collect</h2>
      <p>When you interact with the Kerry Yaps Podcast website, we may collect personal information that you voluntarily provide, such as your name and email address when you subscribe to our "yap collective" mailing list via Typeform.</p>

      <h2>2. How We Use Your Information</h2>
      <p>We use your email address exclusively to send you updates, new episode alerts, and relevant content regarding the Kerry Yaps Podcast. We do not sell, rent, or trade your personal information to third parties.</p>

      <h2>3. Third-Party Services</h2>
      <p>Our website utilizes third-party services, including Spotify (for audio embedding) and Typeform (for email collection). These platforms may use cookies or tracking technologies to collect data about your interaction with their embedded widgets. We encourage you to review the privacy policies of Spotify and Typeform for more information on their data practices.</p>

      <h2>4. Data Security</h2>
      <p>We take reasonable measures to protect the information you provide against unauthorized access. However, please be aware that no data transmission over the internet is 100% secure.</p>

      <h2>5. Contact Us</h2>
      <p>If you have any questions or wish to be removed from our mailing list, please contact us at <a href="mailto:kerryyapspodcast@gmail.com">kerryyapspodcast@gmail.com</a>.</p>
    </div>
  </div>
</section>
"""

terms_body = """
<section class="legal-page">
  <div class="wrap">
    <div class="legal-content">
      <h1>Terms &amp; Conditions</h1>
      <div class="last-updated">Last Updated: August 2026</div>

      <h2>1. Acceptance of Terms</h2>
      <p>By accessing and using <a href="https://kerryyapspodcast.netlify.app/">https://kerryyapspodcast.netlify.app/</a> (the "Website") and listening to the Kerry Yaps Podcast, you agree to be bound by these Terms and Conditions.</p>

      <h2>2. Intellectual Property</h2>
      <p>All content, including but not limited to audio episodes, text, graphics, logos, and the "Big brain energy. Bigger mouth." branding, is the intellectual property of Kerry Namayan and the Kerry Yaps Podcast. You may not reproduce, distribute, or modify any content without explicit written permission.</p>

      <h2>3. Disclaimer of Liability</h2>
      <p>The Kerry Yaps Podcast is a platform for commentary, cultural critique, and personal opinions. The content provided in the audio episodes and on this Website is for entertainment and informational purposes only. It does not constitute professional, legal, or financial advice. The host is not liable for any actions taken based on the opinions expressed on the show.</p>

      <h2>4. User Conduct</h2>
      <p>When interacting with our platforms, you agree not to use the Website or our contact channels for transmitting spam, malicious code, or harassing communication.</p>

      <h2>5. Governing Law</h2>
      <p>These Terms shall be governed by and construed in accordance with the laws of Kenya. Any disputes arising from the use of this Website shall be subject to the exclusive jurisdiction of the courts located in Nairobi.</p>

      <h2>6. Changes to Terms</h2>
      <p>We reserve the right to update or modify these Terms at any time. Continued use of the Website after any changes indicates your acceptance of the new Terms.</p>
    </div>
  </div>
</section>
"""

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

with open("privacy.html", "w") as f:
    f.write(generate_html(privacy_body))

with open("terms.html", "w") as f:
    f.write(generate_html(terms_body))
