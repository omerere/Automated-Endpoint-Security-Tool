# USB Attack Vector Simulation (with AI Threat Intelligence)

## Ethical Disclaimer
**This software was developed strictly for educational purposes.** The code demonstrates vulnerabilities in physical security ("Honey Trap"), user awareness, and post-exploitation data analysis. 
**Do not use this tool on unauthorized systems.**

## Project Overview
This project simulates a full-lifecycle **Red Team operation** focusing on physical access vectors.
The goal is to demonstrate how an adversary can bypass network firewalls using a weaponized USB drive, maintain persistence, and automate the intelligence gathering process using AI.
## Compatibility
- **Operating System:** Windows 10 / 11 (64-bit)
- **Note:** This is a native Windows application. It is not currently supported on macOS or Linux.

**The Attack Scenario:**
1.  **Infiltration (The Honey Trap):** A USB drive labeled "CRYPTO WALLET" is dropped in a target location, such as Binance store. It contains a payload disguised as `Wallet_App.exe`.
2.  **Infection:** When the victim opens the file, the malware installs silently to the Windows Startup folder while displaying a fake "Wallet has been disabled" error to lower suspicion.
3.  **Exfiltration (The Chain):** To remain stealthy, the malware streams encrypted logs to an intermediate "Dead Drop" email account.
4.  **Intelligence (The AI):** Once a day, the attacker's server automatically aggregates these logs and uses **Google Gemini AI** to extract high-value credentials (passwords/users) and generate a clean intelligence report.

## Architecture: The "Chain of Custody"
This project implements a sophisticated **3-Tier Exfiltration Architecture** to hide the attacker's identity:



* **Tier 1: The Mule (Mail 1)**
    * **Role:** The "Sender" account embedded in the malware.
    * **Security:** Disposable. If the malware is reverse-engineered, the victim only finds this empty shell account.
* **Tier 2: The Vault (Mail 2)**
    * **Role:** The "Receiver" / "Dead Drop".
    * **Security:** Never accessed directly by the malware. It acts as a holding tank for raw data logs.
* **Tier 3: The Master (Mail 3)**
    * **Role:** The Attacker's personal secure email.
    * **Security:** Completely air-gapped from the victim. Receives only the final, AI-processed report.

## Technical Capabilities

### 1. Payload & Persistence (`keylogger.py`, `deployment.py`)
* **Hardware Hooking:** Uses `ctypes` to interact with low-level Windows APIs (`user32.dll`) for capturing raw input.
* **Smart Normalization:** Detects active keyboard layouts (Hebrew/English toggling) and Shift/Caps Lock states.
* **Registry Persistence:** Replicates itself to `AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup` for reboot survival.

### 2. Email Service (`email_service.py`)
* **Generic Service:** Implements `EmailService` class.
* **TLS Encryption:** All traffic is transmitted via SMTP/SSL (Port 465) to bypass basic packet sniffing.

### 3. AI Analysis Module (`log_analyzer.py`)
* **Automated Aggregation:** Connects to the "Vault" via IMAP, fetching only logs created today.
* **AI Integration:** Uses **Google Gemini 1.5** to parse thousands of lines of raw keystrokes.
* **Credential Harvesting:** The AI filters out noise (backspaces, navigation keys) and extracts only potential usernames, passwords, and URLs.

## Project Structure

| File | Module | Description |
| :--- | :--- | :--- |
| `main.py` | **Orchestrator** | Entry point. Manages the malware lifecycle (Looping, Logging, Wiping Evidence). |
| `deployment.py` | **Loader** | Handles installation, persistence, and the Social Engineering "Fake Error" UI. |
| `keylogger.py` | **Payload** | Captures and interprets hardware input signals. |
| `email_service.py` | **Service** | Generic SMTP client used by both the Malware (for logs) and the Analyzer (for reports). |
| `log_analyzer.py` | **Intelligence** | Post-exploitation tool. Fetches logs, runs AI analysis, and emails the Master Report. |
| `config.py` | **Configuration** | Centralized credentials for the 3-Email Chain and API Keys. |

## Setup & Usage

### Prerequisites
* Python 3.10+
* **Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### 1. Configuration (`config.py`)
You must configure the **3-Email Chain** and your **AI Key**:
1.  **`RAW_LOG_SENDER`**: The "Mule" email (User/App Password).
2.  **`RAW_LOG_RECEIVER`**: The "Vault" email (User/App Password).
3.  **`FINAL_REPORT_RECEIVER`**: Your personal email.
4.  **`API_KEY`**: Google Gemini API Key.

### 2. Build the Weapon (The Malware)
Compile the script into a standalone executable for the USB drive:
```bash
pyinstaller --onefile --noconsole --name="Wallet_App_v2" --icon="bitcoin.ico" --clean main.py
```

### 3. Run the Analysis (The Attacker)
This script runs on your machine (not the victim's). Run it manually (e.g., once a day) to process the logs collected in the Vault:
```bash
python log_analyzer.py
```