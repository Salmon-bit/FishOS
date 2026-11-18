import sys
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
            QMessageBox.information(self, "Warning", "Пожалуйста, примите пользовательское соглашение и\
 подтведтите, что вы отдаёте отчет своим действиям.")
            return
        print("Installing FishOS")

        # Some code

        self.installed = True
        QMessageBox.information(self, "Информация", "FishOS успешно утсановлена на ваш ПК.\nСпасибо, что выбираете нас!")

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