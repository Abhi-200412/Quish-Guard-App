# 🛠️ Quish-Guard ULTRA: Technical Whitepaper

## 1. Project Overview
**Quish-Guard ULTRA** is a client-side forensic tool designed for **Defensive Security** and **OSINT** (Open Source Intelligence). It specifically targets "Quishing" (QR Code Phishing), a vector where attackers bypass email filters by embedding malicious URLs inside QR code images.

Unlike standard QR scanners, this tool is built for **Threat Analysis**, providing deep inspection of the payload rather than just opening it.

---

## 2. The Vision Engine (Robust Detection Pipeline)
The core of the application is a high-availability computer vision pipeline built on **OpenCV** and **Pyzbar**. To ensure detection in adverse conditions (low light, glare, grain), the system employs a multi-stage fallback mechanism for every video frame:

### Stage 1: Standard Decode
*   **Input**: Raw BGR frame.
*   **Method**: Direct pass to `pyzbar`.
*   **Use Case**: Ideal lighting, high-contrast black-on-white codes.

### Stage 2: Grayscale Conversion
*   **Input**: `cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)`
*   **Method**: Removes color channel noise.
*   **Use Case**: Colored QR codes or chromatic aberration from lenses.

### Stage 3: Night Vision (CLAHE)
*   **Technique**: **Contrast Limited Adaptive Histogram Equalization**.
*   **Parameters**: `ClipLimit=2.0`, `TileGridSize=(8,8)`.
*   **Logic**: This locally enhances contrast in small regions of the image, effectively "turning on the lights" in dark video feeds without blowing out highlights.
*   **Use Case**: Dark rooms, shadowed paper.

### Stage 4: De-Noising (Gaussian Blur)
*   **Technique**: `cv2.GaussianBlur(gray, (5,5), 0)`.
*   **Logic**: Smooths out high-frequency noise (grain) common in low-quality webcams.
*   **Use Case**: Grainy/Old webcams.

### Stage 5: Binary Thresholding (Otsu)
*   **Technique**: `cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)`.
*   **Logic**: Forces every pixel to be either pure black or pure white based on a calculated threshold.
*   **Use Case**: Faded prints, low contrast codes.

---

## 3. Forensic Analysis Module
Once a payload is extracted, it undergoes a battery of forensic checks:

### A. Payload Identification
The system first enables **Schema Analysis** to identify non-web vectors:
*   `WIFI:`: Wi-Fi network credentials.
*   `SMSTO:`: SMS triggers (often used for premium rate fraud).
*   `VCARD:`: Contact cards (used for social engineering/impersonation).

### B. Redirect Tracing
Attackers often use URL shorteners or open redirects to hide the true phishing domains.
*   **Method**: `requests.head(url, allow_redirects=True)`
*   **Output**: Traces the full hop chain (e.g., `bit.ly` -> `evil-site.com`). All analysis is performed on the *final* destination.

### C. Heuristic Engine
Static analysis flags suspicious patterns without needing external APIs:
*   **IP Hostnames**: `http://192.168.x.x` (Bypasses domain filters).
*   **Insecure Protocol**: `http://` (Data interception risk).
*   **Suspicious TLDs**: `.xyz`, `.top`, `.cn` (Statistically higher abuse rates).
*   **Keyword Matching**: `verify`, `login`, `secure` in the URL path.

### D. Threat Intelligence (VirusTotal)
*   Integrates with the **VirusTotal v3 API**.
*   Checks the URL hash against 70+ security vendors.
*   Returns a consensus verdict (Malicious/Clean).

---

## 4. Architecture & UI
The application uses a **Reactive State Machine** architecture powered by **Streamlit**.

### State Management (`st.session_state`)
Because Streamlit re-runs the script on every interaction, persistent data (like history, current scan results, and UI toggles) is stored in the `st.session_state` dictionary.
*   `scanning_active`: boolean - Controls the OpenCV `while` loop.
*   `uploader_key`: integer - Used to force-reset the file uploader widget.

### Glassmorphism & Cyber-Aesthetics
The "Ultra" look is achieved via **CSS Injection** (`st.markdown(unsafe_allow_html=True)`).
*   **Backdrop Filter**: `backdrop-filter: blur(16px)` creates the frosted glass effect.
*   **Animations**: CSS Keyframes allow for the "Scanning Beam" and "Pulsing Badges" without JavaScript overhead.
*   **HUD**: The webcam overlay is drawn directly onto the image array using OpenCV primitives (`cv2.line`, `cv2.putText`) before being rendered to the UI, ensuring zero latency lag between the video and the overlay.
