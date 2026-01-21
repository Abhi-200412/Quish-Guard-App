# 🛡️ Quish-Guard ULTRA

**The Ultimate QR Code Phishing Defense System**

Quish-Guard ULTRA is an advanced, AI-powered forensic tool designed to detect and neutralize "Quishing" (QR Phishing) attacks. It combines real-time scanning, threat intelligence (VirusTotal), and heuristic analysis into a sleek, cyber-warfare themed dashboard.

---

## 🚀 Features

*   **Real-Time Webcam Scanner**: Continuously scans for QR codes with a high-tech HUD overlay.
*   **Instant Analysis**: Automatically decodes and analyzes targets upon detection.
*   **VirusTotal Integration**: Checks URLs against the world's largest threat database.
*   **Advanced Heuristics**: Detects insecure protocols (HTTP), IP-based domains, and suspicious keywords.
*   **AI Threat Insight**: Generates natural language explanations of *why* a link is dangerous.
*   **Geo-Intelligence**: Visualizes the server's physical location on an interactive map.
*   **Mission Log**: Tracks your session history and findings.
*   **Forensic Reports**: Download detailed analysis reports for documentation.

---

## 📦 Installation

1.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the application**:
    ```bash
    streamlit run quish_ultra/quish_ultra.py
    ```

---

## 🎮 Usage Guide

### 1. The Landing Page
*   Launch the app to see the cinematic entry screen.
*   Click **"ENTER SYSTEM"** to access the dashboard.

### 2. The Dashboard
*   **Scanner Tab**: Use your webcam to scan QR codes. The app will lock onto the code and auto-analyze it.
*   **Upload Tab**: Upload an image file containing a QR code.
*   **Configuration (Sidebar)**: Enter your **VirusTotal API Key** here for real threat data.

### 3. The Verdict
*   **GREEN (SAFE)**: The link is clean.
*   **RED (THREAT)**: The link is malicious or suspicious.
*   **AI Insight**: Read the generated explanation to understand the risk.
*   **Map**: See where the server is hosted.

### 4. CLI Mode (Headless)
For batch analysis or automation, use the CLI tool:
```bash
python quish_cli.py path/to/image.png --key YOUR_API_KEY
```

---

## ⚠️ Disclaimer
This tool is for educational and defensive purposes only. Always verify findings manually before taking action.
