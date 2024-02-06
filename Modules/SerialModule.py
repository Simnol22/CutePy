from Modules.Module import DataModule
#import serial from PySerial

class SerialModule(DataModule):
    def __init__(self):
        print("Serial")
        self.com_port = "COM4"
        self.baud_rate = 9600
