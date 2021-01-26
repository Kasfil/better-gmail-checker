"""Module to handle authentication.

Module handles to authentication and refresh token or credential.

Functions:
    _check_credential
    authenticate
"""
import os
import json
from typing import Dict
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class BetterGmailChecker:
    # public properties
    label_id: str
    api_response: Dict

    # Private properties
    _credential: Credentials = None
    _scopes: list[str] = ['https://www.googleapis.com/auth/gmail.labels']
    _dir: str = Path(__file__).resolve().parent
    _client_secrets_path = Path(_dir, 'client_secrets.json').resolve()
    _credential_path: Path = Path(_dir, 'credentials.json').resolve()

    def __init__(self, label_id: str = 'INBOX'):
        # set default label to INBOX
        self.label_id = label_id

        # Force authenticate if no valid credential
        while self._credential is None:
            if self._credential_path.is_file():
                self._parse_credential()
            else:
                self._authenticate()

        # execute API call

    def _write_credentials(self, credential: str) -> None:
        """Write given credential json to file

        Parameter:
            credential_json -> str
        Return:
            void
        """
        credential_file = open(self._credential_path, 'w')
        credential_file.write(credential)

    def _parse_credential(self) -> None:
        """Parse credential from credential file

        Return:
            Credentials
        """
        # read credential file
        credential = Credentials.from_authorized_user_file(self._credential_path)
        # check if credential is expired
        if not credential.expired:
            self._credential = credential
        else:
            try:
                credential.refresh(Request())
                self._write_credentials(credential.to_json())
            except RefreshError:
                os.remove(self._credential_path)

    def _authenticate(self) -> None:
        """Authenticate while nothing credential file"""
        # Creating object
        flow = InstalledAppFlow.from_client_secrets_file(
            self._client_secrets_path,
            scopes = self._scopes
        )
        # call authentication
        credential = flow.run_local_server()
        # write authentication response to credential file
        self._write_credentials(credential.to_json())

    def _call_api(self):
        # build service
        gmail = build('gmail', 'v1', credentials = self._credential)
        # get API response
        response = gmail.users().labels().get(userId = 'me', id = self.label_id).execute() # pylint: disable=no-member
        self.api_response = json.loads(response)
