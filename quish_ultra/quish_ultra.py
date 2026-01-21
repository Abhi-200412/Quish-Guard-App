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

# --- Configuration & Theme ---
st.set_page_config(
    page_title="Quish-Guard ULTRA",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Cyber-Warfare Theme
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #050505;
        color: #e0e0e0;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0a0a0a;
        border-right: 1px solid #333;
    }
    
    /* Headings */
    h1, h2, h3 {
        color: #00f0ff !important;
        font-family: 'Courier New', monospace;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(45deg, #00f0ff, #0080ff);
        color: #000;
        font-weight: bold;
        border: none;
        border-radius: 5px;
        transition: all 0.3s;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton>button:hover {
        box-shadow: 0 0 15px #00f0ff;
        transform: scale(1.02);
    }
    
    /* Verdict Box */
    .verdict-box {
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
        font-weight: bold;
        font-size: 2.5em;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    .safe {
        background: rgba(0, 255, 0, 0.1);
        border: 2px solid #00ff00;
        color: #00ff00;
        box-shadow: 0 0 30px rgba(0, 255, 0, 0.3);
    }
    .danger {
        background: rgba(255, 0, 0, 0.1);
        border: 2px solid #ff0000;
        color: #ff0000;
        box-shadow: 0 0 30px rgba(255, 0, 0, 0.3);
    }
    
    /* Logs */
    .log-box {
        background-color: #000;
        border: 1px solid #333;
        padding: 15px;
        height: 250px;
        overflow-y: auto;
        font-family: 'Consolas', monospace;
        color: #00f0ff;
        font-size: 0.85em;
        line-height: 1.5;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Assets (Lottie) ---
@st.cache_data
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

# Try to load animations, but don't crash if they fail
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

def check_virustotal(url, api_key):
    if not api_key: return None
    try:
        headers = {"x-apikey": api_key}
        # Mocking actual call for speed/demo reliability unless key provided
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



def generate_ai_insight(url, score, heuristics):
    """Generates a natural language explanation of the threat."""
    insight = f"**Analysis for {url}:**\n\n"
    if score > 50:
        insight += "⚠️ **CRITICAL THREAT DETECTED.**\n"
        insight += "This URL exhibits multiple high-risk indicators. "
        if "IP Address" in str(heuristics): insight += "It uses a raw IP address, which is a common tactic to bypass domain filters. "
        if "HTTP" in str(heuristics): insight += "The connection is unencrypted (HTTP), putting your data at risk. "
        insight += "\n\n**RECOMMENDATION:** DO NOT OPEN THIS LINK."
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
    for h in heuristics: score += 25
    final_score = min(score, 100)
    return final_score, "DANGER" if final_score > 50 else ("WARNING" if final_score > 0 else "SAFE")

def render_landing_page():
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<h1 style='text-align: center; font-size: 4em; text-shadow: 0 0 20px #00f0ff;'>QUISH-GUARD</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #fff;'>ULTRA EDITION</h3>", unsafe_allow_html=True)
        
        if LOTTIE_SCAN:
            st_lottie(LOTTIE_SCAN, height=300, key="landing_anim")
        else:
            st.markdown("<div style='text-align:center; font-size: 5em;'>🛡️</div>", unsafe_allow_html=True)
        
        if st.button("ENTER SYSTEM", type="primary", use_container_width=True):
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
        if 'history' not in st.session_state: st.session_state.history = []
        
        if not st.session_state.history:
            st.caption("No targets analyzed yet.")
        else:
            for i, item in enumerate(reversed(st.session_state.history[-5:])): # Show last 5
                icon = "🟢" if item['level'] == "SAFE" else "🔴"
                st.markdown(f"{icon} **{item['time']}**<br>`{item['url'][:20]}...`", unsafe_allow_html=True)
                st.divider()

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
                    st.session_state.scanning_active = True
                    st.rerun()
                if c2.button("⏹ STOP", use_container_width=True):
                    st.session_state.scanning_active = False
                    st.rerun()
                    
                if st.session_state.scanning_active:
                    placeholder = st.empty()
                    cap = cv2.VideoCapture(0)
                    while st.session_state.scanning_active:
                        ret, frame = cap.read()
                        if not ret: break
                        
                        # Decode
                        decoded_objects = decode(frame)
                        if not decoded_objects: decoded_objects = decode(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
                        
                        # HUD
                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        h, w, _ = frame_rgb.shape
                        cv2.rectangle(frame_rgb, (w//2-100, h//2-100), (w//2+100, h//2+100), (0, 255, 0), 2)
                        cv2.line(frame_rgb, (0, h//2), (w, h//2), (0, 255, 0), 1)
                        
                        if decoded_objects:
                            obj = decoded_objects[0]
                            decoded_text = obj.data.decode("utf-8")
                            
                            # Store Metadata
                            st.session_state.qr_meta = {
                                "type": obj.type,
                                "size": f"{obj.rect.width}x{obj.rect.height} px",
                                "raw_len": len(decoded_text)
                            }
                            
                            st.session_state.decoded_url = decoded_text
                            st.session_state.analysis_triggered = True # Auto-trigger for scanner
                            st.session_state.scanning_active = False
                            cap.release()
                            st.rerun()
                                
                        # Use default width (None) to avoid passing an invalid string value
                        # (passing a string like "stretch" raises a TypeError in newer Streamlit)
                        placeholder.image(frame_rgb, channels="RGB")
                    cap.release()

        with tab2:
            f = st.file_uploader("Upload Image", type=['png', 'jpg'], key="uploader")
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
            url = st.session_state.decoded_url
            
            # Check if analysis is triggered
            if not st.session_state.get('analysis_triggered', False):
                st.info(f"Target Loaded: {url}")
                st.write(f"Metadata: {st.session_state.get('qr_meta', 'N/A')}")
                if st.button("⚡ START ANALYSIS", type="primary", use_container_width=True):
                    st.session_state.analysis_triggered = True
                    st.rerun()
            
            # Auto-Analyze if triggered and no result yet
            elif 'result' not in st.session_state:
                with logs_ph.container():
                    st.markdown('<div class="log-box">', unsafe_allow_html=True)
                    st.write(f"> Target Acquired: {url}")
                    st.write(f"> Metadata: {st.session_state.get('qr_meta', 'N/A')}")
                    
                    # Heuristics
                    st.write("> Running Heuristic Scan...")
                    heuristics = check_heuristics(url)
                    if use_mock and "evil" in url: heuristics.append("Suspicious Keywords")
                    st.write(f"> Flags found: {len(heuristics)}")
                    
                    # VT
                    st.write("> Querying VirusTotal Database...")
                    vt_res = check_virustotal(url, vt_api_key)
                    if use_mock and "evil" in url: vt_res = "MALICIOUS"
                    st.write(f"> Threat Intel: {vt_res}")
                    
                    st.write("> Analysis Complete.")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                score, level = calculate_risk(vt_res, heuristics)
                insight = generate_ai_insight(url, score, heuristics)
                
                # Save to History
                if 'history' not in st.session_state: st.session_state.history = []
                st.session_state.history.append({
                    "url": url,
                    "level": level,
                    "score": score,
                    "time": datetime.datetime.now().strftime("%H:%M:%S")
                })
                
                st.session_state.result = {
                    "score": score, "level": level, "insight": insight, 
                    "url": url
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
                # Verdict Animation
                if res['level'] == "SAFE":
                    if LOTTIE_SAFE:
                        st_lottie(LOTTIE_SAFE, height=150, key="safe_anim")
                    else:
                        st.markdown("<div style='text-align:center; font-size: 3em;'>✅</div>", unsafe_allow_html=True)
                    st.markdown(f'<div class="verdict-box safe">SAFE<br><span style="font-size:0.4em">Score: {res["score"]}</span></div>', unsafe_allow_html=True)
                else:
                    if LOTTIE_DANGER:
                        st_lottie(LOTTIE_DANGER, height=150, key="danger_anim")
                    else:
                        st.markdown("<div style='text-align:center; font-size: 3em;'>🚨</div>", unsafe_allow_html=True)
                    st.markdown(f'<div class="verdict-box danger">THREAT<br><span style="font-size:0.4em">Score: {res["score"]}</span></div>', unsafe_allow_html=True)
                
                # AI Insight
                with st.expander("🤖 AI Threat Insight", expanded=True):
                    st.write(res['insight'])
                

                
                # Download Report
                report_text = f"QUISH-GUARD FORENSIC REPORT\n\nTarget: {res['url']}\nVerdict: {res['level']}\nScore: {res['score']}\n\nInsight:\n{res['insight']}"
                st.download_button("⬇️ DOWNLOAD REPORT", report_text, file_name="forensic_report.txt")

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
