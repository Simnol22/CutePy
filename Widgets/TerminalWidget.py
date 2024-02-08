from Widgets.Widget import Widget
from PySide6.QtWidgets import QLabel, QWidget, QMainWindow
from PySide6 import QtCore

class TerminalWidget(Widget):
    def __init__(self, parent):
        super(TerminalWidget, self).__init__(parent)
        #self.setWindowTitle("Data Widget")
        self.label = QLabel("No data")
        self.layout.addWidget(self.label)
        self.setStyleSheet("border: 1px solid black;")
        #self.setCentralWidget(self.label)
        self.requiredData = ["all"]
        self.latVal = None
        self.lonVal = None
        self.latest = None
        self.resize(300,200)
        self.allData = []
        
    def mode(self,x,y):
        self.move(x,y)
    # Here we are receiving measurements wanted in requiredData. 
    # We need to separate them with the value of the source.
    def setData(self, data):
        found = False
        for i in self.allData:
            if i.source == data.source:
                found = True
                i.value = data.value
        if not found:
            self.allData.append(data)    
        text = " Fake data \n\n"
        for i in self.allData:
            text += i.source + " : " + str(i.value) + "\n"
        self.label.setText(text)

    def refresh(self):
        print("refreshing terminal widget")
        #if self.latVal:
        #text = " Fake data \n\n"
        #for i in self.allData:
        #    text += i.source + " : " + str(i.value) + "\n"
        #self.label.setText(text)
        #self.parent.update()