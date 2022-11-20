# ---------------------------------------------------------------------

import config as cfg
import libs.helper as hlp

from google.oauth2.service_account import Credentials
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from io import FileIO


# ---------------------------------------------------------------------

def get_service():
    creds = Credentials.from_service_account_file(
        cfg.SERVICE_ACCOUNT, scopes=cfg.SCOPES)

    return build('drive', 'v3', credentials=creds)


def load_files(service):
    files = __get_files(service)

    for file in files:
        if file['mimeType'] != 'application/vnd.google-apps.folder':
            file_name = file['name']
            path = 'files\\' + __get_email(file) + __get_path(file, files)

            hlp.create_dir(path)
            full_name = path + '\\' + file_name

            if hlp.file_newer(full_name, file['modifiedTime'][:-5]):
                print(f'Файл "{file_name}" уже существует!')
                continue
            else:
                done = False
                request = service.files().get_media(fileId=file['id'])
                loader = MediaIoBaseDownload(FileIO(full_name, 'wb'), request)

                while not done:
                    _, done = loader.next_chunk()
                print(f'Файл "{file_name}" успешно загружен!\n')

    print('Загрузка успешно завершена!\n')


# ---------------------------------------------------------------------

def __get_files(service, page_size=10):
    attrs = 'id, name, mimeType, permissions, modifiedTime, parents'
    fields = f'nextPageToken, files({attrs})'

    results = service.files().list(
        pageSize=page_size,
        fields=fields).execute()

    next_token = results.get('nextPageToken')

    while next_token:
        next_page = service.files().list(
            pageSize=page_size,
            fields=fields,
            pageToken=next_token).execute()

        next_token = next_page.get('nextPageToken')
        results['files'] += next_page['files']

    return results['files']


def __get_path(file: dict, files: list, path=''):
    if 'parents' in file.keys():
        parent = [f for f in files if f['id'] == file['parents'][0]][0]
        path = __get_path(parent, files, path) + '\\' + parent['name']
    return path


def __get_email(file: dict):
    perms = file['permissions']
    return [p['emailAddress'] for p in perms if p['role'] == 'owner'][0]

# ---------------------------------------------------------------------
