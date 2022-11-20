# ---------------------------------------------------------------------

import os
from datetime import datetime as dt


# ---------------------------------------------------------------------

def create_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


def to_cur_dir():
    os.chdir('..')


def file_newer(file_name: str, server_time: str):
    if os.path.exists(file_name):
        ctime = dt.fromtimestamp(os.path.getctime(file_name))
        local_time = ctime.strftime('%Y-%m-%dT%H:%M:%S')

        return local_time >= server_time
    return False

# ---------------------------------------------------------------------
