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

    # onUpdate is called when the widget is updated in the view thread looop
    # This method can be overriden by any widget if wanted.
    # This is not to update the data, but to update the widget itself if necessary
    def onUpdate(self):
        pass 