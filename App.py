from Model import CuteModel
from Modules.ModuleFactory import ModuleFactory
from threading import Thread

class App:
    def __init__(self):
        pass # Add any initialization code here
        
    def run(self):
        print('App is running')
        print("Initialising Modules")
        factory = ModuleFactory()

        fake = factory.create("fake")
        if fake.readJson():
            fakeThread = Thread(target=fake.run)
            fakeThread.start()

        serial = factory.create("serial")

        



if __name__ == '__main__':
    # Deal with arguments here if needed
    app = App()
    app.run()