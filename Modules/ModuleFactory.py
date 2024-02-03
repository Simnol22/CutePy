import Modules.SerialModule as SerialModule
import Modules.InfluxModule as InfluxModule
import Modules.FakeModule as FakeModule

class ModuleFactory:
    @staticmethod
    def create(module_name):
        if module_name == "serial":
            return SerialModule.SerialModule()
        elif module_name == "influx":
            return InfluxModule.InfluxModule()
        elif module_name == "fake":
            return FakeModule.FakeModule()
        else:
            print("Module not found")
            return None