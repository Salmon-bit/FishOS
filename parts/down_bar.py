import sys
from PyQt6.QtCore import Qt, QRect, QSize
from PyQt6.QtWidgets import *
from widgets.time import TimeWidget


class Bar(QWidget):
    def __init__(self, parent, width, height, bar_height=50):
        super().__init__(parent)

        self.bar_height = bar_height
        self.win_width = width
        self.win_height = height

        # Разрешаем QWidget отрисовывать фон из StyleSheet
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("Bar { background-color: rgb(0, 50, 255); color: white; }")

        self.layout = QHBoxLayout(self)
        self.tray = QHBoxLayout()
        self.apps = QHBoxLayout()

        self.layout.addLayout(self.apps)
        self.layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.layout.addLayout(self.tray)

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.update_size(QSize(width, height))

    def add_tray_widget(self, widget: QWidget):
        self.tray.addWidget(widget)

    def add_apps_widget(self, widget: QWidget):
        self.apps.addWidget(widget)

    def update_size(self, size: QSize):
        self.win_width = size.width()
        self.win_height = size.height()

        self.setFixedSize(self.win_width, self.bar_height)

        if self.parent() is not None:
            self.move(0, self.win_height - self.bar_height)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    bar = Bar(None, 2560, 1080, 50)
    bar.add_tray_widget(TimeWidget(bar))
    bar.show()
    sys.exit(app.exec())
