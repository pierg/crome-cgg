from core.type.subtypes.context import ContextBooleanTime, ContextBooleanMode


class Housekeeping(ContextBooleanTime):

    def __init__(self, name: str = "housekeeping"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "time"


class Party(ContextBooleanTime):

    def __init__(self, name: str = "party"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "time"


class Cleanup(ContextBooleanMode):

    def __init__(self, name: str = "cleanup"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "modes"


class Groceries(ContextBooleanMode):

    def __init__(self, name: str = "groceries"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "modes"


class Garbage(ContextBooleanMode):

    def __init__(self, name: str = "garbage"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "modes"
