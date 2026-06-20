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

    def send_templated_email(self, from_email, to_emails, template_name, template_data):
        """Send using SES template."""
        response = self.ses.send_templated_email(
            Source=from_email,
            Destination={'ToAddresses': to_emails},
            Template=template_name,
            TemplateData=json.dumps(template_data)
        )
        print(f"Templated email sent: {response['MessageId']}")