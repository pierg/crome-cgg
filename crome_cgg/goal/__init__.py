from __future__ import annotations

from dataclasses import dataclass, field

from crome_contracts.contract import Contract
from crome_logic.specification.boolean import Bool
from crome_logic.typesimple.subtype.robotic.context import ContextType
from crome_synthesis.controller import Controller

from crome_cgg.context import Context
from crome_cgg.tools.strings import generate_goal_name
from crome_cgg.world import World


@dataclass
class Goal:
    contract: Contract
    name: str = ""

    description: str = ""
    context: Context = Context(formula="TRUE")
    world: World | None = None

    _controller: Controller | None = field(init=False, repr=False, default=None)

    def __post_init__(self):
        if self.name == "":
            print(repr(self.contract))
            self.name = generate_goal_name(repr(self.contract))

        if self.world is None:
            self.world = World(self.contract.typeset)
        else:
            self.world = World(self.contract.typeset + self.world.typeset)

    @property
    def realizable(self) -> bool | None:
        if self.controller is not None:
            return self.controller.realizable
        return None

    @property
    def controller(self) -> Controller | None:
        return self._controller

    def realize(self):
        self._controller = Controller(
            self.contract.assumptions, self.contract.guarantees
        )
