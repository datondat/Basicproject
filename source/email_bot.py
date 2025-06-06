import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailBot:
    def __init__(self, smtp_server, smtp_port, bot_email, bot_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.bot_email = bot_email
        self.bot_password = bot_password

    def send(self, to_email, subject, message):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", to_email):
            logger.error(f"Invalid email address: {to_email}")
            return False

        try:
            msg = MIMEMultipart()
            msg['From'] = self.bot_email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, "plain"))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=10)
            server.starttls()
            server.login(self.bot_email, self.bot_password)
            server.send_message(msg)
            server.quit()
            logger.info(f"Email sent to {to_email}")
            return True
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"Authentication failed: {e}")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return False