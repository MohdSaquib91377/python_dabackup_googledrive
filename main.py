import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import service.mail as mail
from datetime import datetime 
# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/drive.metadata.readonly",
    "https://www.googleapis.com/auth/drive.file"
]

class GoogleDrive:

    def get_token(self) -> Credentials:
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        return creds

    def read_files(self):
        creds = self.get_token()
        try:
            service = build("drive", "v3", credentials=creds)

            # Call the Drive v3 API
            results = (
                service.files()
                .list(pageSize=10, fields="nextPageToken, files(id, name)")
                .execute()
            )
            items = results.get("files", [])

            if not items:
                print("No files found.")
                return
            print("Files:")
            for item in items:
                print(f"{item['name']} ({item['id']})")
        except HttpError as error:
            # TODO - Handle errors from drive API.
            print(f"An error occurred: {error}")

    def upload_file(self, file_path, folder_id=None):
        creds = self.get_token()
        service = build("drive", "v3", credentials=creds)
        """Uploads a file to Google Drive."""
        file_metadata = {"name": os.path.basename(file_path)}
        if folder_id:
            file_metadata["parents"] = [folder_id]
        media = MediaFileUpload(file_path, resumable=True)
        try:
            file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
            file_id = file.get('id')
            file_url = f"https://drive.google.com/file/d/{file_id}/view"
            return file_id, file_url
        except HttpError as error:
            # Handle errors from drive API.
            print(f"An error occurred: {error}")

gd_obj = GoogleDrive()

if __name__ == "__main__":
    try:
        home_dir = os.path.expanduser("~/")
        folder_dir = os.path.join('projects/database/')
        database_file = os.listdir(f'{home_dir}{folder_dir}')[0]
        full_path = f"{home_dir}{folder_dir}/{database_file}"
        file_id,file_link = gd_obj.upload_file(full_path,"1EC3FegrKq4XjGVlf2RHJWGe2vt58CnYV")
        mail.send_mail(
            to_email=[os.getenv('RECEIVER_EMAIL')],  # Replace with recipient's email address
            subject='Recieve kaya database backup file link',
            message=f'kaya database backup file uploaded on google drive at {datetime.now()}. please find google drive link to view {file_link}'
        )
    except Exception as e:
        print(f'Error occurred: {e}')
