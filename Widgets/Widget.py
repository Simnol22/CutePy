from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6 import QtCore
from PySide6.QtCore import Signal

class Widget(QWidget):
    refreshSignal = Signal()
    measurementSignal = Signal(object)

    def __init__(self, parent):
        super(Widget, self).__init__(parent)
        self.parent = parent
        self.name = None
        self.layout = QVBoxLayout()
        #self.setStyleSheet("border: 1px solid black;")
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)
        self.requiredData = []
        # Connecter le signal au slot 
        self.refreshSignal.connect(self.refresh)
        self.measurementSignal.connect(self.setData)

    def setSource(self, source):
        #If we have only one source (a string), we need to put it in a list
        if isinstance(source, str):
            self.requiredData = [source]
        else:
            self.requiredData = source
    
    def refreshData(self):
        self.refreshSignal.emit()
    
    def refresh(self):
        pass
    
    def measurementData(self, data):
        self.measurementSignal.emit(data)

    def setData(self, data):
        pass
    # onUpdate is called when the widget is updated in the view thread looop
    # This method can be overriden by any widget if wanted.
    # This is not to update the data, but to update the widget itself if necessary
    def onUpdate(self):
        pass 

