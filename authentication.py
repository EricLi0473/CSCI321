import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

verification_codes = {}


def send_verification_code(email):
    verification_code = random.randint(1000, 9999)

    verification_codes[email] = verification_code

    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "ErrFunnSmelly@gmail.com"  # Need to create new 'App Password' in Google to use different email as sender.
    sender_password = "ugao xkih yhii nrww"  # Need to use the password from above.

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
        print(f"Verification code sent to {email}")
    except Exception as e:
        print(f"Failed to send email: {e}")


def verify_code(email, code):
    if email in verification_codes and verification_codes[email] == int(code):
        print("Verification successful!")
        return True
    else:
        print("Verification failed!")
        return False


# Send verification code
email = "ErrFunnSmelly@gmail.com"
send_verification_code(email)

# Verify verification code
user_input_code = input("Enter the verification code sent to your email: ")
verify_code(email, user_input_code)
