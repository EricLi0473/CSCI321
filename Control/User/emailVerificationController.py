import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from Entity.emailVerification import *


class EmailVerificationController:
    def __init__(self):
        pass

    def send_verification_code(self, email):
        verification_code = random.randint(1000, 9999)

        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "stockforecast4me@gmail.com"  # Need to create new 'App Password' in Google to use different email as sender.
        sender_password = "iwnm mhao iteg rafl"  # Need to use the password from above.

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = email
        message["Subject"] = "Your Verification Code"
        body = f"Your verification code is {verification_code}"
        message.attach(MIMEText(body, "plain"))

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, message.as_string())
            server.quit()
            EmailVerification().insert_verify_code(email, verification_code)
            return f"Verification code sent to {email}"
        except Exception as e:
            raise f"Failed to send email: {e}"

    def verify_code(self, email, code):
        return EmailVerification().emailVerify(email, code)


if __name__ == "__main__":
    # EmailVerificationController().send_verification_code("ljr20040703@gmail.com")
    EmailVerificationController().verify_code("ljr20040703@gmail.com", 3704)
