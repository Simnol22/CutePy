from PySide6.QtWidgets import QLabel, QMainWindow
from PySide6.QtGui import QPainter

class CompassWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.radius = 0
        self.setWindowTitle("Compass Widget")

    
    def drawBackground(self,painter,scale):
        pass

    def drawTarget(self,painter,scale):
        pass