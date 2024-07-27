# import random
# import requests
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from Entity.emailVerification import EmailVerification
#
# class EmailVerificationController:
#     def __init__(self):
#         pass
#
#     def send_verification_code(self, email):
#         verification_code = random.randint(1000, 9999)
#         subject = "Your Verification Code"
#         body = f"Your verification code is {verification_code}"
#         from_email = "stockforecast4me@trial-pq3enl6e8m742vwr.mlsender.net"  # 使用已验证的Mailersend域名
#         api_token = 'mlsn.86f3152b53b95736485f39da2bfa2e8ffc1967b5255bc442fd07c80d04ac34b0'
#
#         url = 'https://api.mailersend.com/v1/email'
#         headers = {
#             'Authorization': f'Bearer {api_token}',
#             'Content-Type': 'application/json'
#         }
#         data = {
#             "from": {
#                 "email": from_email
#             },
#             "to": [
#                 {
#                     "email": email
#                 }
#             ],
#             "subject": subject,
#             "text": body
#         }
#
#         try:
#             response = requests.post(url, json=data, headers=headers)
#             if response.status_code == 202:
#                 EmailVerification().insert_verify_code(email, verification_code)
#                 return f"Verification code sent to {email}"
#             else:
#                 print(f"Failed to send email: {response.status_code}")
#                 print(response.json())
#                 raise Exception(f"Failed to send email: {response.status_code}")
#         except Exception as e:
#             raise Exception(f"Failed to send email: {e}")
#
#     def verify_code(self, email, code):
#         return EmailVerification().emailVerify(email, code)
#
#
# if __name__ == "__main__":
#     # 发送验证码示例
#     controller = EmailVerificationController()
#     result = controller.send_verification_code("ljr20040703@gmail.com")


#     new verification
import random
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Entity.emailVerification import EmailVerification

class EmailVerificationController:
    def __init__(self):
        pass

    def send_verification_code(self, email):
        verification_code = random.randint(1000, 9999)
        subject = "Your Verification Code"
        body = f"Your verification code is {verification_code}"
        from_email = "verification@stockforecast4.me"
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
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 201:
                EmailVerification().insert_verify_code(email, verification_code)
                return f"Verification code sent to {email}"
            else:
                print(f"Failed to send email: {response.status_code}")
                print(response.json())
                raise Exception(f"Failed to send email: {response.status_code}")
        except Exception as e:
            raise Exception(f"Failed to send email: {e}")

    def verify_code(self, email, code):
        return EmailVerification().emailVerify(email, code)


if __name__ == "__main__":
    # 发送验证码示例
    controller = EmailVerificationController()
    result = controller.send_verification_code("jli094@mymail.sim.edu.sg")
    # result = controller.verify_code("lim077@mymail.sim.edu","6509")

    # 验证验证码示例
    # verification_result = controller.verify_code("ljr20040703@gmail.com", 3435)
    # print(verification_result)
