from Widgets.DataWidget import DataWidget
from Widgets.PrintWidget import PrintWidget
from Widgets.CompassWidget import CompassWidget
from Widgets.TerminalWidget import TerminalWidget
from Widgets.GroupWidget import GroupWidget
from Widgets.ChartWidget import ChartWidget
from Widgets.ImageWidget import ImageWidget
from Widgets.StatusWidget import StatusWidget
from Widgets.ButtonWidget import ButtonWidget
from Widgets.TextFieldWidget import TextFieldWidget
from Widgets.ChargeWidget import ChargeWidget
from Widgets.TextWidget import TextWidget
from Widgets.SettingsWidget import SettingsWidget
from Widgets.OrientationWidget import OrientationWidget
from Widgets.GaugeWidget import GaugeWidget

class WidgetFactory:
    def __init__(self, parent):
        self.widgets = {}
        # Important to have a reference to  the view, so that we can register the widgets
        # to the data transfer
        self.view = parent

    def buildAll(self, config, grid, parent = None):
        #Get the widgets from the config file
        for widgetConfig in config["widgets"]:
            #Check required fields
            if widgetConfig.get("x") is not None and widgetConfig.get("y") is not None:
                widget = self.buildWidget(widgetConfig, parent)
                if widget:
                    #Register widget to data transfer
                    self.view.registerWidget(widget)

                    #Add widget to the grid
                    xspan,yspan = 1,1
                    if widgetConfig.get("xspan"):
                        xspan = widgetConfig["xspan"]
                    if widgetConfig.get("yspan"):
                        yspan = widgetConfig["yspan"]
                    widget.name = widgetConfig.get("name")
                
                    grid.addWidget(widget, widgetConfig["x"], widgetConfig["y"],xspan,yspan)

                    #Set the size of the widget if specified might want to use setMinimumSize instead here.
                    if widgetConfig.get("width"):
                        widget.setFixedWidth(widgetConfig["width"])
                    if widgetConfig.get("height"):
                         widget.setFixedHeight(widgetConfig["height"])
            else:
                if widgetConfig.get("type"):
                    print("Widget", widgetConfig["type"], "has no x or y value")
                else:
                    print("Unknown widget has no x or y value")
                


    def buildWidget(self, config, parent= None):
        #Check if the widget has a type
        if (config.get("type")):
            if config["type"] == "PrintWidget":
                return self.buildPrintWidget(config, parent)
            elif config["type"] == "DataWidget":
                return self.buildDataWidget(config, parent)
            elif config["type"] == "CompassWidget":
                return self.buildCompassWidget(config, parent)
            elif config["type"] == "TerminalWidget":
                return self.buildTerminalWidget(config, parent)
            elif config["type"] == "GroupWidget":
                return self.buildGroupWidget(config, parent)
            elif config["type"] == "ChartWidget":
                return self.buildChartWidget(config, parent)
            elif config["type"] == "ImageWidget":
                return self.buildImageWidget(config, parent)
            elif config["type"] == "StatusWidget":
                return self.buildStatusWidget(config, parent)
            elif config["type"] == "ButtonWidget":
                return self.buildButtonWidget(config, parent)
            elif config["type"] == "TextFieldWidget":
                return self.buildTextFieldWidget(config,parent)
            elif config["type"] == "ChargeWidget":
                return self.buildChargeWidget(config, parent)
            elif config["type"] == "TextWidget":
                return self.buildTextWidget(config, parent)
            elif config["type"] == "SettingsWidget":
                return self.buildSettingsWidget(config, parent)
            elif config["type"] == "OrientationWidget":
                return self.buildOrientationWidget(config, parent)
            elif config["type"] == "GaugeWidget":
                return self.buildGaugeWidget(config, parent)
            else:
                print("Widget type", config["type"]," not found")
                return None
            
        else:
            print("Widget has no type")
            return None
    
    def buildGroupWidget(self, config, parent):
        if not config.get("label"):
            print("GroupWidget has no label")
            return None
        if not config.get("widgets"):
            print("GroupWidget has no widgets")
            return None
        name = config.get("label")
        widget = GroupWidget(parent, name)
        self.buildAll(config, widget.grid, widget)
        return widget
    
    def buildDataWidget(self, config, parent):
        if not (config.get("label") or config.get("source")):
            print ("DataWidget has no label or source")
            return None
        position = "vertical"
        if config.get("position"):
            position = config["position"]
        widget = DataWidget(parent,position, config.get("mode"))
        widget.setLabel(config["label"])
        widget.setSource(config["source"])
        if config.get("unit"):
            widget.setUnit(config["unit"])
        if config.get("round") is not None:
            widget.setRounding(config["round"])
        if config.get("conversion") is not None:
            widget.setConversion(config["conversion"])
        widget.updateDataLabel()
        return widget
    
    def buildPrintWidget(self, config, parent):
        widget = PrintWidget(parent)
        return widget
    
    def buildCompassWidget(self, config, parent):
        widget = CompassWidget(parent)
        return widget
    
    def buildTerminalWidget(self, config, parent):
        if not (config.get("label") or config.get("source")):
            print ("DataWidget has no label or source")
            return None
        widget = TerminalWidget(parent)
        widget.setLabel(config["label"])
        widget.setSource(config["source"])
        if config.get("round") is not None:
            widget.setRounding(config["round"])
        return widget
    
    def buildChartWidget(self, config, parent):
        if not (config.get("source")):
            print ("ChartWidget has no source")
            return None
        widget = ChartWidget(parent)
        widget.setSource(config["source"])
        if config.get("title") is not None:
            widget.setTitle(config["title"])
        if config.get("conversion") is not None:
            widget.setConversion(config["conversion"])
        return widget
    
    def buildImageWidget(self, config, parent):
        if not (config.get("image")):
            print ("ImageWidget has no image path")
            return None
        widget = ImageWidget(parent, config.get("image"),config.get("width") )
        return widget
    
    def buildStatusWidget(self, config, parent):
        if not (config.get("source") or config.get('status')):
            print ("StatusWidget has no source or status")
            return None
        widget = StatusWidget(parent, config.get("status"))
        widget.setSource(config["source"])
        return widget
    
    def buildButtonWidget(self, config, parent):
        if not (config.get("label") or config.get("command")):
            print ("ButtonWidget has no label or command")
            return None
        widget = ButtonWidget(parent, config.get("label"), config.get("command"))
        widget.setFieldName(config.get("fieldname"))
        widget.setView(self.view)
        return widget

    def buildTextFieldWidget(self, config, parent):
        widget = TextFieldWidget(parent, config.get("label"), config.get("value"), config.get("placeholder"), config.get("position"))
        return widget
    
    def buildChargeWidget(self, config, parent):
        widget = ChargeWidget(parent, config.get("label"))
        widget.setSource(config["source"])
        return widget
    
    def buildTextWidget(self, config, parent):
        if not (config.get("source") or config.get("mapping")):
            print ("TextWidget has no source or mapping")
            return None
        widget = TextWidget(parent, config.get("mapping"), config.get("nblines"))
        widget.setSource(config["source"])
        return widget
    
    def buildSettingsWidget(self, config, parent):
        widget = SettingsWidget(parent, self.view)
        return widget
    
    def buildOrientationWidget(self, config, parent):
        widget = OrientationWidget(parent)
        widget.setSource(config["source"])
        return widget
    
    def buildGaugeWidget(self,config,parent):
        widget = GaugeWidget(model=config["model"])
        widget.setSource(config["source"])
        widget.setLimit(config["limit"])
        widget.setStep(config["step"])
        if config.get("labelFontSize"):
            widget.setLabelFontSize(config["labelFontSize"])
        if config.get("needleWidth"):
            widget.setNeedleWidth(config["needleWidth"])
        if config.get("arcWidth"):
            widget.setArcWidth(config["arcWidth"])
        if config.get("scaleFontSize"):
            widget.setScaleFontSize(config["scaleFontSize"])
        if config.get("scaleDistance"):
            widget.setScaleDistance(config["scaleDistance"])
        return widget