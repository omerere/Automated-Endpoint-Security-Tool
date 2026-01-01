# Automated Endpoint Security & Monitoring Framework

## Project Overview
This project is a modular security research tool developed in Python to demonstrate a complete end-to-end attack chain. It was designed to explore how unauthorized scripts interact with Windows OS internals, establish persistence, and execute secure data exfiltration while maintaining a deceptive user interface.

**Note: This tool was developed strictly for educational and ethical security research purposes.**

## Technical Features
* **Asynchronous Multi-Threading:** Uses the `threading` library to maintain a responsive "Decoy UI" while core monitoring modules run silently in the background.
* **Low-Level OS Integration:** Interacts with `user32.dll` via the `ctypes` library to monitor hardware states (Caps Lock, Shift) and identify active keyboard layouts in real-time.
* **Automated Persistence:** Programmed an installation module that leverages Windows directory structures to ensure the framework remains active across system reboots.
* **Secure Exfiltration Pipeline:** Implements the SMTP protocol over an SSL-encrypted connection to securely transmit captured data to a remote administrative server.
* **Social Engineering Camouflage:** Displays a non-blocking "Decoy Error" message box using Win32 API to divert user attention during initialization.

## 🛠️ Software Architecture
The system is built with a modular, object-oriented approach for high maintainability:
* `main.py`: The central orchestrator for all security modules.
* `system_ops.py`: Handles persistence and UI deception.
* `network.py`: Manages encrypted data transmission.
* `keylogger.py`: The core hardware event listener.

## Setup & Usage
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/omerere/Automated-Endpoint-Security-Tool.git](https://github.com/omerere/Automated-Endpoint-Security-Tool.git)
    ```
2.  **Configure Credentials:**
    * Rename `config.py.example` to `config.py`.
    * Input your SMTP server details and recipient email address.
3.  **Run the application:**
    ```bash
    python main.py
    ```

## Ethical Disclaimer
I do not condone or support the use of this software for malicious activities.