from .utils import Utils
from celery import shared_task
import logging

logger = logging.getLogger(__name__)


messages = {
            "otp_email": '''
            <html>
            <body>
            <p>Hi,</p>
            <p>Use OTP below to verify ypur email</p>
            <p><strong>{OTP}</strong></p>
            <p>Best regards,</p>
            <p>SavePro Team</p>
            </body>
            </html>
            '''
        }
        

@shared_task
def send_email_message(msg_type, receiver_email, subject, otp):
        logger.info('Sending email to %s', receiver_email)
        try:
            Utils.send_email(
                subject=subject, 
                receiver_email=receiver_email, 
                message=messages.get(msg_type).format(OTP=otp)
            )
            logger.info('Email sent to %s', receiver_email)
        except Exception as e:
            logger.error('Error sending email to %s: %s', receiver_email, str(e))
            
        


