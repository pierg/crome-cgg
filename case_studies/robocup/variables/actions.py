from core.type.subtypes.action import *


class Hold(BooleanAction):

    def __init__(self, name: str = "hold"):
        super().__init__(name)


class Drop(BooleanAction):

    def __init__(self, name: str = "drop"):
        super().__init__(name)


class Reply(BooleanAction):

    def __init__(self, name: str = "reply"):
        super().__init__(name)


class Store(BooleanAction):

    def __init__(self, name: str = "store"):
        super().__init__(name)
