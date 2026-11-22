import os
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QButtonGroup, QPushButton
from parts.widgets.fish_calc_app import FishCalcApp


class FishMenuPopup(QWidget):
    def __init__(self, parent: QWidget, bar_height: int):
        super().__init__(parent)

        self.setGeometry(0, self.screen().size().height() - bar_height - 200, 200, 400)
        print(self.geometry().getRect())
        self.setFixedSize(200, 200)

        self.layout = QVBoxLayout(self)
        self.programs_layout = QVBoxLayout()
        self.buttons_layout = QVBoxLayout()

        self.bg = QButtonGroup(self)

        self.exit_button = QPushButton("Выйти из FishOS", self)
        self.restart_button = QPushButton("Перезагрузка", self)
        self.shut_down_button = QPushButton("Выключение", self)

        self.bg.addButton(self.exit_button)
        self.bg.addButton(self.restart_button)
        self.bg.addButton(self.shut_down_button)

        self.buttons_layout.addWidget(self.exit_button)
        self.buttons_layout.addWidget(self.restart_button)
        self.buttons_layout.addWidget(self.shut_down_button)

        self.exit_button.clicked.connect(self.exit)
        self.restart_button.clicked.connect(self.restart)
        self.shut_down_button.clicked.connect(self.shut_down)

        self.layout.addLayout(self.programs_layout)
        self.layout.addLayout(self.buttons_layout)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("""FishMenuPopup {background-color: #00aaff;}""")

        self.programs_layout.addWidget(FishCalcApp(self, parent))

    def toggle(self):
        if self.isHidden():
            self.show()
        else:
            self.hide()

    def exit(self):
        self.parent().exit_app()

    def restart(self):
        if 'win' in sys.platform:
            os.system('shutdown /r /t 0')
        elif 'linux' in sys.platform:
            os.system('reboot')

    def shut_down(self):
        if 'win' in sys.platform:
            os.system('shutdown /s /t 0')
        elif 'linux' in sys.platform:
            os.system('shutdown 0')