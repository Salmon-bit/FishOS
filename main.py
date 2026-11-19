import sys
from PyQt6.QtWidgets import *


class App(QWidget):
    def __init__(self):
        super().__init__()

        QMessageBox.information(self, "Message", "Hello World")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = App()
    w.show()
    sys.exit(app.exec())
