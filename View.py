from Widgets.PrintWidget import PrintWidget
from Widgets.DataWidget import DataWidget
import time
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow
import sys

class CuteView:
    def __init__(self,frequence = 1):
        self.widgets = []
        self.freq = frequence
        #self.widgets.append(PrintWidget("PrintWidget"))

    def run(self):
        self.app = QApplication(sys.argv)
        #window = QMainWindow()
        window = DataWidget()
        self.widgets.append(window)
        window.show()
        try:
            while True:
                print("CuteView running")
                self.onTimeOut()
                time.sleep(1/self.freq)
        except KeyboardInterrupt:
            print('interrupted!')
        
    def onTimeOut(self): #Loop for all widgets. You could make a different queue for each widget and run them in parallel
        self.app.processEvents()
        for widget in self.widgets:
            widget.refresh()
            widget.update()
    
    def updateMeasurement(self, measurement):
        for widget in self.widgets:
            if measurement.source == 'rockets.anirniq.acquisition.altitude':
                widget.setData(measurement)
