from Widgets.PrintWidget import PrintWidget
from Widgets.DataWidget import DataWidget
from Widgets.TerminalWidget import TerminalWidget
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
        window = QMainWindow()
        window.setWindowTitle("CuteView")
        window.setStyleSheet("border: 1px solid red;")
        window.resize(600,400)
        data = DataWidget(window)
        data2 = TerminalWidget(window)
        data2.move(300,0)
        data2.resize(400,300)

        self.widgets.append(data)
        self.widgets.append(data2)
        window.show()

    # CuteView Thread loop. This is just for refreshing the widgets information
    def run(self):
        try:
            while True:
                #print("CuteView running")
                self.app.processEvents()
                self.onTimeOut()
                
                time.sleep(1/self.freq)
        except KeyboardInterrupt:
            print('interrupted!')
    
    # Start the Qt event loop on the main thread. No other instructions will be executed until the application is closed
    def startApp(self):
       # self.app.exec() 
        ...

    # Loop for all widgets. You could make a different queue for each widget and run them in parallel
    def onTimeOut(self): 
        #for widget in self.widgets:
        #    widget.refresh()
        #    widget.update()
        pass

    # Chaque widget a son requiredData. On peut mettre la ou les sources qu'on souhaite recevoir
    # et la fonction va les envoyer au widget
    def updateMeasurement(self, measurement):
        for widget in self.widgets:
            for i in widget.requiredData:
                if i == measurement.source or i == "all":
                    widget.setData(measurement)

