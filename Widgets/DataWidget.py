from Widgets.Widget import Widget
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt

class DataWidget(Widget):
    def __init__(self, parent, position="vertical"):
        super(DataWidget, self).__init__(parent)
        self.dataLabel = QLabel("Not initialised")
        self.layout.addWidget(self.dataLabel,alignment=Qt.AlignCenter)
        #self.setStyleSheet("border: 1px solid black;")
        self.dataValue = "No value"
        self.label = "No label"
        self.unit = ""
        self.round = 2
        self.requiredData = []
        self.delimiter = "\n" if position == "vertical" else " : "
        self.updateDataLabel()

    def setLabel(self, text):
        self.label = text

    def setUnit(self, unit):
        self.unit = unit

    def setRounding(self, round):
        self.round = round

    def move(self,x,y):
        self.move(x,y)

    def updateDataLabel(self):
        self.dataLabel.setText(self.label + self.delimiter + self.dataValue + " "+ self.unit)

    # Here we are receiving measurements wanted in requiredData. 
    # We need to separate them with the value of the source.
    def setData(self, data):
        for i in self.requiredData:
            if data.source == i:
                self.dataValue = str(round(data.value,2))
                # Update the data label when recieving new data
                self.updateDataLabel()
