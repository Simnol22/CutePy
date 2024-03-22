from Modules.Module import DataModule
from Modules.Tools.Measurement import Measurement
import math
import time
import json

class FakeModule(DataModule):
    def __init__(self,parent,frequence=1):
        self.freq = frequence
        self.baseData = {}
        self.n = 1
        self.parent = parent
        print("FakeModule Created")
    
    # Read the fakeconfig.json file, get the data as a variable
    def readJson(self):
        try:
            with open('Modules/fakeconfig.json') as f:
                data = json.load(f)
                self.baseData = data["fake"]
            return True
        except:
            print("Error reading fakeconfig.json")
            return False

    # FakeModule Thread loop.
    def run(self):
        try:
            while True:
                print("FakeModule running")
                self.onData()
                time.sleep(1/self.freq)
        except KeyboardInterrupt:
            print('interrupted!')
        print("FakeModule running")
    
    # with the variable data, we can calculate the value of the measurement and send it to the parent
    def onData(self):
        for i in self.baseData:
            measurement = Measurement()
            measurement.setSource(i["mid"])
            measurement.setValue(i["alpha"] * math.sin(i["n"]) + i["phi"])
            i["n"] += i["omega"] * ((math.pi * 2) / self.freq)
            self.parent.sendMeasurement(measurement)
            #print(measurement)