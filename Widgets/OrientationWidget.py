from Widgets.Widget import Widget
from PySide6.QtWidgets import QVBoxLayout, QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QPolygonF
from PySide6.QtCore import Qt, QPointF
import math

class OrientationWidget(Widget):
    def __init__(self, parent=None): 
        super(OrientationWidget, self).__init__(parent)
        
        # Initialize the layout
        self.vlayout = QVBoxLayout(self)
        self.ori = 0.0
        self.orientationDrawWidget =  OrientationDrawWidget(self)
        self.vlayout.addWidget(self.orientationDrawWidget)
        self.layout.addLayout(self.vlayout)

    def setData(self, data):
        for i in self.requiredData:
            if data.source == i:
                self.ori = data.value
                self.orientationDrawWidget.set_orientation(self.ori)

class OrientationDrawWidget(QWidget):
    def __init__(self, parent=None):
        super(OrientationDrawWidget, self).__init__(parent)
        self.parent = parent
        self.ori = 0.0

    def set_orientation(self, ori):
        self.ori = ori
        self.update()

    def paintEvent(self,event=None):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the reference horizontal line
        painter.translate(self.width() / 2, self.height() / 2)  # Move to the center of the widget
        ref_pen = QPen(Qt.black, 2, Qt.DotLine)
        painter.setPen(ref_pen)
        painter.drawLine(QPointF(-50, 0), QPointF(50, 0))  # Draw the dotted line
        
        # Calculate angle based on pitch and roll, adjusting for the specific range
        angle = 90 - self.ori

        # Draw the rocket shape
        painter.rotate(-angle)  # Rotate to the correct angle

        # Set dark green color for the rocket
        rocket_pen = QPen(QColor(0, 100, 0), 4)
        painter.setPen(rocket_pen)

        # Draw the main rocket line
        painter.drawLine(QPointF(-50, 0), QPointF(50, 0))

        # Draw the arrowhead (rocket nose)
        arrowhead = QPolygonF([QPointF(50, 0), QPointF(40, -10), QPointF(40, 10)])
        painter.drawPolygon(arrowhead)

        # Draw the fins (as small angled lines)
        fin_pen = QPen(QColor(0, 100, 0), 4)
        painter.setPen(fin_pen)
        painter.drawLine(QPointF(-40, 0), QPointF(-50, -10))  # Top fin
        painter.drawLine(QPointF(-40, 0), QPointF(-50, 10))   # Bottom fin