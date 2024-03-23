from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6 import QtCore

class Widget(QWidget):
    def __init__(self, parent):
        super(Widget, self).__init__(parent)
        self.parent = parent
        self.name = None
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)
