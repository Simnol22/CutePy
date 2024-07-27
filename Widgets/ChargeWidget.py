from Widgets.Widget import Widget
from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget
from PySide6.QtGui import QPainter, QPen, QBrush, QColor
from PySide6.QtCore import Qt

class ChargeWidget(Widget):
    def __init__(self, parent=None, label_text="Charge"):
        super(ChargeWidget, self).__init__(parent)
        
        # Initialize the layout
        self.vlayout = QVBoxLayout(self)
        
        # Create and set the label
        self.label = QLabel(label_text)
        self.label.setAlignment(Qt.AlignCenter)
        self.vlayout.addWidget(self.label)
        
        # Create a QWidget to contain the circle
        self.circle_widget = CircleWidget(self)
        self.vlayout.addWidget(self.circle_widget)
        
        # Setting margins and spacing for better visual appearance
        self.vlayout.setContentsMargins(0, 0, 0, 0)
        self.vlayout.setSpacing(0)
        
        # Initialize charges dictionaries
        self.charges = {}
        self.lastCharges = {}
        self.lastCharge = None
        self.layout.addLayout(self.vlayout)
        
    def setData(self, data):
        for i in self.requiredData:
            if data.source == i:
                self.chargeValue = data.value
                if self.chargeValue != self.lastCharge:
                    self.circle_widget.setCharge(self.chargeValue)
                    self.circle_widget.update()
                    self.lastCharge = self.chargeValue

class CircleWidget(QWidget):
    def __init__(self, parent=None):
        super(CircleWidget, self).__init__(parent)
        self.parent = parent
        self.pen = QPen(Qt.black, 2, Qt.SolidLine)
        self.greenBrush = QBrush(Qt.green, Qt.SolidPattern)
        self.greyBrush = QBrush(Qt.gray, Qt.SolidPattern)
        self.painter = None
        self.charge = 0

    def paintEvent(self, event=None):
        painter = QPainter(self)
        painter.setPen(self.pen)
        if self.charge == 0:
            painter.setBrush(self.greyBrush)
        else:
            painter.setBrush(self.greenBrush)
        h = self.height() / 2
        painter.drawEllipse(self.width() / 2 - h / 2, h/8, 25, 25)
        painter.end()
    
    def setCharge(self, charge=0):
        self.charge = charge