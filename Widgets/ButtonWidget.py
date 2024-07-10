from Widgets.Widget import Widget
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton

class ButtonWidget(Widget):
    def __init__(self, parent, label, command=None):
        super().__init__(parent)
        self.command = command
        self.label = label
        self.fieldName = None
        self.button = QPushButton(label)
        self.button.clicked.connect(self.pressed)
        self.layout.addWidget(self.button)
        self.button.show()

    def setFieldName(self, fieldname = None):
        self.fieldName = fieldname

    def move(self, x, y):
        self.move(x, y)

    def setView(self, view):
        self.view = view
    
    def pressed(self):
        if self.command:
            val = None

            if self.fieldName is not None:
                if isinstance(self.fieldName, str): 
                    val = self.view.getFieldValue(self.fieldName)
                    self.view.sendCommand(self.command, val)
                else:
                    tabval = []
                    for i in self.fieldName:
                        tabval.append(self.view.getFieldValue(i))
                    self.view.sendCommand(self.command, tabval)
            else:
                self.view.sendCommand(self.command, val)
            
    
