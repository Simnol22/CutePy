from PySide6.QtWidgets import QGridLayout

# This class is a subclass of QGridLayout. It is used to add widgets to the grid layout with x and y instead of row and columns.
class GridWidget(QGridLayout):
    def __init__(self):
        super().__init__()

    def addWidget(self, widget, x, y, xspan=1, yspan=1):
        super().addWidget(widget, y, x, yspan, xspan)