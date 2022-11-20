# ---------------------------------------------------------------------

import libs.google_api as gapi
import libs.yandex_api as yapi
import libs.helper as hlp

import schedule as sch
import time


# ---------------------------------------------------------------------

@sch.repeat(sch.every().monday.at("08:00"))
def load_files():
    service = gapi.get_service()
    hlp.to_cur_dir()

    gapi.load_files(service)
    yapi.load_files()


if __name__ == '__main__':
    while True:
        sch.run_pending()
        time.sleep(5)

# ---------------------------------------------------------------------
