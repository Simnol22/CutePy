from Widgets.Widget import Widget
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QLabel
class TextWidget(Widget):
    def __init__(self, parent, mapping, nbLines=1):
        super().__init__(parent)
        self.texts = []
        self.mapping = mapping
        self.vlayout = QVBoxLayout(self)
        self.nbLines = nbLines
        self.counter = 0
        #Adding all Qlabels to the layout, empty by default
        for i in range(nbLines):
            text = QLabel()
            self.texts.append(text) 
            self.vlayout.addWidget(text)
        self.vlayout.addStretch()
        self.layout.addLayout(self.vlayout)

    def setData(self, data):
        for i in self.requiredData:
            if data.source == i:
                self.addNewValue(int(data.value))

    def addNewValue(self, value):
        #Shift all the values of the list, adding the new value at the end
        for i in range(self.nbLines - 1):
            self.texts[i].setText(self.texts[i + 1].text())
        self.texts[self.nbLines - 1].setText(str(self.counter) + ", " + self.mapping[str(value)])
        self.counter += 1