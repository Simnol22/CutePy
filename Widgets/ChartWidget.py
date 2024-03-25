import pyqtgraph as pg
from pyqtgraph import DateAxisItem
from Widgets.Widget import Widget
from PySide6 import QtGui
from datetime import datetime


class ChartWidget(Widget):
    def __init__(self,name):
        super().__init__(name)
        #On utilise un DateAxisItem pour afficher les dates sur l'axe des x
        dateAxis = DateAxisItem()
        self.chart = pg.PlotWidget(axisItems = {'bottom': dateAxis})
        color = self.palette().color(QtGui.QPalette.Window)
        self.chart.setBackground(color)
        self.layout.addWidget(self.chart)
        self.x = []
        self.y = []
        #On utilise un pen pour définir la couleur et l'épaisseur de la ligne
        pen = pg.mkPen(color=(65,105,225), width=5)
        self.dataLine = self.chart.plot(self.y, self.x, pen=pen)
    
    def setTitle(self, title):
        self.chart.setTitle(title)

    def setData(self, data):
        for i in self.requiredData:
            if data.source == i:
                self.x.append(data.value)
                self.y.append(data.timestamp)
                self.refresh()                
    
    def refresh(self):
        self.dataLine.setData(self.y,self.x)
        
        