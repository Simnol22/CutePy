from Modules.Module import DataModule
from Modules.Tools.protocol import ProtocolHelper
from Modules.Tools.radiopacket import RadioPacket
from Modules.Tools.Measurement import Measurement
import serial
import time
import struct
import serial.tools.list_ports

# serial.tools.list_ports.comports() pour list les ports

class SerialModule(DataModule):
    def __init__(self, parent, frequence = 5, protocol = None):
        
        self.freq = frequence
        self.parent = parent
        self.protocol = protocol
        self.packetSize = 8
        self.serial = None
        self.buffer = []
        
        # The COM port and baud rate will be changed from within the GUI
        self.com_port = "COM3"
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
    
    def getAvailablePorts(self):
        availablePorts = []
        for port,desc, hwid in sorted(serial.tools.list_ports.comports()):
            availablePorts.append(str(port))
        return availablePorts
    
    def setComPort(self, port):
        self.com_port = port
        self.serialConnection()
    
    # Taking a packet recieved by the RFD900 and building a Measurement object from it for the app to use.
    def buildMeasurement(self, packet):
        measurement = Measurement()
        measurement_source =self.protocol.to_cute_name(packet.node_group_id, packet.node, packet.message_id)
        measurement.setSource(measurement_source)

        # Turning the Bytes received into a float. 
        # Need to investigate this a little more. We seem to always only be sending 4 bytes of our 8 bytes payload,
        # the rest of which is always 0.
        double_value = struct.unpack('<f', packet.payload[:4])[0]
        measurement.setValue(double_value)
        
        measurement.setTimestamp(time.time())
        return measurement
    
    # Taking a packet recieved by the RFD900 and building a Measurement object from it for the app to use.
    def buildTestStatusMeasurement(self, packet):
        measurementArray = [Measurement(),Measurement(),Measurement(),Measurement()]
        measurement_source =self.protocol.to_cute_path(packet.node_group_id, packet.node)

        measurementArray[0].setSource(measurement_source+".test_en_cours")
        measurementArray[1].setSource(measurement_source+".igniter")
        measurementArray[2].setSource(measurement_source+".purge_valve")
        measurementArray[3].setSource(measurement_source+".main_valve")

        current_time = time.time()
        for i in range(len(measurementArray)):
            measurementArray[i].setValue(packet.payload[i])
            measurementArray[i].setTimestamp(current_time)

        return measurementArray

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
                packet.checksum = self.buffer[7]

                if packet.radio_compute_crc() == packet.checksum:
                    print("Valid Packet Received : Got " , self.buffer[:self.packetSize])
                    
                   # This is a bit hardcoded, but works for now. Verifying that the nodegroup id is 2 which is the testbench. then we verify some nodes.
                   # This should not affect anirniq. Ideally there would be no need for test cases here.
                    if packet.node == 11 and packet.node_group_id == 2:
                        measurementArray = self.buildTestStatusMeasurement(packet)
                        for measurement in measurementArray:
                            if measurement.hasValue():
                                self.parent.sendMeasurement(measurement)
                                print("sending ",measurement)
                            else:
                                print("Failed to build Measurement")

                    #If we do not have the node 11 from testbench, we will build a normal measurement.
                    else:
                        measurement = self.buildMeasurement(packet)
                        if measurement.hasValue():
                            self.parent.sendMeasurement(measurement)
                            print("sending ",measurement)
                        else:
                            print("Failed to build Measurement")
        
                    #It we have 14, we have an error message from the testbench. We will print it
                    if packet.node == 14 and packet.node_group_id == 2:
                        print("Received TestBench Error : "+self.protocol.to_cute_name(packet.node_group_id, packet.node, packet.message_id))

                    self.buffer = self.buffer[self.packetSize:] # remove 8 first elements
                else:
                    print("Invalid CRC : Got " + str(packet.checksum) + " Expected " + str(packet.radio_compute_crc()))
                    self.buffer = self.buffer[1:] # remove first element
    
    def sendCommand(self, command, val=None):
        nodeGroupId, nodeId, messageId = self.protocol.from_cute_name(command)
        sentBuffer = []
        
        sentBuffer.append(nodeGroupId)
        sentBuffer.append(nodeId)
        sentBuffer.append(messageId)
        print(val)
        #populate payload
        #this is very rough, and covers only the cases we have in the testbench
        #This code will need to be more modular and adaptable.
        payload = bytearray(4)
        if val is not None:
            if isinstance(val, str):
                val = val.replace(",",".")
                #TODO : find better way to verify these conditions. We might need to add other parameters to the function,
                #because we have no way of knowing if we are sending an int or a float or a list of int.
                if command == "rockets.testbench.coldflow.valve_open_time_ms":
                    payloadval = bytearray(struct.pack("i",int(val)))
                else:
                    payloadval = bytearray(struct.pack("f",float(val)))
            else:
                payloadval = bytearray(4)
                #I am tired and this needs to work. make it better.
                valtab1 = bytearray(struct.pack("i",int(val[0])))
                valtab2 = bytearray(struct.pack("i",int(val[1])))
                payloadval[0] = valtab1[0]
                payloadval[1] = valtab1[1]
                payloadval[2] = valtab2[0]
                payloadval[3] = valtab2[1]

            for i in range(len(payloadval)):
                payload[i] = payloadval[i]
                print(payload[i])


        for i in payload:
            sentBuffer.append(i)
        
        sentBuffer.append(0) # checksum

        packet = RadioPacket(data = sentBuffer)
        packet.nodeGroupId = nodeGroupId
        packet.nodeId = nodeId
        packet.messageId = messageId
        packet.payload = payload
        packet.checksum = packet.radio_compute_crc()

        self.serial.write(packet.to_bytearray())
