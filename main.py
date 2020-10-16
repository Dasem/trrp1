from __future__ import print_function

import io
import os.path
import pickle

from cryptography.fernet import Fernet
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

from constants import *


def auth():
    global service
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    f = Fernet(KEY)

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.loads(f.decrypt(token.read()))
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'test_user.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            data_for_write = pickle.dumps(creds)
            token.write(f.encrypt(data_for_write))

    return build('drive', 'v3', credentials=creds)


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']
service = auth()


def upload_file(name, remote_name):
    file_metadata = {'name': remote_name}
    media = MediaFileUpload(name)

    file = service.files().create(body=file_metadata,
                                  media_body=media).execute()
    print("File successfully uploaded")
    return file


def delete_file(id):
    service.files().delete(fileId=id).execute()
    print("File successfully deleted")


def change_file_name():
    id = input("Input file id:")
    name = input("Input new file name:")

    try:
        temp_name = "temp_name"
        download_file(id, temp_name)
        delete_file(id)
        upload_file(temp_name, name)
    except Exception as ex:
        print("Something going wrong", ex)
        return

    print("File name successfully changed")


def download_file(id, name):
    try:
        request = service.files().get_media(fileId=id)
        fh = io.FileIO(name, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
    except Exception as ex:
        print("File with this id doesn't exist", ex)


def show_list():
    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])


    result = ''
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            result += u'{0} ({1});'.format(item['name'], item['id'])
            print(u'{0} ({1})'.format(item['name'], item['id']))

    return result


def user_menu():
    command = "0"
    while command != MENU_EXIT:
        print(MENU)
        command = input()
        if command == MENU_LIST:
            show_list()
        elif command == MENU_DOWNLOAD:
            download_file(input("Input file id:"), input("Input file name for save:"))
        elif command == MENU_UPLOAD:
            upload_file_name = input("Input file name:")
            upload_file(upload_file_name, upload_file_name)
        elif command == MENU_CHANGE:
            change_file_name()
        elif command == MENU_DELETE:
            delete_file(input("Input file id:"))
        elif command == MENU_EXIT:
            break
        else:
            print(UNEXPECTED_INPUT)


if __name__ == '__main__':
    auth()
    user_menu()
