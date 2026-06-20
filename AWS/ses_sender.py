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


    if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--from', dest='from_email', required=True)
    parser.add_argument('--to', dest='to_emails', nargs='+', required=True)
    parser.add_argument('--subject', required=True)
    parser.add_argument('--html', required=True, help='HTML body')
    parser.add_argument('--text', help='Plain text body')
    parser.add_argument('--region', default='us-east-1')
    args = parser.parse_args()

    sender = SESEmailSender(args.region)
    sender.send_email(args.from_email, args.to_emails, args.subject, args.html, args.text)