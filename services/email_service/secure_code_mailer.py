import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template

import os
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = os.getenv('SENDER_EMAIL')
APP_PASSWORD = os.getenv('APP_PASSWORD')


def load_template():
    with open(r"../services/email_service/templates/verification_template.html", "r") as file:
        template_str = file.read()
    return Template(template_str)


def send_verification_email(receiver_email, verification_code):
    sender_email = SENDER_EMAIL
    app_password = APP_PASSWORD
    email_data = {
        "subject": "Email Verification From Soly",
        "greeting": f"Hi!",
        "message": f"your email verification is:{verification_code}"
    }
    email_content = load_template().render(email_data)
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = email_data['subject']
    message.attach(MIMEText(email_content, "html"))

    # Connect to the SMTP server
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, app_password)

        # Send the email
        server.sendmail(sender_email, receiver_email, message.as_string())


def generate_verification_code():
    return random.randint(100000, 999999)


async def send_email(user_email: str) -> int:
    user_email = user_email
    verification_code = generate_verification_code()
    send_verification_email(user_email, str(verification_code))
    return verification_code
