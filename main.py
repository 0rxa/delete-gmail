from __future__ import print_function
import json
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = [ 'https://mail.google.com/' ]

def main():
    creds = None
    if os.path.exists("token.pickle"):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    ids = []
    nextPageToken = ''
    c=0
    while True:
        response = service.users().messages().list(userId='me',
                q='after:2012/1/1 before:2016/1/1',
                maxResults=10000,
                pageToken=nextPageToken
                ).execute()
        ids.extend([obj['id'] for obj in response['messages']])
        if 'nextPageToken' in response.keys():
            nextPageToken = response["nextPageToken"]
        else:
            break
    print(json.dumps(ids, indent=4))
    print(len(ids))
    service.users().messages().batchDelete(
            userId='me',
            body={ "ids": ids }
        ).execute()


if __name__ == "__main__":
    main()
