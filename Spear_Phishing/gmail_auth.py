import os
import joblib
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Define API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    """Authenticate and generate token.json for Gmail API."""
    creds = None
    if os.path.exists("token.json"):
        creds = joblib.load("token.json")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        joblib.dump(creds, "token.json")

    return creds

if __name__ == "__main__":
    authenticate_gmail()
    print("✅ Authentication Successful! Token saved.")
