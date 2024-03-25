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
        self.requiredData = []
    
    def setSource(self, source):
        #If we have only one source (a string), we need to put it in a list
        if isinstance(source, str):
            self.requiredData = [source]
        else:
            self.requiredData = source
    
    # onUpdate is called when the widget is updated in the view thread looop
    # This method can be overriden by any widget if wanted.
    # This is not to update the data, but to update the widget itself if necessary
    def onUpdate(self):
        pass 

