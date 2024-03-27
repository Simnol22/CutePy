from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel
from Widgets.Widget import Widget
from PySide6.QtCore import Qt

class ImageWidget(Widget):
    def __init__(self, parent, image):
        super().__init__(parent)
        self.image = image
        pixmap = QPixmap(image)
        self.imageLabel = QLabel()
        self.imageLabel.setPixmap(pixmap)
        self.layout.addWidget(self.imageLabel)
        self.imageLabel.show()


    def move(self, x, y):
        self.move(x, y)
