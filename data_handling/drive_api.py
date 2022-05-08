from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from googleapiclient.discovery import build
import os
import ast


def get_service():
    """
    Get credentials for Google api from env and returns service object
    :return: service object
    """
    info = ast.literal_eval(os.environ.get('GOOGLE_CREDS'))
    credentials = service_account.Credentials.from_service_account_info(
        info, scopes=['https://www.googleapis.com/auth/drive'])
    service = build('drive', 'v3', credentials=credentials)
    return service


def upload_file(folder_id, file_name, file_path):
    """
    Uploads file to the Google Drive directory
    :param folder_id: Google Drive folder id
    :param file_name: name of the file
    :param file_path: path of the file to be uploaded
    :return: {'id': file_id}
    """
    service = get_service()
    file_metadata = {
                    'name': file_name,
                    'parents': [folder_id]
                }
    media = MediaFileUpload(file_path, resumable=True)
    r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return r
