import sys

from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QResizeEvent, QKeyEvent
from PyQt6.QtWidgets import *

from parts.desktop import Desktop
from parts.down_bar import Bar
from parts.widgets.time import TimeWidget
from parts.widgets.fish_menu import FishMenu

from parts.programs.fish_calc import Calculator

class App(QWidget):
    def __init__(self, app: QApplication):
        super().__init__()

        self.bar = None
        self.desktop = None
        self.app = app

        self.width = 0
        self.height = 0

        self.calc_app = Calculator()
        self.calc_app.hide()

        self.desktop = Desktop(self, self.width, self.height)
        self.desktop.setGeometry(0, 0, self.width, self.height - 50)
        self.desktop.show()

        self.bar = Bar(self, self.width, self.height)
        self.time_widget = TimeWidget(self.bar)
        self.menu = FishMenu(self, 50)

        self.bar.add_tray_widget(self.time_widget)
        self.bar.add_apps_widget(self.menu)
        self.bar.show()

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)

        self.width = event.size().width()
        self.height = event.size().height()

        print(f'Screen size: {self.width}x{self.height}')

        if self.desktop is not None:
            self.desktop.setGeometry(0, 0, self.width, self.height - 50)
            self.desktop.resize_assets(self.width, self.height - 50)
        if self.bar is not None:
            self.bar.update_size(event.size())

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.exit_app()

    def exit_app(self):
        self.app.closeAllWindows()
        self.app.exit(0)

    def getMenu(self) -> FishMenu:
        return self.menu


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = App(app)
    w.showFullScreen()
    sys.exit(app.exec())