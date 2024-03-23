from PySide6.QtWidgets import QGroupBox

from Widgets.Widget import Widget
from Widgets.GridWidget import GridWidget

class GroupWidget(Widget):
    def __init__(self, parent, name):
        super(GroupWidget, self).__init__(parent)
        self.box = QGroupBox(name, self)
        self.grid = GridWidget()
        self.box.setLayout(self.grid)
        self.layout.addWidget(self.box)
        self.layout.setContentsMargins(10,10,10,10)
        #List of required data for this widget. Empty since its a group. Could add something if wanted
        self.requiredData = [] 
        
    def setName(self, name):
        self.name = name
        self.box.setTitle(name)