from Modules.Module import DataModule
#import serial from PySerial

class SerialModule(DataModule):
    def __init__(self):
        print("Serial")
        com_port = "COM4"
        baud_rate = 9600
