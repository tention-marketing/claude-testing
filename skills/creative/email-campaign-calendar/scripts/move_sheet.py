#!/usr/bin/env python3
"""
Move a Google Sheet (or any Drive file) into a target folder.
Removes all current parents and sets the new one.

Usage:
  python3 move_sheet.py SHEET_ID TARGET_FOLDER_ID
"""
import sys, json, warnings
warnings.filterwarnings('ignore')
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN = '/home/rajeev/.hermes/google_token.json'

def move_file(file_id, target_folder_id):
    creds = Credentials.from_authorized_user_file(TOKEN)
    service = build('drive', 'v3', credentials=creds)

    meta = service.files().get(fileId=file_id, fields='parents').execute()
    prev_parents = ','.join(meta.get('parents', []))

    result = service.files().update(
        fileId=file_id,
        addParents=target_folder_id,
        removeParents=prev_parents,
        fields='id, parents'
    ).execute()

    print(json.dumps({'moved': True, 'file_id': file_id, 'new_parents': result.get('parents', [])}))

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: move_sheet.py FILE_ID TARGET_FOLDER_ID')
        sys.exit(1)
    move_file(sys.argv[1], sys.argv[2])
