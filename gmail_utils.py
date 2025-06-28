# gmail_utils.py
import os
from base64 import urlsafe_b64decode
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def gmail_authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    print("✅ Gmail authentication successful.")
    return build('gmail', 'v1', credentials=creds)


def get_recent_emails(service, max_results=50):
    results = service.users().messages().list(userId='me', q='in:inbox -in:sent', maxResults=max_results).execute()
    messages = results.get('messages', [])

    email_data = []
    for msg in messages:
        msg_detail = service.users().messages().get(userId='me', id=msg['id']).execute()
        headers = {d['name']: d['value'] for d in msg_detail['payload']['headers']}
        email_data.append({
            'id': msg['id'],
            'subject': headers.get('Subject', 'No Subject'),
            'from': headers.get('From', 'Unknown Sender'),
            'snippet': msg_detail.get('snippet', ''),
            'has_attachment': any(part.get('filename') for part in msg_detail.get('payload', {}).get('parts', []))
        })
    return email_data



def get_attachment(service, message_id):
    msg = service.users().messages().get(userId='me', id=message_id).execute()
    parts = msg['payload'].get('parts', [])
    for part in parts:
        if part.get('filename') and 'attachmentId' in part['body']:
            attachment = service.users().messages().attachments().get(
                userId='me',
                messageId=message_id,
                id=part['body']['attachmentId']
            ).execute()
            file_data = urlsafe_b64decode(attachment['data'].encode('UTF-8'))
            return part['filename'], file_data
    return None, None


if __name__ == "__main__":
    service = gmail_authenticate()
    emails = get_recent_emails(service)
    for email in emails:
        print(f"Subject: {email['subject']} | From: {email['from']}")
