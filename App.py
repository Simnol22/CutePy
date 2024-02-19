from View import CuteView
from Modules.FakeModule import FakeModule
from Modules.SerialModule import SerialModule

from threading import Thread

import signal 

class App: # Controlleur
    def __init__(self):
        self.view = None
        self.modules = []
        signal.signal(signal.SIGINT, signal.SIG_DFL) # For catching Ctrl+C which is not working while multithreading in windows python

    def run(self):
        print('App is running')
        self.createModules()
        self.createView()
        
    # All the modules are created here. Might create a model class for the modules for clearer and more maintainable code
    def createModules(self):
        print("Initialising Modules")
        fake = FakeModule(self, frequence=200)
        if fake.readJson(): # If the fakeconfig.json file is read correctly
            print("Starting module threads")
            fakeThread = Thread(target=fake.run)
            fakeThread.start()
        #
        #serialModule = SerialModule(self, frequence=1) # No frequency for the serial module, this frequency is only for retrying connection with serial port
        #print("Starting module threads")
        #serialThread = Thread(target=serialModule.run)
        #serialThread.start()
    
    # The view is created here. It is a Qt application that will be running as the main thread
    def createView(self):
        print("Initialising View")
        view = CuteView(frequence=20)
        self.view = view
        print("Starting view threads")
        viewThread = Thread(target=view.run)
        viewThread.start()
        # This will start the Qt event loop on the main thread. No other instructions will be executed until the application is closed
        self.view.startApp()
        print("Done !") 

    def sendMeasurement(self, measurement):
        #Sending measurement to the view.
        if self.view:
            self.view.updateMeasurement(measurement)


if __name__ == '__main__':
    # Deal with arguments here if needed
    app = App()
    app.run()