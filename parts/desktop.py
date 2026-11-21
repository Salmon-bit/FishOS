import os
from PyQt6.QtGui import QPicture, QPixmap
from PyQt6.QtWidgets import *
import sys


class Desktop(QWidget):
    def __init__(self, parent: QWidget, width, height):
        super().__init__(parent)

        self.assets_folder = ''
        if sys.platform == 'linux':
            self.assets_folder = os.path.join(os.path.expanduser('~'), '.local/share/FishOS')

        self.bg = QLabel(self)
        self.bg.setPixmap(QPixmap(os.path.join(self.assets_folder, 'wallpaper.jpg')))
        self.bg.setGeometry(0, 0, width, height)