import os
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import *


class Desktop(QWidget):
    def __init__(self, parent: QWidget, width, height):
        super().__init__(parent)

        self.assets_folder = ''
        if sys.platform == 'linux':
            self.assets_folder = os.path.join(os.path.expanduser('~'), '.local/share/FishOS')
        elif 'win' in sys.platform:
            self.assets_folder = os.path.join(os.getenv('LOCALAPPDATA'), 'FishOS')

        self.bg = QLabel(self)
        self.bg.setScaledContents(True)

        wallpaper_path = os.path.join(self.assets_folder, 'wallpaper.jpg')
        if os.path.exists(wallpaper_path):
            self.bg.setPixmap(QPixmap(wallpaper_path))
        else:
            self.setStyleSheet("Desktop { background-color: rgb(30, 30, 30); }")
            self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.resize_assets(width, height)

    def resize_assets(self, width: int, height: int):
        self.bg.setGeometry(0, 0, width, height)