import pandas as pd
import io
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class email_send():
    def __init__(self,users_non_compliant_dict):
        self.users_non_compliant_dict = users_non_compliant_dict

        self.SMTP_SERVER = 'smtp.gmail.com'
        self.SMTP_PORT = 587
        self.SMTP_USERNAME = os.getenv('USERNAME')
        self.SMTP_PASSWORD = os.getenv('PASSWORD')
        self.SENDER_EMAIL = os.getenv('USERNAME')
        self.SENDER_NAME = 'Mr. Panda'

    def email_sending(self):

        df = pd.DataFrame(self.users_non_compliant_dict)
        print(df.head())
        with smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT) as server:
            server.starttls()
            server.login(self.SMTP_USERNAME, self.SMTP_PASSWORD)

            # Send an email to each non-compliant customer
            non_compliant_customers = df[df['CompliantStatus'] == 'Non-Compliant']
            output = list()
            for index, row in non_compliant_customers.iterrows():
                msg = MIMEMultipart()
                msg['From'] = f"{self.SENDER_NAME} <{self.SENDER_EMAIL}>"
                msg['To'] = row['EmailId']
                msg['Subject'] = 'Documents Required for KYC of Bio Emergent Solutions.'

                # Customize the email body as needed
                body = f"Hi there,\n\n" \
                        f"Hope you're doing great!\n\n" \
                        f"Just wanted to quickly reach out and share some updates. We’ve been working on a few exciting things and would love for you to check them out.\n\n" \
                        f"If you're interested, feel free to reply to this email — happy to share more details.\n\n" \
                        f"Looking forward to staying in touch!\n\n" \
                        f"Cheers,\n" \
                        f"{self.SENDER_NAME}"

                msg.attach(MIMEText(body, 'plain'))
                server.send_message(msg)
                message = f"Email sent successfully to {row['CustomerID']}"
                output.append(message)
                #print(message)
        return {"output" : output}


