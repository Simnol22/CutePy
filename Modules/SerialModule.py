from Modules.Module import DataModule
import serial #From PySerial

class SerialModule(DataModule):
    def __init__(self):
        print("Serial")
        com_port = "COM4"
        baud_rate = 9600
