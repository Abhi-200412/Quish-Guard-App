import qrcode
import os
import shutil

base_dir = "samples"
normal_dir = os.path.join(base_dir, "normal")
suspicious_dir = os.path.join(base_dir, "suspicious")

# Ensure directories exist
if not os.path.exists(normal_dir):
    os.makedirs(normal_dir)
if not os.path.exists(suspicious_dir):
    os.makedirs(suspicious_dir)

def generate(url, filename, category):
    img = qrcode.make(url)
    path = os.path.join(base_dir, category, filename)
    img.save(path)
    print(f"Generated: {path}")

# --- Normal Samples ---
normal_urls = [
    ("https://www.google.com", "google.png"),
    ("https://www.wikipedia.org", "wikipedia.png"),
    ("https://github.com", "github.png"),
    ("https://www.linkedin.com", "linkedin.png"),
    ("https://www.python.org", "python.png"),
] + [
    (f"https://www.google.com/search?q={i}", f"google_{i}.png") for i in range(95)
]

for url, name in normal_urls:
    generate(url, name, "normal")

# --- Suspicious Samples ---
suspicious_urls = [
    ("http://bit.ly/3xyz123", "shortener_bitly.png"),
    ("https://www.g0ogle.com", "typosquat_google.png"),
    ("http://secure-login-update.com", "phishing_login.png"),
    ("http://192.168.1.1/admin", "ip_address_admin.png"),
    ("https://paypal-verify-account.com", "typosquat_paypal.png"),
    ("http://xn--80ak6aa92e.com", "punycode_apple.png"),
    ("http://free-iphone-giveaway.net", "scam_giveaway.png"),
] + [
    (f"http://suspicious-bank-login-{i}.xyz", f"phishing_{i}.png") for i in range(93)
]

for url, name in suspicious_urls:
    generate(url, name, "suspicious")

print("Categorized samples generated successfully.")
