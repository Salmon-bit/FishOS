from PyQt6.QtGui import QPicture, QPixmap
from PyQt6.QtWidgets import *


class Desktop(QWidget):
    def __init__(self, parent: QWidget, width, height):
        super().__init__(parent)

        self.bg = QLabel(self)
        self.bg.setPicture(QPixmap())