from Widgets.Widget import Widget
from PySide6.QtWidgets import QLabel, QMainWindow

class DataWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Widget")
        self.label = QLabel("Data Widget")
        self.setCentralWidget(self.label)
        self.data = None
    
    def setData(self, data):
        self.data = data
    
    def refresh(self):
        if self.data:
            self.label.setText(str(self.data))