# 🛡️ Quish-Guard ULTRA

**The Ultimate QR Code Phishing Defense System**

![Quish-Guard Banner](https://img.shields.io/badge/Status-OPERATIONAL-brightgreen?style=for-the-badge) ![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python) ![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit)

Quish-Guard ULTRA is an advanced, AI-powered forensic tool designed to detect and neutralize "Quishing" (QR Phishing) attacks. It combines real-time scanning with a multi-stage robust detection engine, threat intelligence (VirusTotal), and heuristic analysis into a sleek, cyber-warfare themed dashboard.

---

## 🚀 Key Features

### 👁️ Tactical HUD Scanner
*   **Real-Time Overlay**: "Head-Up Display" with dynamic targeting reticles.
*   **Robust Detection Engine**: Multi-stage pipeline using **Grayscale**, **CLAHE** (Night Vision), and **Otsu Thresholding** to detect QR codes in any lighting condition.
*   **Boot Sequence**: Immersive sensor initialization animations.

### 🧠 Forensic Analysis
*   **Deep Inspection**: Traces redirects, checks domain age, and identifies insecure protocols (HTTP, IP-based URLs).
*   **VirusTotal Integration**: Cross-references findings with the world's largest threat database.
*   **AI Threat Insight**: Generates natural language explanations of *why* a link is dangerous.
*   **Payload Detection**: Identifies non-web payloads like Wi-Fi configs, SMS triggers, and vCards.

### 💻 System Dashboard
*   **Glassmorphism UI**: A premium, responsive interface with neon accents and 3D background animations.
*   **Mission Log**: Persistently tracks your session history and findings.
*   **Forensic Reports**: Download detailed text reports for documentation.

---

## 📦 Installation Configuration

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/quish-guard-ultra.git
    cd quish-guard-ultra
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the System**:
    ```bash
    streamlit run quish_ultra/quish_ultra.py
    ```

---

## 🎮 Operational Guide

### 1. The Landing Page
*   Launch the app to see the cinematic entry screen.
*   Click **"INITIATE SYSTEM"** to access the command center.

### 2. The Dashboard
*   **Scanner Tab**: Activate the webcam. The HUD will search for targets. When a QR code is detected, it locks on (Green Box) and auto-analyzes.
*   **Upload Tab**: Upload an image file for static analysis.
*   **Configuration**: Enter your **VirusTotal API Key** in the sidebar for enhanced threat data.

### 3. Threat Verdicts
*   **GREEN (SAFE)**: The link is clean and established.
*   **RED (THREAT)**: The link shows signs of phishing, obfuscation, or malicious intent.
*   **AI Insight**: Read the generated brief to understand specific risks.

---

## ⚠️ Disclaimer
This tool is for educational and defensive purposes only. Always verify findings manually before taking action. "Quish-Guard" is a proof-of-concept cybersecurity tool.
