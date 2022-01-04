import smtplib
from email.mime.text import MIMEText
from CONST import MAIL_PASS


def send_email(message, getter, sender):
    sender = sender
    password = MAIL_PASS

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login(sender, password)
    msg = MIMEText(message)
    msg["Subject"] = "CLICK ME PLEASE!"
    server.sendmail(sender, getter, msg.as_string())
