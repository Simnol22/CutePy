class ConfigSettings:
    def __init__(self, parent):
        self.app = parent
        self.serialPort = "COM4"
        self.baudrate = 115200
        self.saveData = False
        self.configFile = "config.json"
        self.defaultSavePath = "saved_data/cutepylog.csv"
        self.fakeData = True