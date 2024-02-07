from Widgets.Widget import Widget
from PySide6.QtWidgets import QLabel, QMainWindow

class DataWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Widget")
        self.label = QLabel("No data")
        self.setCentralWidget(self.label)
        self.data = None
        self.requiredData = ["rockets.anirniq.acquisition.gps.lat","rockets.anirniq.acquisition.gps.lon","rockets.anirniq.mission.charge_status.main"]
        self.latVal = None
        self.lonVal = None
    
    # Here we are receiving measurements wanted in requiredData. 
    # We need to separate them with the value of the source.
    def setData(self, data):
        self.data = data
        if data.source == "rockets.anirniq.mission.charge_status.main":
            self.latVal = data.value
            print("just set beuatiful data : ", self.latVal)
        if data.source == "rockets.anirniq.acquisition.gps.lon":
            self.lonVal = data.value

    def refresh(self):
        #if self.latVal:
        self.label.setText( "charge : " + str(self.latVal))# + "Lon : " + str(self.lonVal))