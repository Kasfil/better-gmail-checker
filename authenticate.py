"""Module to handle authentication.

Module handles to authentication and refresh token or credential.

Functions:
    _check_credential
    authenticate
"""
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = ['https://www.googleapis.com/auth/gmail.labels']
CLIENT_SECRETS_PATH = Path('client_secrets.json').resolve()
CREDENTIAL_PATH = Path('credentials.json').resolve()

def _parse_credential():
    creds = Credentials.from_authorized_user_file(CREDENTIAL_PATH)
    print(creds.expired)
    print(creds.refresh_token)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        return None

    return creds

def _authenticate():
    """Authenticate while nothing credential file"""
    # Creating object
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_PATH,
        scopes = SCOPES
    )
    # call authentication
    credential = flow.run_local_server()
    # prepare credential file
    cred_file = open(CREDENTIAL_PATH, 'w')
    # write authentication response to credential file
    cred_file.write(credential.to_json())

def get_credential() -> Credentials:
    """Get credential for retreive API"""
    creds = None

    while creds is None:
        if CREDENTIAL_PATH.is_file():
            creds = _parse_credential()
        else:
            _authenticate()

    return creds

gmail = build('gmail', 'v1', credentials=get_credential())
response = gmail.users().labels().get(userId = 'me', id = 'INBOX').execute()
print(json.dumps(response, sort_keys=True, indent=2))
