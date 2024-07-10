import pyqtgraph as pg
from pyqtgraph import DateAxisItem
from Widgets.Widget import Widget
from PySide6 import QtGui
from datetime import datetime
from collections import deque

class ChartWidget(Widget):
    def __init__(self, parent, max_points=1000):
        super().__init__(parent)
        # Use a DateAxisItem to display dates on the x-axis
        dateAxis = DateAxisItem()
        self.chart = pg.PlotWidget(axisItems={'bottom': dateAxis})
        color = self.palette().color(QtGui.QPalette.Window)
        self.chart.setBackground(color)
        self.layout.addWidget(self.chart)
        self.max_points = max_points
        self.x = deque(maxlen=self.max_points)
        self.y = deque(maxlen=self.max_points)
        # Use a pen to define the color and thickness of the line
        pen = pg.mkPen(color=(65, 105, 225), width=5)
        self.dataLine = self.chart.plot(self.y, self.x, pen=pen)

    def setTitle(self, title):
        self.chart.setTitle(title)

    def setData(self, data):
        for i in self.requiredData:
            if data.source == i:
                self.x.append(data.value)
                self.y.append(data.timestamp)
    
    def refresh(self):
        self.dataLine.setData(self.y, self.x)
