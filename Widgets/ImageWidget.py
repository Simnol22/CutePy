from Widgets.Widget import Widget
from PySide6.QtWidgets import QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class ImageWidget(Widget):
    def __init__(self, parent, image, width=None):
        super().__init__(parent)
        self.image = image
        self.pixmap = QPixmap(image)
        self.imageLabel = QLabel()
        # Set width if specified
        if width is not None:
            self.imageWidth = width
            self.pixmap = self.pixmap.scaledToWidth(self.imageWidth, Qt.SmoothTransformation)
        self.imageLabel.setPixmap(self.pixmap)

        # Set up layout
        self.vlayout = QVBoxLayout()
        self.vlayout.addWidget(self.imageLabel)
        self.layout.addLayout(self.vlayout)

    def onUpdate(self):
        print("Resizing image")
        self.pixmap = self.pixmap.scaled(self.width(), self.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.imageLabel.setPixmap(self.pixmap)
