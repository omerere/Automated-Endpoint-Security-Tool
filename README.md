# Crypto Wallet Social Engineering PoC (Attack Simulation)

## Ethical Disclaimer
**This software was developed strictly for educational purposes and authorized security research.** The code demonstrates vulnerabilities in physical security and user awareness. It performs persistence, data capture, and exfiltration. **Do not use this tool on unauthorized systems.**

## Project Overview
This project simulates a **"Red Team" physical attack vector** known as a "Honey Trap". 
The goal is to demonstrate how a targeted adversary can bypass network firewalls by leveraging human curiosity.

**The Scenario:** 1. A weaponized USB drive labeled "CRYPTO WALLET" is dropped in a target location, such as next to a Binance store.
2. The drive contains a **Decoy** (`passwords.txt`) and a **Payload** (disguised as `Wallet_App.exe`).
3. When the victim attempts to use the "wallet" with the fake credentials, the malware installs silently while displaying a fake error message ("Wallet Disabled") to lower suspicion.

## Technical Capabilities

### The Payload (Input Signal Processing)
* **Hardware Hooking:** Interacts with `user32.dll` to capture raw keystrokes.
* **Smart Mapping:** Detects active keyboard layouts (focusing on Hebrew/English toggling) and hardware states (Caps Lock/Shift).
* **Stealth:** Runs as a background process with no visible console window.

### The Loader (Deployment & Persistence)
* **Automated Persistence:** Detects the execution environment and replicates the executable to the Windows `Startup` directory for reboot survival.
* **Decoy UI:** Uses Win32 API (`MessageBoxW`) to generate a realistic "Critical Error" popup, validating the victim's belief that the files are simply broken/corrupted.

### Exfiltration
* **Encrypted Pipeline:** Logs are exfiltrated via SMTP (Gmail) using SSL encryption (`port 465`).
* **Heartbeat System:** Data is transmitted in configurable intervals (default: every 60 seconds) to minimize network noise.

## Software Architecture
The project follows a **Loader/Payload** design pattern to decouple system operations from intelligence gathering.

| File | Module Type | Description |
| :--- | :--- | :--- |
| **`main.py`** | **Orchestrator** | The entry point. Detects if running from USB (Attack Phase) or Startup (Persistence Phase) and triggers the appropriate modules. |
| **`deployment.py`** | **Loader** | Handles OS-level lifecycle: Installation, Persistence, and the Social Engineering UI (Fake Error). |
| **`keylogger.py`** | **Payload** | Pure capture module. Interfaces with low-level Windows APIs to normalize and record input data. |
| **`network.py`** | **Exfiltration** | Manages the secure transport layer for sending captured logs to the attacker. |
| **`config.py`** | **Config** | Centralized credentials and path configurations. |

## Usage & Deployment

### Prerequisites
* Python 3.10+
* Installation: To run this project in a development environment, install the necessary dependencies:
```bash
pip install -r requirements.txt

### Configuration
1.  Rename `config.py.example` to `config.py`.
2.  Add your "Attacker" email credentials (using App Password for Gmail).

### compiling (Weaponization)
To create the standalone executable for the USB drive:
```bash
pyinstaller --onefile --noconsole --name="Wallet_App_v2" --icon="bitcoin.ico" --clean main.py