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

        self.page1 = page1.Page1(self)
        self.setLayout(self.page1.verticalLayout)
        self.page1.show()

        self.page2 = page2.Page2(self)
        self.page2.hide()

        self.page1.next_btn.pressed.connect(self.page_1_to_2)

    def page_1_to_2(self):
        self.page2.show()

        self.page2.install_button.clicked.connect(self.install)

    def install(self):
        print("Installing FishOS")

    def closeEvent(self, a0: QtGui.QCloseEvent | None, /) -> None:
        if not self.installed:
            a0.ignore()
        else:
            a0.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    install_window = InstallWindow()
    install_window.show()

    sys.exit(app.exec())