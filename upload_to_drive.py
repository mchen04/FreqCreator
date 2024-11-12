from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
import os

# Set up Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = 'credentials.json'

creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=creds)

# Specify the folder ID where you want to upload files
folder_id = 'YOUR_GOOGLE_DRIVE_FOLDER_ID'

def upload_to_drive(file_name):
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_name, mimetype='audio/mpeg')
    service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f'Uploaded {file_name} to Google Drive')

# Upload each MP3 file to Google Drive
for file in os.listdir():
    if file.endswith(".mp3"):
        upload_to_drive(file)
        os.remove(file)  # Optionally delete local file after upload
