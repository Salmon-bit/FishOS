import sys
import os
import requests
from PyQt6.QtWidgets import QMessageBox


def download_asset(asset: str, branch: str = 'main') -> bool:
    local_data = '/'
    if sys.platform == 'linux':
        os.makedirs(os.path.join(os.path.expanduser('~'), '.local/share/FishOS'), exist_ok=True)
        local_data = os.path.join(os.path.expanduser('~'), '.local/share/FishOS')
    elif 'win' in sys.platform:
        os.makedirs(os.path.join(os.getenv('LOCALAPPDATA'), 'FishOS'), exist_ok=True)
        local_data = os.path.join(os.getenv('LOCALAPPDATA'), 'FishOS')

    with open(os.path.join(local_data, asset), 'wb') as f:
        try:
            r = requests.get(
                f'https://raw.githubusercontent.com/Salmon-bit/FishOS/refs/heads/{branch}/assets/{asset}')
            if r.status_code == 200:
                f.write(r.content)
            else:
                QMessageBox.critical(
                    None,
                    'Ошибка',
                    "Не удалось скачать файл с сервера.\nПроверьте своё интренет-подключение и попробуйте еще позднее."
                )
                f.close()
                print(f'Error file download: {asset}. Got error: {r.status_code}')
                return False
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(
                None,
                'Ошибка',
                "Не удалось скачать файл с сервера.\nПроверьте своё интренет-подключение и попробуйте еще позднее."
            )
            f.close()
            print(f'Error to connect during downloading {asset}.')
            return False

    return True