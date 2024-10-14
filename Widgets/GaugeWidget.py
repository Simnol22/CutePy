"""
Gauge widget :
Displays the evoluation of a value thanks to a dial and a needle.

Config:
* Mandatory *
model : 1 or 2, select the gauge model you want
height : height of teh widget
width : width of the widget
limit : maximum value displayed on the dial
step : step between values on the dial 

* Optional * 
arcWidth : width of the dial's arc
needleWidth : width of the needle
labelFontSize : font size of the label displaying real time speed
scaleFontSize : font size of the scales on the dial 
scaleDistance : distance bewteen the scales and the dial's arc
"""

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPainter, QPen, QFont, QTransform
from PySide6.QtCore import Qt, QRectF
from Widgets.Widget import Widget
import math

class GaugeWidget(Widget):
    def __init__(self, model=1, parent=None):
        super(GaugeWidget, self).__init__(parent)
        # Initialize the layout
        self.model = model
        self.vlayout = QVBoxLayout()
        self.gaugeDrawWidget = GaugeDrawWidget(self.model, self)
        self.vlayout.addWidget(self.gaugeDrawWidget)
        self.layout.addLayout(self.vlayout)
    
    def setData(self, data):
        for i in self.requiredData:
            if data.source == i:
                self.ori = data.value
                self.gaugeDrawWidget.set_value(self.ori)
    
    def setLimit(self, limit_):
        self.gaugeDrawWidget.limit = limit_

    def setStep(self, step_):
        self.gaugeDrawWidget.step = step_

    def setLabelFontSize(self, label_font_size):
        self.gaugeDrawWidget.speed_label.setStyleSheet(f"font-size: {label_font_size}px;")
    
    def setNeedleWidth(self, needle_width_):
        self.gaugeDrawWidget.needle_width = needle_width_
    
    def setArcWidth(self, arc_width_):
        self.gaugeDrawWidget.arc_width = arc_width_
    
    def setScaleFontSize(self, scale_font_size_):
        self.gaugeDrawWidget.scale_font_size = scale_font_size_
    
    def setScaleDistance(self, scale_distance_):
        self.gaugeDrawWidget.scale_distance = scale_distance_

class GaugeDrawWidget(QWidget):
    def __init__(self, model=1, parent=None):
        super(GaugeDrawWidget, self).__init__(parent)

        self.model = model
        self.step = 0
        self.limit = 0
        self.value = 0
        self.speed_label = QLabel('000 km/h', self)
        self.speed_label.setStyleSheet("font-size: 12px;")
        self.needle_width = 5
        self.arc_width = 8
        self.scale_font_size = 8
        self.scale_distance = 20

        
        #Type1
        self.angle = 180
        self.angleAdjust = 0
        self.start_angle = 0
        self.span_angle = self.angle * 16
        self.negAngleLimit = -self.angle/2
        self.posAngleLimit = self.angle/2
        self.labelHeight = 2
        

    def set_value(self, value):
        self.value = int(value)
        # Met à jour le texte de l'étiquette de vitesse
        text = f'{self.value:03d} km/h' if self.value < 100 else f'{self.value} km/h'
        self.speed_label.setText(text)
        self.update()
    
    def paintEvent(self, event=None):
        width = self.width()
        height = self.height()

        if self.model == 2:
            
            self.angle = 270
            self.angleAdjust = 45
            self.start_angle = -45 * 16
            self.span_angle = self.angle * 16
            self.negAngleLimit = -self.angle/2
            self.posAngleLimit = self.angle/2
            height = height/2
            self.labelHeight = 1.5
        
        self.speed_label.move(width // 2 - self.speed_label.width() // 2, height // self.labelHeight - self.speed_label.height() // 2)

        # Dessiner la jauge
        painter = QPainter(self)
        rect = QRectF(5, 5, width - 10, height * 2 - 10)

        # Dessiner le fond de la jauge
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.black, self.arc_width))
        painter.drawArc(rect, self.start_angle, self.span_angle)

        # Dessiner les graduations et les étiquettes
        painter.setPen(QPen(Qt.black, 2))
        font = QFont("Arial", self.scale_font_size)
        painter.setFont(font)
        step = int(self.limit / self.step)
        for i in range(0, step+1):
            angle = self.angle * (i / step) - self.angleAdjust
            radians = math.radians(angle)
            x = width / 2 + (width / 2 - self.scale_distance) * -math.cos(radians)
            y = height - (height - self.scale_distance) * math.sin(radians)
            painter.drawText(x - 5, y, f'{i * self.step}')

        # Dessiner l'aiguille
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.red)

        # Calculer l'angle de l'aiguille en fonction de la valeur de la vitesse (0-100 km/h)
        if (self.value / self.limit) > 1:
            angle = self.posAngleLimit
        elif (self.value / self.limit) < 0:
            angle = -self.negAngleLimit
        else:
            angle = self.angle * (self.value / self.limit) - self.angle/2  # L'angle doit aller de -90° à +90°

        # Créer une transformation pour pivoter l'aiguille autour du centre de la jauge
        transform = QTransform()
        transform.translate(width / 2, height)  # Centrer au milieu en bas de la jauge
        transform.rotate(angle)
        painter.setTransform(transform)

        # Dessiner un rectangle pour représenter l'aiguille
        painter.drawRect(-self.needle_width / 2, -height, self.needle_width, height)

        painter.end()

        
    