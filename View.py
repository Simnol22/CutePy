from Widgets.PrintWidget import PrintWidget
import time
from PySide6.QtWidgets import QApplication, QWidget
import sys

class CuteView:
    def __init__(self,frequence = 1):
        self.widgets = []
        self.freq = frequence
        self.widgets.append(PrintWidget("PrintWidget"))

    def run(self):
        app = QApplication(sys.argv)
        window = QWidget()
        window.show()
        app.exec()
        #try:
        #    while True:
        #        print("CuteView running")
        #        self.onTimeOut()
        #        time.sleep(1/self.freq)
        #except KeyboardInterrupt:
        #    print('interrupted!')
        
    def onTimeOut(self):
        for widget in self.widgets:
            widget.refresh()
    
    def updateMeasurement(self, measurement):
        for widget in self.widgets:
            if measurement.source == 'rockets.timmiaq.acquisition.temperature':
                widget.setData(measurement)
