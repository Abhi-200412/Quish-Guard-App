import streamlit as st
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import requests
import whois
import ssl
import socket
import datetime
import re
import json
import random
import asyncio
from urllib.parse import urlparse
from streamlit_lottie import st_lottie
import pandas as pd
import os
import time

# --- Configuration & Theme ---
st.set_page_config(
    page_title="Quish-Guard ULTRA",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Cyber-Warfare Theme (Premium Glassmorphism)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;600&display=swap');
    
    /* GLOBAL RESET & SCROLLBAR */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #020202; }
    ::-webkit-scrollbar-thumb { background: #00f0ff; border-radius: 4px; }
    
    .stApp {
        background: radial-gradient(circle at top, #1a0b2e 0%, #000000 70%);
        color: #e0e0e0;
        font-family: 'Inter', sans-serif;
    }
    
    /* NEON HEADERS */
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        background: linear-gradient(90deg, #fff, #00f0ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(0, 240, 255, 0.4);
    }
    
    /* GLASSMORPHISM CARDS */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    .glass-card:hover {
        border-color: rgba(0, 240, 255, 0.3);
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.1);
        transform: translateY(-2px);
    }
    
    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background: rgba(5, 5, 10, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* CUSTOM BUTTONS */
    .stButton>button {
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.1), rgba(0, 100, 255, 0.1));
        border: 1px solid rgba(0, 240, 255, 0.3);
        color: #00f0ff;
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 1px;
        border-radius: 8px;
        backdrop-filter: blur(4px);
        text-transform: uppercase;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #00f0ff, #0066ff);
        color: #000;
        box-shadow: 0 0 25px rgba(0, 240, 255, 0.4);
        border-color: transparent;
    }
    
    /* METRICS */
    [data-testid="stMetricValue"] {
        font-family: 'Orbitron', sans-serif;
        color: #fff !important;
        text-shadow: 0 0 10px rgba(255,255,255,0.3);
    }
    
    /* ANIMATED SCANNER BORDER */
    .scanner-container {
        position: relative;
        border: 2px solid #00f0ff;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.2);
    }
    .scan-line {
        position: absolute;
        width: 100%;
        height: 4px;
        background: #00f0ff;
        box-shadow: 0 0 15px #00f0ff;
        animation: scan 2s linear infinite;
        z-index: 10;
        opacity: 0.7;
    }
    @keyframes scan {
        0% { top: 0%; }
        50% { top: 90%; opacity: 0; }
        51% { top: 0%; opacity: 0; }
        100% { top: 0%; opacity: 0.7; }
    }
    
    /* VERDICT BADGES */
    .verdict-badge {
        font-family: 'Orbitron', sans-serif;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        font-weight: 900;
        font-size: 2em;
        letter-spacing: 3px;
    }
    .v-safe {
        background: linear-gradient(90deg, rgba(0,255,0,0.1), transparent);
        border-left: 5px solid #00ff00;
        color: #00ff00;
        text-shadow: 0 0 15px rgba(0,255,0,0.4);
    }
    .v-danger {
        background: linear-gradient(90deg, rgba(255,0,0,0.1), transparent);
        border-left: 5px solid #ff0000;
        color: #ff0000;
        text-shadow: 0 0 15px rgba(255,0,0,0.4);
        animation: danger-pulse 1.5s infinite;
    }
    @keyframes danger-pulse {
        0% { box-shadow: 0 0 10px rgba(255,0,0,0.1); }
        50% { box-shadow: 0 0 30px rgba(255,0,0,0.3); }
        100% { box-shadow: 0 0 10px rgba(255,0,0,0.1); }
    }
    
    /* REDIRECT FLOW */
    .redirect-flow {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
        background: rgba(0,0,0,0.3);
        padding: 15px;
        border-radius: 12px;
        border: 1px dashed #444;
    }
    .flow-node {
        background: rgba(255,255,255,0.05);
        padding: 8px 12px;
        border-radius: 6px;
        font-family: 'Consolas', monospace;
        font-size: 0.85em;
        color: #aaa;
    }
    .flow-final {
        background: rgba(0, 240, 255, 0.1);
        border: 1px solid rgba(0, 240, 255, 0.3);
        color: #00f0ff;
        font-weight: bold;
    }
    /* ANIMATED BACKGROUND */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; 
        left: 0;
        width: 100%; 
        height: 100%;
        background: 
            linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%),
            linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
        background-size: 100% 2px, 3px 100%;
        z-index: -1;
        pointer-events: none;
    }
    .background-grid {
        position: fixed;
        top: 0; left: 0; width: 200%; height: 200%;
        background-image: 
            linear-gradient(rgba(0, 240, 255, 0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 240, 255, 0.1) 1px, transparent 1px);
        background-size: 40px 40px;
        transform: perspective(500px) rotateX(60deg) translateY(-100px) translateZ(-200px);
        animation: grid-move 20s linear infinite;
        z-index: -2;
        pointer-events: none;
    }
    @keyframes grid-move {
        0% { transform: perspective(500px) rotateX(60deg) translateY(0) translateZ(-200px); }
        100% { transform: perspective(500px) rotateX(60deg) translateY(40px) translateZ(-200px); }
    }

    /* FOOTER */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: rgba(0, 0, 0, 0.8);
        border-top: 1px solid #333;
        color: #555;
        text-align: center;
        padding: 5px;
        font-family: 'Consolas', monospace;
        font-size: 0.7em;
        z-index: 100;
    }
    </style>
    
    <!-- BACKGROUND GRID -->
    <div class="background-grid"></div>
    <div class="footer">QUISH-GUARD ULTRA // SYSTEM v2.4 // UNCLASSIFIED</div>
    """, unsafe_allow_html=True)

# --- Assets (Lottie) ---
@st.cache_data
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

LOTTIE_SCAN = load_lottieurl("https://lottie.host/5a88c703-d63f-4209-8466-932641753140/9Qyq5Z5Z5Z.json")
LOTTIE_SAFE = load_lottieurl("https://lottie.host/96813451-0367-4286-8805-481971775791/0000000000.json")
LOTTIE_DANGER = load_lottieurl("https://lottie.host/38513451-0367-4286-8805-481971775791/0000000000.json")

# --- Backend Logic ---

@st.cache_data(show_spinner=False)
def decode_qr_from_bytes(image_bytes):
    try:
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        decoded_objects = decode(img)
        if decoded_objects: return decoded_objects[0], img.shape
    except: pass
    return None, None

def detect_qr_robust(frame):
    """
    Multi-stage detection pipeline for challenging conditions.
    """
    # 1. Standard Decode
    objs = decode(frame)
    if objs: return objs
    
    # Pre-processing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 2. Grayscale
    objs = decode(gray)
    if objs: return objs
    
    # 3. CLAHE (Contrast Limited Adaptive Histogram Equalization) - For Low Light
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    objs = decode(enhanced)
    if objs: return objs
    
    # 4. Gaussian Blur - For Noise/Grain
    blurred = cv2.GaussianBlur(gray, (5,5), 0)
    objs = decode(blurred)
    if objs: return objs
    
    # 5. Otsu's Thresholding - For High Contrast/Binary
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    objs = decode(thresh)
    if objs: return objs
    
    return []

def simulate_decryption():
    """Renders a cool 'Hacking' text animation."""
    status_text = st.empty()
    bar = st.progress(0)
    
    steps = [
        "🔵 ESTABLISHING SECURE CONNECTION...",
        "🔵 BYPASSING FIREWALL...",
        "🟡 DECODING PACKET STREAM...",
        "🟡 ANALYZING HEURISTIC SIGNATURES...",
        "🔴 QUERYING THREAT INTELLIGENCE...",
        "🟢 ACCESS GRANTED. SIGNAL DECRYPTED."
    ]
    
    for i, step in enumerate(steps):
        status_text.markdown(f"### `{step}`")
        # Ensure we don't exceed 100
        progress = min((i + 1) * 17, 100)
        bar.progress(progress)
        time.sleep(0.3)
    
    time.sleep(0.5)
    status_text.empty()
    bar.empty()

def check_virustotal(url, api_key):
    if not api_key: return None
    try:
        headers = {"x-apikey": api_key}
        # Mocking actual call for speed/demo reliability unless key provided
        if "virustotal" in url: return "CLEAN"
        return "UNKNOWN" 
    except: return "ERROR"

def trace_redirects(url):
    """Follows redirects to find the final destination."""
    try:
        # User-Agent to avoid being blocked by some sites
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.head(url, allow_redirects=True, timeout=5, headers=headers)
        if response.history:
            return response.url, True, len(response.history)
        return url, False, 0
    except:
        return url, False, 0

def check_domain_age(url):
    """Checks the creation date of the domain using Whois."""
    try:
        domain = urlparse(url).netloc
        if not domain: return None, "Invalid Domain"
        
        w = whois.whois(domain)
        creation_date = w.creation_date
        
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
            
        if creation_date:
            now = datetime.datetime.now()
            age = now - creation_date
            return age.days, creation_date.strftime('%Y-%m-%d')
        return None, "Unknown"
    except:
        return None, "Whois Error"

def get_payload_type(text):
    """Identifies non-URL payloads."""
    text = text.upper()
    if text.startswith("WIFI:"): return "WIFI_CONFIG"
    if text.startswith("SMSTO:"): return "SMS_SEND"
    if text.startswith("TEL:"): return "CALL_NUMBER"
    if text.startswith("MATMSG:"): return "EMAIL_SEND"
    if text.startswith("VCARD:") or text.startswith("BEGIN:VCARD"): return "CONTACT_CARD"
    if text.startswith("GEO:"): return "LOCATION"
    if text.startswith("GEO:"): return "LOCATION"
    return "URL"

def get_payload_icon(p_type):
    if p_type == "WIFI_CONFIG": return "📶"
    if p_type == "SMS_SEND": return "💬"
    if p_type == "CALL_NUMBER": return "📞"
    if p_type == "EMAIL_SEND": return "📧"
    if p_type == "CONTACT_CARD": return "📇"
    if p_type == "LOCATION": return "📍"
    return "🔗"

def load_history():
    if os.path.exists("history.json"):
        with open("history.json", "r") as f:
            try: return json.load(f)
            except: return []
    return []

def save_history(entry):
    hist = load_history()
    hist.append(entry)
    # Keep last 50
    if len(hist) > 50: hist = hist[-50:]
    with open("history.json", "w") as f:
        json.dump(hist, f)
    return hist

def check_heuristics_enhanced(url, final_url, domain_age_days, payload_type):
    findings = []
    
    # 1. Payload Check
    if payload_type != "URL":
        findings.append(f"Non-Web Payload: {payload_type}")
        return findings # Skip URL checks for non-URLs
        
    try:
        # 2. Redirect Check
        if url != final_url:
            findings.append("Hidden Redirect Detected")
            
        # 3. Domain Age Check
        if domain_age_days is not None and domain_age_days < 30:
            findings.append(f"New Domain ({domain_age_days} days old)")
            
        parsed = urlparse(final_url) # Analyze the FINAL url
        if parsed.scheme != 'https': findings.append("Insecure Protocol (HTTP)")
        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", parsed.netloc): findings.append("IP Address as Domain")
        if any(parsed.netloc.endswith(t) for t in ['.xyz', '.top', '.ru', '.cn']): findings.append("Suspicious TLD")
        if any(k in parsed.path.lower() for k in ['login', 'verify', 'bank']): findings.append("Suspicious Keywords")
    except: pass
    return findings



def generate_ai_insight(url, score, heuristics):
    """Generates a natural language explanation of the threat."""
    insight = f"**Analysis for {url}:**\n\n"
    if score > 50:
        insight += "⚠️ **CRITICAL THREAT DETECTED.**\n"
        insight += "This URL exhibits multiple high-risk indicators. "
        if "IP Address" in str(heuristics): insight += "It uses a raw IP address, which is a common tactic to bypass domain filters. "
        if "HTTP" in str(heuristics): insight += "The connection is unencrypted (HTTP), putting your data at risk. "
        if "New Domain" in str(heuristics): insight += "The domain was registered very recently (less than 30 days ago), which is a huge red flag for phishing. "
        if "Redirect" in str(heuristics): insight += "The identifier uses a redirect to hide the true destination. "
        if "Non-Web Payload" in str(heuristics): insight += "This code triggers a system action (WiFi/SMS/Call) which can be dangerous if not verified. "
        insight += "\n\n**RECOMMENDATION:** DO NOT OPEN/EXECUTE THIS LINK."
    elif score > 0:
        insight += "⚠️ **POTENTIAL RISK.**\n"
        insight += "While not confirmed malicious, this link has suspicious traits. Proceed with extreme caution."
    else:
        insight += "✅ **NO THREATS FOUND.**\n"
        insight += "The URL appears legitimate and uses standard security protocols."
    return insight

def calculate_risk(vt_result, heuristics):
    score = 0
    if vt_result and "MALICIOUS" in vt_result: score += 100
    
    # Weighted Heuristics
    for h in heuristics:
        if "New Domain" in h: score += 75
        elif "Redirect" in h: score += 50
        elif "IP Address" in h: score += 60
        elif "Non-Web Payload" in h: score += 40
        else: score += 25
        
    final_score = min(score, 100)
    return final_score, "DANGER" if final_score > 50 else ("WARNING" if final_score > 0 else "SAFE")

def render_landing_page():
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        # Glitch/Neon Title
        st.markdown("""
        <div style="text-align: center;">
            <h1 style="font-size: 5em; margin-bottom: 0;">QUISH-GUARD</h1>
            <h3 style="letter-spacing: 8px; color: #aaa !important; margin-top: -20px;">ULTRA FORENSICS</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if LOTTIE_SCAN:
            st_lottie(LOTTIE_SCAN, height=350, key="landing_anim")
        else:
            st.markdown("<div style='text-align:center; font-size: 6em; margin: 30px;'>🛡️</div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 INITIATE SYSTEM", type="primary", use_container_width=True):
            st.session_state.page = "Dashboard"
            st.rerun()

def render_dashboard(use_mock, vt_api_key):
    # Sidebar
    with st.sidebar:
        st.title("COMMAND CENTER")
        if st.button("⬅️ EXIT SYSTEM"):
            st.session_state.page = "Landing"
            st.rerun()
        st.divider()
        st.metric("System Status", "ONLINE", delta="SECURE")
        
        # Session History
        st.divider()
        st.markdown("### 📜 MISSION LOG")
        
        # Load persistent history
        if 'history' not in st.session_state: 
            st.session_state.history = load_history()
        
        if not st.session_state.history:
            st.caption("No targets analyzed yet.")
        if not st.session_state.history:
            st.caption("No targets analyzed yet.")
        else:
            for i, item in enumerate(reversed(st.session_state.history[-5:])): # Show last 5
                icon = "🟢" if item['level'] == "SAFE" else "🔴"
                with st.expander(f"{icon} {item['time']}"):
                     st.caption(f"Score: {item['score']}")
                     st.code(item['url'], language=None)

    st.title("🛡️ Forensic Console")
    
    # Layout
    col_input, col_logs, col_verdict = st.columns([1.2, 1.5, 1.3])
    
    # 1. Input Section
    with col_input:
        st.markdown("### 📡 Target Acquisition")
        
        # Reset Button (only if we have a result)
        if 'result' in st.session_state:
            if st.button("🔄 SCAN ANOTHER TARGET", type="primary", use_container_width=True):
                del st.session_state.result
                del st.session_state.decoded_url
                st.session_state.scanning_active = True
                st.rerun()
        
        tab1, tab2 = st.tabs(["📷 Scanner", "📁 Upload"])
        
        with tab1:
            if 'scanning_active' not in st.session_state: st.session_state.scanning_active = False
            
            # Only show start/stop if not already analyzed
            if 'result' not in st.session_state:
                c1, c2 = st.columns(2)
                if c1.button("▶ START", use_container_width=True):
                    # Boot Sequence
                    with st.status("INITIALIZING OPTICAL SENSORS...", expanded=True) as status:
                        st.write("Checking camera permissions...")
                        time.sleep(0.5)
                        st.write("Loading heuristic database...")
                        time.sleep(0.5)
                        st.write("Calibrating lenses...")
                        time.sleep(0.5)
                        status.update(label="SYSTEM READY", state="complete", expanded=False)
                    
                    st.session_state.scanning_active = True
                    st.rerun()
                if c2.button("⏹ STOP", use_container_width=True):
                    st.session_state.scanning_active = False
                    st.rerun()
                    
                if st.session_state.scanning_active:
                    # Scanner Container with Animation
                    st.markdown('<div class="scanner-container"><div class="scan-line"></div>', unsafe_allow_html=True)
                    placeholder = st.empty()
                    
                    cap = cv2.VideoCapture(0)
                    
                    def draw_hud(frame, target_found=False):
                        h, w, _ = frame.shape
                        color = (0, 255, 0) if target_found else (0, 240, 255) # Green vs Cyan
                        
                        # Corners
                        l = 30
                        t = 4
                        # Top Left
                        cv2.line(frame, (w//2-100, h//2-100), (w//2-100+l, h//2-100), color, t)
                        cv2.line(frame, (w//2-100, h//2-100), (w//2-100, h//2-100+l), color, t)
                        # Top Right
                        cv2.line(frame, (w//2+100, h//2-100), (w//2+100-l, h//2-100), color, t)
                        cv2.line(frame, (w//2+100, h//2-100), (w//2+100, h//2-100+l), color, t)
                        # Bottom Left
                        cv2.line(frame, (w//2-100, h//2+100), (w//2-100+l, h//2+100), color, t)
                        cv2.line(frame, (w//2-100, h//2+100), (w//2-100, h//2+100-l), color, t)
                        # Bottom Right
                        cv2.line(frame, (w//2+100, h//2+100), (w//2+100-l, h//2+100), color, t)
                        cv2.line(frame, (w//2+100, h//2+100), (w//2+100, h//2+100-l), color, t)
                        
                        # Text
                        status = "TARGET LOCKED" if target_found else "SEARCHING..."
                        cv2.putText(frame, status, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                        
                        # REC Blinker (Simulated by seconds)
                        if int(time.time() * 2) % 2 == 0:
                            cv2.circle(frame, (w-30, 30), 10, (0, 0, 255), -1)
                            cv2.putText(frame, "REC", (w-80, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                            
                        return frame

                    while st.session_state.scanning_active:
                        ret, frame = cap.read()
                        if not ret: break
                        
                        # Robust Detection Pipeline
                        decoded_objects = detect_qr_robust(frame)
                        
                        # HUD Overlay
                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        
                        if decoded_objects:
                            frame_rgb = draw_hud(frame_rgb, target_found=True)
                            obj = decoded_objects[0]
                            decoded_text = obj.data.decode("utf-8")
                            
                            # Store Metadata
                            st.session_state.qr_meta = {
                                "type": obj.type,
                                "size": f"{obj.rect.width}x{obj.rect.height} px",
                                "raw_len": len(decoded_text)
                            }
                            
                            # Draw Lock Box
                            pts = np.array([obj.polygon], np.int32)
                            pts = pts.reshape((-1,1,2))
                            cv2.polylines(frame_rgb, [pts], True, (0, 255, 0), 3)
                            
                            st.session_state.decoded_url = decoded_text
                            st.session_state.analysis_triggered = True # Auto-trigger for scanner
                            st.session_state.scanning_active = False
                            
                            # Show final frame briefly
                            placeholder.image(frame_rgb, channels="RGB")
                            time.sleep(0.5)
                            
                            cap.release()
                            st.rerun()
                        else:
                            frame_rgb = draw_hud(frame_rgb, target_found=False)
                            placeholder.image(frame_rgb, channels="RGB")
                            
                    cap.release()

        with tab2:
            if 'uploader_key' not in st.session_state: st.session_state.uploader_key = 0
            f = st.file_uploader("Upload Image", type=['png', 'jpg'], key=f"uploader_{st.session_state.uploader_key}")
            if f: 
                obj, shape = decode_qr_from_bytes(f.getvalue())
                if obj: 
                    val = obj.data.decode("utf-8")
                    # Only update if it's a new file/url to avoid resetting state on rerun
                    if st.session_state.get('decoded_url') != val:
                        st.session_state.decoded_url = val
                        st.session_state.qr_meta = {
                            "type": obj.type, 
                            "size": f"{obj.rect.width}x{obj.rect.height} px (Img: {shape[1]}x{shape[0]})", 
                            "raw_len": len(val)
                        }
                        st.session_state.analysis_triggered = False # Manual trigger for upload
                        if 'result' in st.session_state: del st.session_state.result

    # 2. Analysis & Logs (Auto-Run)
    with col_logs:
        st.markdown("### 💻 System Logs")
        logs_ph = st.empty()
        
        if 'decoded_url' in st.session_state and st.session_state.decoded_url:
            raw_text = st.session_state.decoded_url
            
            # Check if analysis is triggered
            if not st.session_state.get('analysis_triggered', False):
                st.info(f"Target Loaded: {raw_text}")
                st.write(f"Metadata: {st.session_state.get('qr_meta', 'N/A')}")
                if st.button("⚡ START ANALYIS", type="primary", use_container_width=True):
                    st.session_state.analysis_triggered = True
                    st.rerun()
            
            # Auto-Analyze if triggered and no result yet
            elif 'result' not in st.session_state:
                
                # Perform Analysis steps first
                with logs_ph.container():
                     simulate_decryption()
                
                p_type = get_payload_type(raw_text)
                final_url = raw_text
                domain_age = None
                created_date_str = "N/A"
                redirected = False
                hops = 0
                
                if p_type == "URL":
                    final_url, redirected, hops = trace_redirects(raw_text)
                    domain_age, created_date_str = check_domain_age(final_url)
                
                heuristics = check_heuristics_enhanced(raw_text, final_url, domain_age, p_type)
                if use_mock and "evil" in raw_text: heuristics.append("Suspicious Keywords")
                
                vt_res = check_virustotal(final_url, vt_api_key)
                if use_mock and "evil" in raw_text: vt_res = "MALICIOUS"
                
                # --- VISUAL DASHBOARD (Glassmorphism) ---
                with logs_ph.container():
                     st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                     st.markdown("### 📊 SIGNAL ANALYSIS")
                     # Top Metrics
                     m1, m2, m3 = st.columns(3)
                     m1.metric("Payload Type", p_type.replace("_", " "), get_payload_icon(p_type))
                    
                     age_delta = "Unknown"
                     if domain_age:
                        age_delta = f"{domain_age} days"
                        m2.metric("Domain Age", age_delta, delta="-New" if domain_age < 30 else "+Established", delta_color="inverse")
                     else:
                        m2.metric("Domain Age", "N/A")
                        
                     m3.metric("Redirect Hops", hops, delta="Direct" if hops==0 else f"{hops} Redirects", delta_color="inverse")
                    
                     st.divider()
                    
                     # Redirect Flow
                     if redirected:
                         st.markdown(f"""
                         <div class="redirect-flow">
                            <div class="flow-node">ORIGIN<br>{raw_text[:20]}...</div>
                            <div style="color:#666">➜</div>
                            <div class="flow-node flow-final">DESTINATION<br>{final_url[:30]}...</div>
                         </div>
                         """, unsafe_allow_html=True)
                     else:
                         st.code(raw_text, language=None)
                    
                     st.divider()
                    
                     # Logs
                     st.caption("FORENSIC LOGS")
                     if heuristics:
                        for h in heuristics: st.markdown(f"🚫 **FLAG:** {h}")
                     else:
                        st.markdown("✅ *No anomaly signatures detected.*")
                        
                     st.markdown('</div>', unsafe_allow_html=True)

                score, level = calculate_risk(vt_res, heuristics)
                insight = generate_ai_insight(final_url, score, heuristics)
                
                # Save to History (Persistent)
                entry = {
                    "url": raw_text,
                    "final_url": final_url,
                    "type": p_type,
                    "level": level,
                    "score": score,
                    "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                updated_history = save_history(entry)
                st.session_state.history = updated_history
                
                st.session_state.result = {
                    "score": score, "level": level, "insight": insight, 
                    "url": final_url, "original_url": raw_text
                }
                st.rerun() # Rerun to show verdict immediately
            
            else:
                # Show static logs if result exists
                with logs_ph.container():
                    st.markdown('<div class="log-box">', unsafe_allow_html=True)
                    st.write(f"> Target: {st.session_state.result['url']}")
                    st.write("> Analysis Completed Successfully.")
                    st.write("> See Intelligence Report for details.")
                    st.markdown('</div>', unsafe_allow_html=True)

    # 3. Verdict & Features
    with col_verdict:
        st.markdown("### 🛡️ Intelligence Report")
        verdict_ph = st.empty()
        
        if 'result' in st.session_state:
            res = st.session_state.result
            
            with verdict_ph.container():
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                
                # Verdict Animation
                if res['level'] == "SAFE":
                    if LOTTIE_SAFE:
                        st_lottie(LOTTIE_SAFE, height=150, key="safe_anim")
                    else:
                        st.markdown("<div style='text-align:center; font-size: 3em;'>✅</div>", unsafe_allow_html=True)
                    st.markdown(f'<div class="verdict-badge v-safe">SAFE<br><span style="font-size:0.4em">Score: {res["score"]}</span></div>', unsafe_allow_html=True)
                else:
                    if LOTTIE_DANGER:
                        st_lottie(LOTTIE_DANGER, height=150, key="danger_anim")
                    else:
                        st.markdown("<div style='text-align:center; font-size: 3em;'>🚨</div>", unsafe_allow_html=True)
                    st.markdown(f'<div class="verdict-badge v-danger">THREAT<br><span style="font-size:0.4em">Score: {res["score"]}</span></div>', unsafe_allow_html=True)
                
                # AI Insight
                with st.expander("🤖 AI Threat Insight", expanded=True):
                    st.write(res['insight'])
                
                st.markdown('</div>', unsafe_allow_html=True)

                
                report_text = f"QUISH-GUARD FORENSIC REPORT\n\nTarget: {res['url']}\nVerdict: {res['level']}\nScore: {res['score']}\n\nInsight:\n{res['insight']}"
                st.download_button("⬇️ DOWNLOAD REPORT", report_text, file_name="forensic_report.txt")
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🆕 NEW MISSION", type="primary", use_container_width=True):
                    st.session_state.uploader_key += 1
                    del st.session_state.result
                    del st.session_state.decoded_url
                    st.session_state.analysis_triggered = False
                    st.rerun()

def main():
    if 'page' not in st.session_state: st.session_state.page = "Landing"
    
    # Global Sidebar Config (Hidden on Landing)
    if st.session_state.page == "Landing":
        render_landing_page()
    else:
        # Mock Config for Demo
        vt_key = "" 
        mock = True
        render_dashboard(mock, vt_key)

if __name__ == "__main__":
    main()
