import qrcode
import os
import shutil

base_dir = "samples"

# 1. Cleanup Old Samples
if os.path.exists(base_dir):
    shutil.rmtree(base_dir)
    print(f"Deleted old {base_dir} directory.")

# 2. Setup Directories
categories = ["normal", "suspicious", "payloads"]
for cat in categories:
    os.makedirs(os.path.join(base_dir, cat), exist_ok=True)

def generate(data, filename, category):
    img = qrcode.make(data)
    path = os.path.join(base_dir, category, filename)
    img.save(path)
    print(f"Generated [{category}]: {filename}")

# --- A. Normal Samples (Safe Sites) ---
normal_samples = [
    ("https://www.google.com", "google.png"),
    ("https://www.wikipedia.org", "wikipedia.png"),
    ("https://github.com", "github.png"),
    ("https://www.openai.com", "openai.png"),
    ("https://www.stackoverflow.com", "stackoverflow.png"),
    ("https://www.reddit.com", "reddit.png"),
    ("https://www.amazon.com", "amazon.png"),
    ("https://www.microsoft.com", "microsoft.png"),
]
# Generate 50 extra normal samples
for i in range(1, 51):
    normal_samples.append((f"https://www.example-site-{i}.com/page/{i}", f"normal_random_{i}.png"))

for data, name in normal_samples: generate(data, name, "normal")

# --- B. Suspicious Samples (Phishing/Malware) ---
suspicious_samples = [
    # 1. URL Shorteners (Redirects)
    ("http://bit.ly/3xyz123", "redirect_bitly.png"),
    ("https://t.co/abcdefg", "redirect_twitter.png"),
    
    # 2. Insecure / IP
    ("http://192.168.1.55/admin", "ip_address_local.png"),
    ("http://104.21.55.2/login.php", "ip_address_public.png"),
    ("http://insecure-bank-login.com", "insecure_http.png"),
    
    # 3. Typosquatting / Suspicious TLDs
    ("https://www.g0ogle.com", "typosquat_google.png"),
    ("https://update-security.xyz", "tld_xyz_malware.png"),
    ("https://free-crypto.top/claim", "tld_top_scam.png"),
    # 4. Homoglyphs (Punycode)
    ("http://xn--80ak6aa92e.com", "punycode_apple.png"), 
]

# Generate 50 extra phishing samples
for i in range(1, 51):
    suspicious_samples.append((f"http://secure-login-attempt-{i}.xyz/verify", f"phishing_random_{i}.png"))

for data, name in suspicious_samples: generate(data, name, "suspicious")

# --- C. Non-Web Payloads (Forensic Tests) ---
payload_samples = [
    ("WIFI:S:Free_Public_WiFi;T:WPA;P:Password123;;", "wifi_connect.png"),
    ("SMSTO:12345:SUBSCRIBE NOW", "sms_subscribe.png"),
    ("TEL:+15550009999", "call_support.png"),
    ("""BEGIN:VCARD
VERSION:3.0
N:Doe;John;;;
FN:John Doe
ORG:ACME Corp.
TEL;TYPE=CELL:123456789
EMAIL:john.doe@example.com
END:VCARD""", "vcard_contact.png"),
    ("GEO:40.712776,-74.005974", "geo_newyork.png"),
    ("MATMSG:TO:support@bank.com;SUB:Reset Password;BODY:I need help;;", "email_support.png")
]

# Generate 20 random Wi-Fi samples
for i in range(1, 21):
    payload_samples.append((f"WIFI:S:Guest_Network_{i};T:WPA;P:secret{i};;", f"wifi_random_{i}.png"))

for data, name in payload_samples: generate(data, name, "payloads")

print(f"\n✅ Successfully generated {len(normal_samples) + len(suspicious_samples) + len(payload_samples)} samples in '{base_dir}/'")
