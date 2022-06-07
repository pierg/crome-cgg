from core.type.subtypes.sensor import *


class ObjectRecognized(BooleanSensor):

    def __init__(self, name: str = "object_recognized"):
        super().__init__(name)


class GroceriesRecognized(BooleanSensor):

    def __init__(self, name: str = "groceries_recognized"):
        super().__init__(name)


class Alexa(BooleanSensor):

    def __init__(self, name: str = "alexa"):
        super().__init__(name)
