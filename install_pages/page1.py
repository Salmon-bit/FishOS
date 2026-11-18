from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import *

SIZE = (640, 480)
DESCRIPTION = """\
В процессе установки данной программы, будет установлена прекрасная система: FishOS.
Благодарим вас за выбор нашей системы!"""
PS = """\
P.S. Салманская империя не несет ответственности за дальнейшее сосотояние вашего ПК."""


class Page1(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.setGeometry(0, 0, *SIZE)

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setGeometry(QRect(10, 10, SIZE[0] - 20, SIZE[1] - 20))

        self.title = QLabel("Установщик FishOS", self)
        self.title.setFont(QFont("Curier New", 20))
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.title)

        s0 = QSpacerItem(0, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self.verticalLayout.addSpacerItem(s0)

        self.legend = QLabel(DESCRIPTION, self)
        self.legend.setFont(QFont("Curier New", 15))
        self.legend.setWordWrap(True)
        self.verticalLayout.addWidget(self.legend)

        s1 = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.verticalLayout.addSpacerItem(s1)

        self.hl = QHBoxLayout()

        self.next_btn = QPushButton("Далее", self)
        self.next_btn.setFont(QFont("Curier New", 12))
        self.next_btn.setMaximumSize(200, 30)
        self.hl.addWidget(self.next_btn)

        self.verticalLayout.addLayout(self.hl)

        self.ps = QLabel(PS, self)
        self.ps.setFont(QFont("Curier New", 8))
        self.ps.setWordWrap(True)
        self.ps.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.ps)