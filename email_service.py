"""
Module: Network Utilities
Description: A generic, reusable SMTP client. 
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os

class EmailService:
    def __init__(self, sender_email, sender_password):
        """Initialize with the identity of the SENDER."""
        self.sender = sender_email
        self.password = sender_password

    def send_email(self, receiver_email, subject, body, attachment_path=None):
        """
        Generic method to send an email to any receiver.
        """
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender
            msg['To'] = receiver_email
            msg['Subject'] = subject

            # Attach Body
            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            # Attach File (if provided)
            if attachment_path and os.path.exists(attachment_path):
                with open(attachment_path, "rb") as f:
                    part = MIMEApplication(f.read(), Name=os.path.basename(attachment_path))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
                msg.attach(part)

            # Send via Gmail SMTP
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(self.sender, self.password)
                server.sendmail(self.sender, receiver_email, msg.as_string())
            
            return True
        except Exception as e:
            print(f"[Network] Error: {e}")
            return False