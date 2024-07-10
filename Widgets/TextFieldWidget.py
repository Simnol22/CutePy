from Widgets.Widget import Widget
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QLineEdit, QLabel, QHBoxLayout, QVBoxLayout

class TextFieldWidget(Widget):
    def __init__(self, parent, label=None, value=None, placeholder=None, position="horizontal"):
        super().__init__(parent)
        self.textField = QLineEdit() # QLineEdit is a text input field
        self.label = label
        if position == "vertical":
            currentLayout = QVBoxLayout()
        else:
            currentLayout = QHBoxLayout()
        self.layout.addLayout(currentLayout)
        if label is not None:
            currentLayout.addWidget(QLabel(parent=self, text=label))
        if value is None and placeholder is not None:
            self.textField.setPlaceholderText(placeholder)   
        else:
            self.textField.setText(value)
        
        currentLayout.addWidget(self.textField, stretch=1)
        self.textField.show()

    def move(self, x, y):
        self.move(x, y)

    def setView(self, view):
        self.view = view
    
    def getValue(self):
        return self.textField.text()
    
