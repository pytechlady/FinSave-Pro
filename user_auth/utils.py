from django.utils.crypto import get_random_string
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from decouple import config
import logging

logger = logging.getLogger(__name__)

class Utils:
    
    @staticmethod
    def generate_vals(action):
        val = ''
        if action == 'acct_num':
            val = get_random_string(10, allowed_chars='123456789')
        elif action == 'otp_num':
            val = get_random_string(5, allowed_chars='123456789')
        return val
    
    @staticmethod
    def send_email(
        subject,
        receiver_email,
        message
    ):
        EMAIL_SERVER = config('EMAIL_SERVER')
        PORT = config('PORT')
        sender = config('SENDER_EMAIL')
        sender_password = config('SENDER_PASSWORD')

        msg = EmailMessage()
        msg["subject"] = subject
        msg["from"] = sender
        msg["To"] = receiver_email
        msg["BCC"] = sender

        msg.add_alternative(
            message,
            subtype="html",
        )

        try:
            with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
                server.starttls()
                server.login(sender, sender_password)
                server.send_message(msg)
            logger.info("Email sent successfully")
            print("Email sent successfully")
        except Exception as e:
            logger.error(f"Error sending message {e}")
            print(f"Error: {e}")
            