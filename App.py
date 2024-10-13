from View import CuteView
from Modules.FakeModule import FakeModule
from Modules.SerialModule import SerialModule
from Repositories.CsvData import CsvData
from threading import Thread
from PySide6.QtCore import QThreadPool
from ConfigSettings import ConfigSettings
import signal 
import sys

class App: # Controlleur
    def __init__(self):
        self.view = None
        self.modules = []
        self.csvData = None 
        self.serialModule = None
        self.fakeModule = None
        self.configSettings = ConfigSettings(self)
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        signal.signal(signal.SIGINT, signal.SIG_DFL) # For catching Ctrl+C which is not working while multithreading in windows python

    def run(self):
        print('App is running')
        self.createModules()
        self.createView()
        
    # All the modules are created here. Might create a model class for the modules for clearer and more maintainable code
    def createModules(self):
        print("Initialising Modules")
        self.csvData = CsvData(self, path = self.configSettings.defaultSavePath,frequence = 1)
        saveThread = Thread(target=self.csvData.run)
        saveThread.start()
        
        if self.configSettings.fakeData:
            self.startFakeData()

        self.serialModule = SerialModule(self, frequence=1) # No frequency for the serial module, this frequency is only for retrying connection with serial port
        print("Starting module threads")
        serialThread = Thread(target=self.serialModule.run)
        serialThread.start()

    def startFakeData(self):
        fake = FakeModule(self, frequence=15)
        if fake.readJson(): # If the fakeconfig.json file is read correctly
            print("Starting module threads")
            self.threadpool.start(fake)
    
    # The view is created here. It is a Qt application that will be running as the main thread
    def createView(self):
        print("Initialising View")
        view = CuteView(self, frequence=0.5, config=self.configSettings.configFile)
        self.view = view
        self.threadpool.start(self.view.run)
        # This will start the Qt event loop on the main thread. No other instructions will be executed until the application is closed
        self.view.startApp()
        print("Done !") 
    
    def sendCommand(self, command, val=None):
        if self.serialModule:
            self.serialModule.sendCommand(command, val)
        else:
            print("No serial module to send command to")

    def sendMeasurement(self, measurement):
        #Sending measurement to the view.
        if self.view:
            self.view.updateMeasurement(measurement)
        #Saving measurements
        if self.configSettings.saveData:
            if self.csvData:
                self.csvData.addMeasurement(measurement)

if __name__ == '__main__':
    # Deal with arguments here if needed
    app = App()
    sys._excepthook = sys.excepthook 
    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback) 
        sys.exit(1) 
    sys.excepthook = exception_hook 
    app.run()