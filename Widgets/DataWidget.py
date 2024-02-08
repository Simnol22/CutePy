from Widgets.Widget import Widget
from PySide6.QtWidgets import QLabel, QWidget, QMainWindow
from PySide6 import QtCore

class DataWidget(Widget):
    def __init__(self, parent):
        super(DataWidget, self).__init__(parent)
        #self.setWindowTitle("Data Widget")
        self.label = QLabel("No data")
        self.layout.addWidget(self.label)
        #self.setCentralWidget(self.label)
        self.data = None
        self.requiredData = ["rockets.anirniq.acquisition.gps.lat","rockets.anirniq.acquisition.gps.lon","rockets.anirniq.mission.charge_status.main","rockets.anirniq.mission.charge_status.drogue","rockets.anirniq.mission.charge_status.payload"]
        self.latVal = None
        self.lonVal = None
        self.latest = None

    # Here we are receiving measurements wanted in requiredData. 
    # We need to separate them with the value of the source.
    def setData(self, data):
        self.data = data
        if data.source == "rockets.anirniq.mission.charge_status.main":
            self.latVal = data.value
        if data.source == "rockets.anirniq.mission.charge_status.drogue":
            self.lonVal = data.value
        if data.source == "rockets.anirniq.mission.charge_status.payload":
            self.latest = data.value

    def refresh(self):
        #if self.latVal:
        self.label.setText( "charge main : " + str(self.latVal) + "\n" + "charge drogue " + str(self.lonVal) + "\n" + "charge drogue " + str(self.latest))# + "Lon : " + str(self.lonVal))