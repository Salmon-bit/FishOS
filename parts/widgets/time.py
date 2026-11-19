import datetime as dt
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout


class TimeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(2)

        self.time = QLabel(self)
        self.time.setFont(QFont("Arial", 14))
        self.time.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.date = QLabel(self)
        self.date.setFont(QFont("Arial", 9))
        self.date.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.time)
        self.layout.addWidget(self.date)

        self.setMinimumWidth(100)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(10)

        # Вызываем сразу при создании, чтобы не ждать первую секунду
        self.update_time()

    def update_time(self):
        now = dt.datetime.now()
        self.time.setText(now.strftime("%H:%M"))
        self.date.setText(now.strftime("%d.%m.%Y"))
