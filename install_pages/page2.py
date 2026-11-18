from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import *

SIZE = (640, 480)

class Page2(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.setGeometry(0, 0, *SIZE)
        self.counter = 0

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setGeometry(QRect(10, 10, SIZE[0] - 20, SIZE[1] - 20))

        self.title = QLabel("Установщик FishOS", self)
        self.title.setFont(QFont("Curier New", 20))
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.title)

        sp0 = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.verticalLayout.addSpacerItem(sp0)

        self.cb1 = QCheckBox("Согласен с пользовательским соглашением", self)
        self.cb2 = QCheckBox("Полностью отдаю отчет своим действиям", self)
        self.cb3 = QCheckBox("Добровольно устанавливаю данную ОС", self)
        self.cb3.setChecked(True)

        self.cb1.setObjectName('cb1')
        self.cb2.setObjectName('cb2')
        self.cb3.setObjectName('cb3')

        self.verticalLayout.addWidget(self.cb1)
        self.verticalLayout.addWidget(self.cb2)
        self.verticalLayout.addWidget(self.cb3)

        hl = QHBoxLayout()
        self.install_button = QPushButton("Установить", self)
        hl.addWidget(self.install_button)

        self.verticalLayout.addLayout(hl)

        self.cb3.clicked.connect(self.cb3_click)

    def cb3_click(self):
        if not self.cb3.isChecked():
            self.cb3.setChecked(True)

            if self.counter >= 1:
                QMessageBox.critical(
                    self,
                    "Ошибка",
                    "Мы вас предупреждали."
                )
                return

            QMessageBox.information(
                self,
                "Предупреждение",
                "Вы не можете быть против системы, ведь так?\n\
Если ваши действия повторятся, для вас это плохо кончится."
            )

            self.counter += 1