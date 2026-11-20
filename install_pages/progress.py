from threading import Thread
from PyQt6.QtCore import QRect
from PyQt6.QtGui import QIcon, QFont, QCloseEvent
from PyQt6.QtWidgets import *


class ProgressWindow(QWidget):
    def __init__(self, icon: QIcon, steps: int):
        super().__init__()

        self.steps = steps
        self.done_steps = 0

        self.setWindowTitle("Статус установки")
        self.setGeometry(300, 300, 500, 200)
        self.setWindowIcon(icon)
        self.setMinimumSize(500, 200)
        self.setMaximumSize(500, 200)

        self.verticalLayout = QVBoxLayout(self)

        self.title = QLabel('Установка FishOS...', self)
        self.title.setFont(QFont('Courier new', 10))

        self.verticalLayout.addWidget(self.title)

        sp = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.verticalLayout.addSpacerItem(sp)

        self.progressBar = QProgressBar(self)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)
        self.progressBar.setMinimum(0)

        self.verticalLayout.addWidget(self.progressBar)
        self.verticalLayout.setGeometry(QRect(0, 0, 500, 200))

    def addValue(self, value: int):
        self.progressBar.setValue(self.progressBar.value() + value)

    def next(self):
        if self.done_steps + 1 == self.steps:
            self.addValue(100 - self.progressBar.value())
        else:
            self.addValue(round(100 / self.steps))

    def closeEvent(self, event: QCloseEvent):
        if self.progressBar.value() == 100:
            event.accept()
        else:
            event.ignore()