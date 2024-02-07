from Widgets.PrintWidget import PrintWidget
from Widgets.DataWidget import DataWidget
import time
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow
import sys

class CuteView:
    def __init__(self,frequence = 1):
        self.widgets = []
        self.freq = frequence
        self.app = QApplication(sys.argv)
        self.createWidgets()

    def createWidgets(self): # Will be done more fancy test
        window = DataWidget()
        self.widgets.append(window)
        window.show()

    def run(self):
        try:
            while True:
                print("CuteView running")
                self.onTimeOut()
                time.sleep(1/self.freq)
        except KeyboardInterrupt:
            print('interrupted!')

    def startApp(self):
        self.app.exec() #Start the Qt event loop on the main thread. No other instructions will be executed until the application is closed

    def onTimeOut(self): #Loop for all widgets. You could make a different queue for each widget and run them in parallel
        for widget in self.widgets:
            widget.refresh()
            widget.update()

    # Chaque widget a son requiredData. On peut mettre la ou les sources qu'on souhaite recevoir
    # et la fonction va les envoyer au widget
    def updateMeasurement(self, measurement):
        for widget in self.widgets:
            for i in widget.requiredData:
                if i == measurement.source:
                    widget.setData(measurement)
