from Widgets.Widget import Widget
from PySide6.QtWidgets import QLabel, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor

class StatusWidget(Widget):
    def __init__(self, parent, status):
        super().__init__(parent)
        self.status = status
        self.statusVal = 0
        self.statusLayout = QVBoxLayout(alignment=Qt.AlignCenter)
        self.statusLayout.setContentsMargins(0,0,0,0)
        self.statusLayout.setSpacing(0)
        self.arrowIcon = '▼'
        self.statusPrevious = QLabel()
        self.statusActual = QLabel()
        self.statusActual.setStyleSheet('font-size: 18pt')
        self.statusNext = QLabel()
        self.prevArrow = QLabel(self.arrowIcon)
        self.nextArrow = QLabel(self.arrowIcon)
        self.setLabelColor()
        self.statusLayout.addWidget(self.statusPrevious,alignment=Qt.AlignCenter)
        self.statusLayout.addWidget(self.prevArrow,alignment=Qt.AlignCenter)
        self.statusLayout.addWidget(self.statusActual,alignment=Qt.AlignCenter)
        self.statusLayout.addWidget(self.nextArrow,alignment=Qt.AlignCenter)
        self.statusLayout.addWidget(self.statusNext,alignment=Qt.AlignCenter)
        self.layout.addLayout(self.statusLayout)
        self.refresh()

    #Method used for code organization. This is setting the color of the label (essentially keeping the base color but changing the alpha value)
    def setLabelColor(self):
        current_color = self.statusPrevious.palette().color(self.statusPrevious.foregroundRole())
        new_color = QColor(current_color.red(), current_color.green(), current_color.blue(), 128)  # Setting alpha to 128 (50% transparency)
        self.statusPrevious.setStyleSheet("color: rgba({}, {}, {}, {})".format(new_color.red(), new_color.green(), new_color.blue(), new_color.alpha()))
        self.statusNext.setStyleSheet("color: rgba({}, {}, {}, {})".format(new_color.red(), new_color.green(), new_color.blue(), new_color.alpha()))

    def setData(self, data):
        for i in self.requiredData:
            if data.source == i:
                self.statusVal = int(round(data.value,0)) 
                
            
    def refresh(self):
        currentVal = int(self.statusVal)
        self.statusActual.setText(self.status.get(str(currentVal)))
        self.prevArrow.setText(self.arrowIcon)
        self.nextArrow.setText(self.arrowIcon)
        if currentVal == 0: 
            self.statusPrevious.setText("")
            self.statusNext.setText(self.status.get(str(currentVal+1)))
            self.prevArrow.setText("")
        elif currentVal == len(self.status) - 1:
            self.statusPrevious.setText(self.status.get(str(currentVal-1)))
            self.statusNext.setText("")
            self.nextArrow.setText("")
        else:
            self.statusPrevious.setText(self.status.get(str(currentVal-1)))
            self.statusNext.setText(self.status.get(str(currentVal+1)))
