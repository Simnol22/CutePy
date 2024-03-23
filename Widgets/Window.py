from PySide6.QtWidgets import QMainWindow
from Widgets.GridWidget import GridWidget
from PySide6.QtWidgets import QWidget

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.grid = GridWidget()
        widget = QWidget()
        widget.setLayout(self.grid)
        self.setCentralWidget(widget)
        self.setWindowTitle("CuteView")


