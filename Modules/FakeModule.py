from Modules.Module import DataModule

class FakeModule(DataModule):
    def __init__(self):
        print("Fake")
    
    def test(self):
        print("in test")

    def onMessage(self, msg):
        pass