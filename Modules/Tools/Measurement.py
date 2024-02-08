import time

class Measurement:
    def __init__(self):
        self.source = None
        self.value = None

        # Setting timestamp as Measurment creation time. 
        # Might want to change this in the future with the detection of flight.
        ts = time.time()
        self.timestamp = ts

    def setSource(self, source):
        self.source = source

    def setTimestamp(self, timestamp):
        self.timestamp = timestamp

    def setValue(self, value):
        self.value = value

    def hasValue(self):
        return self.value is not None
    
    def __str__(self):
        return "Measurement: " + str(self.source) + " -> " + str(self.value) + " @ " + str(self.timestamp)