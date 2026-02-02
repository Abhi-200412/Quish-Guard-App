# 🛠️ Quish-Guard ULTRA: Technical Documentation

## Architecture Overview

Quish-Guard ULTRA is built on **Streamlit**, a Python framework for rapid web app development. It follows a reactive, state-based architecture where user interactions trigger re-runs of the script, updating the UI dynamically.

### Core Components

1.  **Frontend (UI)**:
    *   **Streamlit**: Handles layout, widgets, and state management.
    *   **Custom CSS**: Injected via `st.markdown` to enforce the "Cyber-Warfare" dark theme, glowing borders, and custom fonts.
    *   **Lottie Animations**: Vector animations for visual feedback (Scanning, Safe, Danger).

2.  **Backend (Logic)**:
    *   **OpenCV (`cv2`)**: Captures video frames and processes images.
    *   **Pyzbar**: Decodes QR code data from image frames.
    *   **Requests**: Handles API calls to VirusTotal and IP-API.
    *   **Socket**: Resolves domains to IP addresses.

---

## Key Modules

### `quish_ultra.py`
The main application entry point.

*   `render_landing_page()`: Displays the intro screen.
*   `render_dashboard()`: The main UI loop.
    *   **Scanner Loop**: A `while` loop inside `st.empty()` that captures frames, runs `decode()`, and updates the image placeholder.
    *   **Auto-Analysis**: Triggered immediately when `decoded_objects` is found.
*   `check_heuristics(url)`:
    *   Checks for `http://` vs `https://`.
    *   Regex check for IP addresses in the domain (`192.168.x.x`).
    *   Checks for suspicious TLDs (`.xyz`, `.top`, etc.).
*   `check_virustotal(url, key)`:
    *   Queries the VirusTotal v3 API.
    *   Returns "MALICIOUS", "SUSPICIOUS", or "CLEAN".
*   `generate_ai_insight(url, score, heuristics)`:
    *   Rule-based string generation to explain the risk score in plain English.

### `quish_cli.py`
A headless version of the logic for command-line use.
*   Iterates through directories or single files.
*   Prints colored output to stdout.

---

## Data Flow

1.  **Input**: Webcam Frame -> `cv2` -> `pyzbar` -> `URL String`.
2.  **Processing**:
    *   `URL` -> `check_heuristics()` -> `Flags List`.
    *   `URL` -> `check_virustotal()` -> `VT Status`.
    *   `URL` -> `socket.gethostbyname()` -> `IP` -> `ip-api.com` -> `Lat/Lon`.
3.  **Scoring**:
    *   `calculate_risk(VT, Flags)` -> `Score (0-100)` -> `Verdict (SAFE/DANGER)`.
4.  **Output**:
    *   UI updates with Verdict, Map, and AI Insight.
    *   Result appended to `st.session_state.history`.

---

## Dependencies

*   `streamlit`: UI Framework.
*   `opencv-python-headless`: Image processing (headless for server compatibility).
*   `pyzbar`: QR Decoding.
*   `requests`: HTTP Client.
*   `streamlit-lottie`: Animation rendering.
*   `pandas`: Data handling for maps.
