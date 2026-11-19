import sys
from PyQt6.QtWidgets import *


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.showFullScreen()
        self.size = self.geometry().getRect()
