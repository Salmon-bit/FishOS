import sys
import os
import requests
from PyQt6.QtWidgets import QMessageBox


def _get_local_data() -> str:
    """Возвращает папку для данных FishOS, создавая её при необходимости."""
    if sys.platform == 'linux':
        local_data = os.path.join(os.path.expanduser('~'), '.local/share/FishOS')
    elif 'win' in sys.platform:
        local_data = os.path.join(os.getenv('LOCALAPPDATA'), 'FishOS')
    else:
        local_data = os.path.join(os.path.expanduser('~'), 'FishOS')

    os.makedirs(local_data, exist_ok=True)
    return local_data


def download_asset(asset: str, branch: str = 'main') -> bool:
    local_data = _get_local_data()
    dest_path = os.path.join(local_data, asset)

    # Создаём подпапки, если asset содержит вложенный путь (например, widgets/foo.png)
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    url = f'https://raw.githubusercontent.com/Salmon-bit/FishOS/refs/heads/{branch}/assets/{asset}'

    try:
        r = requests.get(url, timeout=30)
    except requests.exceptions.RequestException as e:
        QMessageBox.critical(
            None,
            'Ошибка',
            "Не удалось скачать файл с сервера.\nПроверьте своё интернет-подключение и попробуйте ещё позднее."
        )
        print(f'Error to connect during downloading {asset}: {e}')
        return False

    if r.status_code != 200:
        QMessageBox.critical(
            None,
            'Ошибка',
            "Не удалось скачать файл с сервера.\nПроверьте своё интернет-подключение и попробуйте ещё позднее."
        )
        print(f'Error file download: {asset}. Got error: {r.status_code}')
        return False

    with open(dest_path, 'wb') as f:
        f.write(r.content)

    return True