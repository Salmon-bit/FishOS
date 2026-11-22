import os
import sys
from PyQt6.QtCore import Qt, QRect, pyqtSignal
from PyQt6.QtGui import QPixmap, QMouseEvent
from PyQt6.QtWidgets import QWidget, QLabel
from parts.widgets.pop_up_menu import FishMenuPopup


class FishMenu(QWidget):
    def __init__(self, parent: QWidget, bar_height: int):
        super().__init__(parent)

        self.popup = FishMenuPopup(parent, 50)
        self.popup.hide()
        self.bar_height = bar_height

        local_data = ''
        if 'win' in sys.platform:
            local_data = os.path.join(os.getenv("LOCALAPPDATA"), "FishOS")
        elif sys.platform == 'linux':
            local_data = os.path.join(os.path.expanduser('~'), '.local/share/FishOS')

        self.icon = QLabel(self)
        self.icon.setPixmap(QPixmap(os.path.join(local_data, 'fos_ICON.png')))
        self.icon.setScaledContents(True)

        self.setFixedSize(bar_height, bar_height)
        self.icon.setGeometry(QRect(0, 0, bar_height, bar_height))

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.popup.toggle()