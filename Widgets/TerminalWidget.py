from Widgets.Widget import Widget
from PySide6.QtWidgets import QLabel

class TerminalWidget(Widget):
    def __init__(self, parent):
        super(TerminalWidget, self).__init__(parent)
        self.Terminallabel = QLabel("No terminal data")
        self.label = "No Label"
        self.layout.addWidget(self.Terminallabel)
        self.setStyleSheet("border: 1px solid black;")
        self.requiredData = []
        self.allData = []
        self.round = 2

    def setLabel(self, text):
        self.label = text

    def setRounding(self, round):
        self.round = round

    def move(self,x,y):
        self.move(x,y)
    
    def updateTerminalLabel(self):
        textLabel = self.label + "\n"
        for i in self.allData:
            textLabel += i.source + " : " + str(i.value) + "\n"
        self.Terminallabel.setText(textLabel)
    
    # Here we are receiving measurements wanted in requiredData. 
    # We need to separate them with the value of the source.
    def setData(self, data):
        for sources in self.requiredData:
            if data.source == sources or sources == "all":
                found = False
                for i in self.allData:
                    if i.source == data.source:                         
                        found = True
                        i.value = str(round(data.value,self.round))
                if not found:
                    self.allData.append(data)
                # Update the data label when recieving new data
                self.updateTerminalLabel()