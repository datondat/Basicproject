import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailBot:
    def __init__(self, smtp_server, smtp_port, bot_email, bot_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.bot_email = bot_email
        self.bot_password = bot_password

    def send(self, to_email, subject, message):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.bot_email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, "plain"))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.bot_email, self.bot_password)
            server.send_message(msg)
            server.quit()
            print(f"Email sent to {to_email}")
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False