from Modules.Module import DataModule
from Measurement import Measurement
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
    
    def readJson(self):
        try:
            with open('Modules/fakeconfig.json') as f:
                data = json.load(f)
                self.freq = data["freq"]
                self.baseData = data["fake"]
            return True
        except:
            print("Error reading fakeconfig.json")
            return False

    def run(self):
        try:
            while True:
                print("FakeModule running")
                self.onData()
                time.sleep(1/self.freq)
        except KeyboardInterrupt:
            print('interrupted!')
        print("FakeModule running")

    def onData(self):
        for i in self.baseData:
            measurement = Measurement()
            measurement.setSource(i["mid"])
            measurement.setValue(i["alpha"] * math.sin(i["n"]) + i["phi"])
            i["n"] += i["omega"] * ((math.pi * 2) / self.freq)
            self.parent.sendMeasurement(measurement)

    def onMessage(self, msg):
        pass