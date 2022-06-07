from core.type.subtypes.location import *


class L1(ReachLocation):

    def __init__(self, name: str = "l1"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"L2", "L4"}


class L2(ReachLocation):

    def __init__(self, name: str = "l2"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"B2", "L1", "H1", "L3", "L5"}


class L3(ReachLocation):

    def __init__(self, name: str = "l3"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"L2", "L6", "K1", "R1", "H2"}


class L4(ReachLocation):

    def __init__(self, name: str = "l4"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"L1", "L5"}


class L5(ReachLocation):

    def __init__(self, name: str = "l5"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"L4", "L6", "L2"}


class L6(ReachLocation):

    def __init__(self, name: str = "l6"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"L5", "L3"}


class K1(ReachLocation):

    def __init__(self, name: str = "k1"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"L3", "K2", "K3"}


class K2(ReachLocation):

    def __init__(self, name: str = "k2"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"K1", "K3"}


class K3(ReachLocation):

    def __init__(self, name: str = "k3"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"K1", "K2"}


class B1(ReachLocation):

    def __init__(self, name: str = "b1"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"B1", "B2", "B3"}


class B2(ReachLocation):

    def __init__(self, name: str = "b2"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"B1", "B3", "L2"}


class B3(ReachLocation):

    def __init__(self, name: str = "b3"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"B1", "B2"}


class H1(ReachLocation):

    def __init__(self, name: str = "h1"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"H2", "L2"}


class H2(ReachLocation):

    def __init__(self, name: str = "h2"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"H1", "E2", "L3"}

class E1(ReachLocation):

    def __init__(self, name: str = "e1"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"E2"}


class E2(ReachLocation):

    def __init__(self, name: str = "e2"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"E1", "H2"}


class R1(ReachLocation):

    def __init__(self, name: str = "r1"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"R2", "L3"}


class R2(ReachLocation):

    def __init__(self, name: str = "r2"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"R1"}



