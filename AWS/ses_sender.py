import boto3
import argparse
import json

class SESEmailSender:
    def __init__(self, region='us-east-1'):
        self.ses = boto3.client('ses', region_name=region)

 def send_email(self, from_email, to_emails, subject, body_html, body_text=None):
        """Send plain text or HTML email."""
        payload = {
            'Source': from_email,
            'Destination': {'ToAddresses': to_emails},
            'Message': {
                'Subject': {'Data': subject},
                'Body': {
                    'Html': {'Data': body_html}
                }
            }
        }
        if body_text:
            payload['Message']['Body']['Text'] = {'Data': body_text}
        response = self.ses.send_email(**payload)
        print(f"Email sent: {response['MessageId']}")
        return response['MessageId']