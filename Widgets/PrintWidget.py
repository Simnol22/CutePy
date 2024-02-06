from Widgets.Widget import Widget

class PrintWidget(Widget):
    def __init__(self,name):
        super().__init__(name)
        self.data = None

    def setData(self,data):
        self.data = data

    def refresh(self):
        if self.data:
            print(self.data)
