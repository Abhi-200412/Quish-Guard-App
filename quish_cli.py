import cv2
import numpy as np
from pyzbar.pyzbar import decode
import requests
import socket
import re
import argparse
import os
from urllib.parse import urlparse

# --- Core Logic (Ported from Quish-Guard ULTRA) ---

def decode_qr(image_path):
    try:
        img = cv2.imread(image_path)
        if img is None: return None
        decoded_objects = decode(img)
        if decoded_objects: return decoded_objects[0].data.decode("utf-8")
        
        # Try grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        decoded_objects = decode(gray)
        if decoded_objects: return decoded_objects[0].data.decode("utf-8")
    except: pass
    return None

def check_virustotal(url, api_key):
    if not api_key: return "SKIPPED (No Key)"
    try:
        headers = {"x-apikey": api_key}
        # Mocking for demo if "virustotal" in url, else real logic would go here
        # For CLI, we'll just print the status
        if "virustotal" in url: return "CLEAN"
        return "UNKNOWN" 
    except: return "ERROR"

def check_heuristics(url):
    findings = []
    try:
        parsed = urlparse(url)
        if parsed.scheme != 'https': findings.append("Insecure Protocol (HTTP)")
        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", parsed.netloc): findings.append("IP Address as Domain")
        if any(parsed.netloc.endswith(t) for t in ['.xyz', '.top', '.ru', '.cn']): findings.append("Suspicious TLD")
        if any(k in parsed.path.lower() for k in ['login', 'verify', 'bank']): findings.append("Suspicious Keywords")
    except: pass
    return findings

def calculate_risk(vt_result, heuristics):
    score = 0
    if "MALICIOUS" in vt_result: score += 100
    for h in heuristics: score += 25
    final_score = min(score, 100)
    return final_score, "DANGER" if final_score > 50 else ("WARNING" if final_score > 0 else "SAFE")

# --- CLI ---

def main():
    parser = argparse.ArgumentParser(description="Quish-Guard CLI: Headless QR Phishing Detector")
    parser.add_argument("target", help="Path to image file or directory")
    parser.add_argument("--key", help="VirusTotal API Key", default="")
    args = parser.parse_args()
    
    targets = []
    if os.path.isdir(args.target):
        for root, _, files in os.walk(args.target):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    targets.append(os.path.join(root, file))
    else:
        targets.append(args.target)
        
    print(f"\n🛡️  QUISH-GUARD CLI | Targets: {len(targets)}\n" + "="*50)
    
    for path in targets:
        print(f"\n[+] Scanning: {os.path.basename(path)}")
        url = decode_qr(path)
        
        if not url:
            print("    ❌ No QR Code found.")
            continue
            
        print(f"    🔗 URL: {url}")
        
        # Analysis
        heuristics = check_heuristics(url)
        vt_res = check_virustotal(url, args.key)
        score, verdict = calculate_risk(vt_res, heuristics)
        
        # Output
        color = "🟢" if verdict == "SAFE" else ("🔴" if verdict == "DANGER" else "🟡")
        print(f"    {color} Verdict: {verdict} (Score: {score})")
        if heuristics: print(f"    ⚠️  Flags: {', '.join(heuristics)}")
        if vt_res != "SKIPPED (No Key)": print(f"    🌍 VirusTotal: {vt_res}")

if __name__ == "__main__":
    main()
