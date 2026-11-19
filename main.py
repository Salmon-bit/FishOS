import sys
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import *
from down_bar import Bar
from widgets.time import TimeWidget


class App(QWidget):
    def __init__(self):
        self.bar = None

        super().__init__()

        self.width = 0
        self.height = 0

        self.bar = Bar(self, self.width, self.height)
        self.time_widget = TimeWidget(self.bar)

        self.bar.add_tray_widget(self.time_widget)

        # Should be at the end of __init__!!!
        self.showFullScreen()

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)

        self.width = event.size().width()
        self.height = event.size().height()

        print(f'Screen size: {self.width}x{self.height}')

        if self.bar is not None:
            self.bar.update_size(event.size())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = App()
    w.show()
    sys.exit(app.exec())
