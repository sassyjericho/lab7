from model.interface.interface import Interface


class BaseClass(Interface):
    def __init__(self):
        self.parameters = {}

    def set_parameter(self, params, value):
        self.parameters[params] = value

    def get_parameter(self, params):
        return self.parameters[params]
