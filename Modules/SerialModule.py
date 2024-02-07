from Modules.Module import DataModule
from protocol import ProtocolHelper
from Modules.radiopacket import RadioPacket
from Measurement import Measurement
import serial 
import time
import struct

#serial.tools.list_ports.comports() pour list les ports

class SerialModule(DataModule):
    def __init__(self, parent, frequence = 5, protocol = None):
        print("Serial")
        self.freq = frequence
        self.parent = parent

        self.com_port = "/dev/tty.usbserial-FT9MI2X7"
        self.baud_rate = 115200
        self.serial = None
        self.protocol = protocol
        self.buffer = []
        if self.protocol is None:
            self.protocol = ProtocolHelper('protocol.xml')
        #if self.serialConnection():
        #    print("SerialModule Created")
        #else:
        #    print("Error creating SerialModule")
    
    def serialConnection(self):
        if self.com_port and self.baud_rate:
            try:
                self.serial = serial.Serial()
                self.serial.port = self.com_port
                self.serial.baudrate = self.baud_rate
                self.serial.open()
                print("Serial module connected")
            except:
                print("Error opening serial port")
                return False
            return True
        else:
            print("Error with COM PORT or BAUD RATE")
            return False
        
    def buildMeasurement(self, packet):
        measurement = Measurement()
        measurement_source =self.protocol.to_cute_name(packet.node_group_id, packet.node, packet.message_id)
        measurement.setSource(measurement_source)
        #Need to turn packet.payload, a byte array, into a float
        double_value = struct.unpack('<f', packet.payload[:4])
        measurement.setValue(double_value)
        
        measurement.setTimestamp(time.time())
        return measurement

    def run(self):
        try:
            while True:
                #print("SerialModule running")
                self.onData()
                #time.sleep(1/self.freq)
        except KeyboardInterrupt:
            print('interrupted!')
        print("SerialModule running") 

    def onData(self):
        bufferRead = self.serial.read(100)
        for i in bufferRead:
            self.buffer.append(i)
            if len(self.buffer)>= 12:
                packet = RadioPacket(data = self.buffer[:12])
                packet.node_group_id = self.buffer[0]
                packet.node = self.buffer[1]
                packet.message_id = self.buffer[2]
                packet.payload[0] = self.buffer[3]
                packet.payload[1] = self.buffer[4]
                packet.payload[2] = self.buffer[5]
                packet.payload[3] = self.buffer[6]
                packet.payload[4] = self.buffer[7]
                packet.payload[5] = self.buffer[8]
                packet.payload[6] = self.buffer[9]
                packet.payload[7] = self.buffer[10]
                packet.checksum = self.buffer[11]
                print("data : ", self.buffer[:12])
                if packet.radio_compute_crc() == packet.checksum:
                    measurement = self.buildMeasurement(packet)
                    if measurement.hasValue():
                        self.parent.sendMeasurement(measurement)
                        print("sending ", measurement)
                    else:
                        print("Failed to build Measurement")
                    self.buffer = self.buffer[12:] #remove 12 first elements
                else:
                    print("Invalid CRC : Got " + str(packet.checksum) + " Expected " + str(packet.radio_compute_crc()))
                    self.buffer = self.buffer[1:] #remove first element


    def onMessage(self, msg):
        pass
