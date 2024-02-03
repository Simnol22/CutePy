from Modules.Module import DataModule
import time
import json

class FakeModule(DataModule):
    def __init__(self):
        self.freq = 1
        print("Fake")
    
    def readJson(self):
        try:
            with open('Modules/fakeconfig.json') as f:
                data = json.load(f)
                self.freq = data["freq"]
                fakeData = data["fake"]
                for i in fakeData:
                    print(i)
            return True
        except:
            print("Error reading fakeconfig.json")
            return False

    def run(self):
        while 1:
            print("FakeModule running")
            time.sleep(1/self.freq)

    def onTimeOut(self):
        pass
        #cute::proto::Measurement measurement;
        #measurement.set_source(mid_);
        #measurement.set_number(alpha_ * std::sin(n_) + phi_);
        #n_ += omega_ * ((std::numbers::pi * 2) / freq_);
        #emit messageReady({this, measurement});

    def onMessage(self, msg):
        pass