from Model import CuteModel
from Modules.ModuleFactory import ModuleFactory

class App:
    def __init__(self):
        pass # Add any initialization code here
        
    def run(self):
        print('App is running')
        print("Initialising Modules")
        factory = ModuleFactory()

        fake = factory.create("Fake")
        serial = factory.create("Serial")
        



if __name__ == '__main__':
    # Deal with arguments here if needed
    app = App()
    app.run()