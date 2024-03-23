from Widgets.Widget import Widget

#Simple widget that prints the data for testing purposes
class PrintWidget(Widget):
    def __init__(self,name):
        super().__init__(name)
        self.data = None

    def setData(self,data):
        self.data = data
        self.refresh()

    def refresh(self):
        if self.data:
            print(self.data)
