from PySide6.QtWidgets import QWidget, QVBoxLayout

class Widget(QWidget):
    def __init__(self, name):
        self.parent = None
        self.name = name