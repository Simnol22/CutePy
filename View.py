#PySide imports
from PySide6.QtWidgets import QApplication

#Widgets
from Widgets.Window import Window
from Widgets.WidgetFactory import WidgetFactory

#Python imports
import time
import sys
import json


class CuteView:
    def __init__(self,frequence = 1):
        self.widgets = []
        self.freq = frequence
        self.jsonConfig = json.load(open("config.json"))
        #Opening the config file
        if not self.jsonConfig:
            print("Error: Could not open config file")
            sys.exit(1)
        print("Opened config file")

        self.app = QApplication(sys.argv)
        self.createWidgets()

    def createWidgets(self):
        self.widgetFactory = WidgetFactory(self)
        self.window = Window()
        self.widgetFactory.buildAll(self.jsonConfig,self.window.grid,self.window)
        self.window.show()

    #Register a widget to the data flow
    def registerWidget(self,widget):
        self.widgets.append(widget)

    # CuteView Thread loop. This is just for refreshing the widgets information
    def run(self):
        try:
            while True:
                self.onTimeOut()
                
                time.sleep(1/self.freq)
        except KeyboardInterrupt:
            print('interrupted!')
    
    # Start the Qt event loop on the main thread. No other instructions will be executed until the application is closed
    def startApp(self):
        self.app.exec() 

    # Loop for all widgets. Since we have data transfer by reference, 
    # we don't need to manualy update the widgets for now. Might come in handy for some widgets
    def onTimeOut(self):
        for widget in self.widgets:
            widget.onUpdate()

    # Chaque widget a son requiredData. On peut mettre la ou les sources qu'on souhaite recevoir
    # et la fonction va les envoyer au widget
    def updateMeasurement(self, measurement):
        for widget in self.widgets:
            for i in widget.requiredData:
                if i == measurement.source or i == "all":
                    widget.setData(measurement)

