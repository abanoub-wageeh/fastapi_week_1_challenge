import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from pwdlib import PasswordHash

def send_verification_email(recipient_email, token):
    """Send verification email with token link"""
    
    # Email configuration
    SMTP_SERVER = "smtp.gmail.com"  
    SMTP_PORT = 587
    SENDER_EMAIL = "wageehabanoub8@gmail.com"
    PASSWORD = os.getenv("APP_PASSWORD")  
    BASE_URL = "http://127.0.0.1:8000"  
    
    # Create verification link
    verification_link = f"{BASE_URL}/verify_account?token={token}"
    
    # Create message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Verify Your Email Address"
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    
    html_body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
          <h2 style="color: #4CAF50;">Verify Your Email Address</h2>
          <p>Welcom inboard,</p>
          <p>Thank you for signing up! Please verify your email address by clicking the button below:</p>
          
          <div style="text-align: center; margin: 30px 0;">
            <a href="{verification_link}" 
               style="background-color: #4CAF50; 
                      color: white; 
                      padding: 12px 30px; 
                      text-decoration: none; 
                      border-radius: 5px;
                      display: inline-block;
                      font-weight: bold;">
              Verify Email Address
            </a>
          </div>
          
          <p>Or copy and paste this link into your browser:</p>
          <p style="word-break: break-all; color: #666; font-size: 14px;">
            {verification_link}
          </p>
          
          <p style="color: #999; font-size: 12px; margin-top: 30px;">
            This link will expire in 24 hours. If you didn't create an account, 
            please ignore this email.
          </p>
        </div>
      </body>
    </html>
    """
    
    part2 = MIMEText(html_body, 'html')
    msg.attach(part2)
    
    # Send email
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"Verification email sent successfully to {recipient_email}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False



password_hash = PasswordHash.recommended()

def hash_password(password : str):
  return password_hash.hash(password)

def verify_password(password, hashed_password):
    return password_hash.verify(password, hashed_password)