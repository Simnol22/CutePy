from Modules.Module import DataModule
from Modules.Tools.protocol import ProtocolHelper
from Modules.Tools.radiopacket import RadioPacket
from Modules.Tools.Measurement import Measurement
import serial
import time
import struct

# serial.tools.list_ports.comports() pour list les ports

class SerialModule(DataModule):
    def __init__(self, parent, frequence = 5, protocol = None):
        
        self.freq = frequence
        self.parent = parent
        self.protocol = protocol
        self.packetSize = 12
        self.serial = None
        self.buffer = []
        
        # The COM port and baud rate will be changed from within the GUI
        self.com_port = "/dev/tty.usbserial-FT9MI2X7"
        self.baud_rate = 115200
        
        #Instanciate protocol object only if it's not already done
        if self.protocol is None:
            self.protocol = ProtocolHelper('Modules/Tools/protocol.xml')
        self.serialConnection()
        print("Serial Module Created")
    
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
    
    # Taking a packet recieved by the RFD900 and building a Measurement object from it for the app to use.
    def buildMeasurement(self, packet):
        measurement = Measurement()
        measurement_source =self.protocol.to_cute_name(packet.node_group_id, packet.node, packet.message_id)
        measurement.setSource(measurement_source)

        # Turning the Bytes received into a float. 
        # Need to investigate this a little more. We seem to always only be sending 4 bytes of our 8 bytes payload,
        # the rest of which is always 0.
        double_value = struct.unpack('<f', packet.payload[:4])
        measurement.setValue(double_value)
        
        measurement.setTimestamp(time.time())
        return measurement

    # This is the main loop of the SerialModule. It will be running in the background as a thread. Since this is waiting for data
    # from the serial port, it will be running in a loop without a frequency like the other modules.
    def run(self):
        try:
            while True:
                if self.serial.isOpen():
                    self.onData()
                else:
                    print("Serial module not connected. Retrying...")
                    time.sleep(1/self.freq)
                    self.serialConnection()
        except KeyboardInterrupt:
            print('interrupted!')
        print("SerialModule running") 

    # Reading data from serial port. waiting for 12 bytes to be read before processing the packet.
    # Once the packet is complete, we build a Measurement object from it and send it to the app. The data
    # will synchronize and validates itself via the CRC check.
    def onData(self):
        bufferRead = self.serial.read(100)
        for i in bufferRead:
            self.buffer.append(i)
            if len(self.buffer)>= self.packetSize:
                packet = RadioPacket(data = self.buffer[:self.packetSize])
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
                print("data : ", self.buffer[:self.packetSize])
                if packet.radio_compute_crc() == packet.checksum:
                    measurement = self.buildMeasurement(packet)
                    if measurement.hasValue():
                        self.parent.sendMeasurement(measurement)
                        print("sending ", measurement)
                    else:
                        print("Failed to build Measurement")
                    self.buffer = self.buffer[self.packetSize:] # remove 12 first elements
                else:
                    print("Invalid CRC : Got " + str(packet.checksum) + " Expected " + str(packet.radio_compute_crc()))
                    self.buffer = self.buffer[1:] # remove first element

    # Function to send a message to the serial port. Not implemented yet.
    def onMessage(self, msg):
        pass
