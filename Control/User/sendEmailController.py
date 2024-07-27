import random
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class sendEmailController:
    def __init__(self):
        pass

    def send_Notification(self, email,bodyContent):
        subject = "Notification from Stock4me"
        body = f"{bodyContent}"
        from_email = "notification@stockforecast4.me"
        api_key = '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'

        url = 'https://api.brevo.com/v3/smtp/email'
        headers = {
            'accept': 'application/json',
            'api-key': api_key,
            'content-type': 'application/json'
        }
        data = {
            "sender": {
                "name": "Stock Forecast4me",
                "email": from_email
            },
            "to": [
                {
                    "email": email,
                    "name": "Recipient"
                }
            ],
            "subject": subject,
            "htmlContent": f"<html><body><p>{body}</p></body></html>"
        }

        try:
            requests.post(url, json=data, headers=headers)
        except Exception as e:
            raise Exception(f"Failed to send email: {e}")

if __name__ == "__main__":
    sendEmailController().send_Notification("jli094@mymail.sim.edu.sg", "Your threshold")
