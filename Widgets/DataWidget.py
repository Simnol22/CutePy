from Widgets.Widget import Widget
from PySide6.QtWidgets import QLabel

class DataWidget(Widget):
    def __init__(self, parent):
        super(DataWidget, self).__init__(parent)
        self.dataLabel = QLabel("Not initialised")
        self.layout.addWidget(self.dataLabel)
        self.setStyleSheet("border: 1px solid black;")
        self.dataValue = "No value"
        self.label = "No label"
        self.unit = ""
        self.round = 2
        self.requiredData = []
        self.updateDataLabel()

    def setLabel(self, text):
        self.label = text

    def setSource(self, source):
        self.requiredData = [source]

    def setUnit(self, unit):
        self.unit = unit

    def setRounding(self, round):
        self.round = round

    def move(self,x,y):
        self.move(x,y)

    def updateDataLabel(self):
        self.dataLabel.setText(self.label + "\n" + self.dataValue + " "+ self.unit)

    # Here we are receiving measurements wanted in requiredData. 
    # We need to separate them with the value of the source.
    def setData(self, data):
        self.data = data
        for i in self.requiredData:
            if data.source == i:
                self.dataValue = str(round(data.value,self.round))
                # Update the data label when recieving new data
                self.updateDataLabel()
