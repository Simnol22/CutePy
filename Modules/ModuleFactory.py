import Modules.SerialModule as SerialModule
import Modules.InfluxModule as InfluxModule
import Modules.FakeModule as FakeModule

class ModuleFactory:
    @staticmethod
    def create(module_name):
        if module_name == "Serial":
            return SerialModule.SerialModule()
        elif module_name == "Influx":
            return InfluxModule.InfluxModule()
        elif module_name == "Fake":
            return FakeModule.FakeModule()
        else:
            print("Module not found")
            return None