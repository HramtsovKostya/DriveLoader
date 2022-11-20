# ---------------------------------------------------------------------

import config as cfg
import libs.helper as hlp
import requests as rq


# ---------------------------------------------------------------------


def load_files():
    url = cfg.HOST_NAME + '/v1/disk/resources/download'

    for headers in __get_headers():
        for file in __get_files(headers):
            path = file['path'].removeprefix('disk:/')
            file_name = path[path.rfind('/') + 1:]

            resp = rq.get(url, params={'path': path}, headers=headers)
            href = resp.json()['href']

            path = path[:path.rfind('/')] if path.rfind('/') > 0 else ''
            path = 'files/' + __get_email(headers) + path

            hlp.create_dir(path)
            full_name = path + '/' + file_name

            if hlp.file_newer(full_name, file['modified'][:-5]):
                print(f'Файл "{file_name}" уже существует!')
                continue
            else:
                with open(full_name, 'wb') as f:
                    f.write(rq.get(href).content)
                    print(f'Файл "{file_name}" успешно загружен!')

    print('Загрузка успешно завершена!\n')


def __get_files(headers: dict):
    url = cfg.HOST_NAME + '/v1/disk/resources/files'

    fields = ', '.join([
        'items.resource_id',
        'items.name',
        'items.mime_type',
        'items.modified',
        'items.path'
    ])

    resp = rq.get(url, params={'fields': fields}, headers=headers)
    return resp.json()['items']


def __get_email(headers: dict):
    url = cfg.HOST_NAME + '/v1/disk'
    resp = rq.get(url, params={'fields': 'user.login'}, headers=headers)

    login = resp.json()['user']['login']
    return login + '@yandex.ru/'


def __get_headers():
    return [{
        'Accept': 'application/json',
        'Authorization': f'OAuth {token}'
    } for token in cfg.TOKENS]

# ---------------------------------------------------------------------
