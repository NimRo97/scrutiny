import jsonpickle

class Device(object):

    def __init__(self, name):
        self.name = name
        self.modules = {}

    def add_module(self, module):
        self.modules[module.module_name] = module

    def add_modules(self, modules):
        for module in modules:
            self.add_module(module)

    def __str__(self):
        return jsonpickle.encode(self, indent=4)


def load_device(filename):
    with open(filename, "r") as f:
        return jsonpickle.decode(f.read())