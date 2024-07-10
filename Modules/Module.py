from PySide6.QtCore import QTimer, QRunnable, Slot, Signal, QObject, QThreadPool
# This is the base class for all modules. Not used yet but might be useful in the future. When dealing with more modules

class DataModule(QRunnable):
    def __init__(self):
        super(DataModule, self).__init__()
        self.signals = Signal(object)

    @Slot()
    def run(self):
        pass