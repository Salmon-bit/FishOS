import os
import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QMouseEvent, QPixmap
from PyQt6.QtWidgets import QWidget, QLabel


class FishCalcApp(QWidget):
    def __init__(self, parent: QWidget, main):
        super().__init__(parent)

        self.main = main
        self.icon = QLabel("Fish Calc", self)
        local_data = (os.path.join(os.getenv('LOCALAPPDATA'), 'FishOS') if 'win' in sys.platform else
                      os.path.join(os.path.expanduser('~'), '.local/share/FishOS') if 'linux' in sys.platform else '')
        self.icon.setPixmap(QPixmap(os.path.join(local_data, 'calc.png')))

        self.minimumSize(QSize(200, 50))
        self.setMaximumHeight(50)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.main.calc_app.toggle()