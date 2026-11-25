from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os


SENDER = str(os.environ.get("GMAIL_ACCOUNT"))
PASSWORD = str(os.environ.get("APP_PASSWORD"))


class Mail(EmailMessage):
    def __init__(self, to,subject,content):
        super().__init__()
        self["To"] = to
        self["From"] = SENDER
        self["Subject"] = subject
        self.content = content

    def sendmail(self):
        msg = MIMEMultipart()
        msg["To"] = self["To"]
        msg["From"] = SENDER
        msg["Subject"] = self["Subject"]

        msg.attach(MIMEText(self.content,'plain','UTF-8'))
        try:
            server = smtplib.SMTP("smtp.gmail.com",587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(SENDER,PASSWORD)
            server.sendmail(self["From"],self["To"],msg.as_string())
            server.quit()
            print(f"Mail sent to {msg['To']} successfully.")
        except Exception as e:
            print(f"Mail Error:{e}")
