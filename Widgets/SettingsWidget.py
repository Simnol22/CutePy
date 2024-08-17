from Widgets.Widget import Widget
from PySide6.QtWidgets import QPushButton, QCheckBox, QComboBox, QHBoxLayout, QVBoxLayout, QLabel, QFileDialog
import serial

class SettingsWidget(Widget):
    def __init__(self, parent, view):
        super().__init__(parent)
        self.parent = parent
        self.view = view
        
        self.settingsLayout = QVBoxLayout()
        self.settingsLayout.setSpacing(10)

        hlayoutserial = QHBoxLayout()
        hlayoutserial.addWidget(QLabel("Serial Port"))
        self.serialportbox = QComboBox()
        self.currentItems = []
        for i in self.getAvailablePorts():
            self.currentItems.append(str(i))
            self.serialportbox.addItem(str(i))
        self.serialportbox.setCurrentIndex(-1) #Nothing selected at first
        self.serialportbox.currentTextChanged.connect(self.changeSerial)

        hlayoutserial.addWidget(self.serialportbox)
        self.settingsLayout.addLayout(hlayoutserial)

        hlayoutbaudrate = QHBoxLayout()
        hlayoutbaudrate.addWidget(QLabel("Baud rate"))
        self.baudratebox = QComboBox()
        self.baudratebox.addItem("9600")
        self.baudratebox.addItem("115200")
        self.baudratebox.setCurrentIndex(-1) #Nothing selected at first
        self.baudratebox.currentTextChanged.connect(self.changeBaudrate)
        hlayoutbaudrate.addWidget(self.baudratebox)
        self.settingsLayout.addLayout(hlayoutbaudrate)

        self.checkboxSave = QCheckBox("Save data")
        self.checkboxSave.clicked.connect(self.checked)
        self.settingsLayout.addWidget(self.checkboxSave)

        self.button = QPushButton("Config File")
        self.button.clicked.connect(self.pressed)
        self.settingsLayout.addWidget(self.button)
        
        self.layout.addLayout(self.settingsLayout)

        self.configSettings = self.view.parent.configSettings

    def changeSerial(self, serialport):
        self.configSettings.serialPort = serialport

    def changeBaudrate(self, baudrate):
        self.configSettings.baudrate = int(baudrate)

    def pressed(self):
        file = QFileDialog.getOpenFileName(self)[0]
        self.view.loadNewConfig(file)
    
    def checked(self):
        self.configSettings.saveData = self.checkboxSave.isChecked()

    def getAvailablePorts(self):
        availablePorts = []
        for port,desc, hwid in sorted(serial.tools.list_ports.comports()):
            availablePorts.append(str(port))
        return availablePorts
    
    #The onTimeOut here refreshes the list for available serial ports
    def onTimeOut(self):
        ports = self.getAvailablePorts()

        #Ajouter un élément si on le détecte
        if len(ports) > len(self.currentItems):
            print("New Serial device detected")
            for i in ports:
                if i not in self.currentItems:
                    self.serialportbox.addItem(str(i))
                    self.currentItems.append(i)

        #Retirer un element si on ne le détecte plus
        elif len(ports) < len(self.currentItems):
            for i in self.currentItems:
                if i not in ports:
                    self.currentItems.remove(i)
                    for index in range(len(ports)):
                        if self.serialportbox.itemText(index) == i:
                            self.serialportbox.removeItem(index)