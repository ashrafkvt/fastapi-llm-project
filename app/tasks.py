import smtplib
import os

from app.celery import app
from email.message import EmailMessage


@app.task
def send_welcome_email(user_email):
    # Email server settings
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_POPT")
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    
    # Email content
    subject = "Welcome to Our Service!"
    body = f"Hello,\n\nThank you for signing up for our service. We're excited to have you on board!\n\nBest regards,\nThe Team"
    
    # Create the email message
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = user_email

    try:
        # Connect to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        print(f"Welcome email sent to {user_email}")
        return f"Welcome email sent to {user_email}"
    except Exception as e:
        print(f"Failed to send email to {user_email}. Error: {e}")
        return f"Failed to send email to {user_email}. Error: {e}"
