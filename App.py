from View import CuteView
from Modules.FakeModule import FakeModule
from Modules.SerialModule import SerialModule

from threading import Thread
from protocol import ProtocolHelper
import signal # For catching Ctrl+C which is not working while multithreading in windows python

class App: # Controlleur
    def __init__(self):
        self.view = None
        self.modules = []
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.protocol = ProtocolHelper('protocol.xml')
        print(self.protocol.to_cute_name(0,2,4))
    def run(self):
        print('App is running')
        
        self.createModules()
        self.createView()
        

    def createModules(self):
        print("Initialising Modules")
        #fake = FakeModule(self, frequence=10)
        #if fake.readJson():
        #    print("Starting module threads")
        #    fakeThread = Thread(target=fake.run)
        #    fakeThread.start()
        serialModule = SerialModule(self, frequence=10)
        if serialModule.serialConnection():
            print("Starting module threads")
            serialThread = Thread(target=serialModule.run)
            serialThread.start()

    def createView(self):
        print("Initialising View")
        view = CuteView(frequence=10)
        self.view = view
        print("Starting view threads")
        viewThread = Thread(target=view.run)
        viewThread.start()
        self.view.startApp()
        print("Done !")

    def sendMeasurement(self, measurement):
        #Sending measurement to the view
        if self.view:
            self.view.updateMeasurement(measurement)


if __name__ == '__main__':
    # Deal with arguments here if needed
    app = App()
    app.run()