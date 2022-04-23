from __future__ import annotations

from dataclasses import dataclass, field

from crome_contracts.contract import Contract
from crome_logic.specification.temporal import LTL
from crome_synthesis.controller import Controller

from crome_cgg.context import Context
from crome_cgg.tools.names import generate_goal_id
from crome_cgg.world import World


@dataclass
class Goal:
    contract: Contract
    id: str = ""
    description: str = ""
    context: Context = Context(formula="TRUE")
    world: World = field(default_factory=lambda: World())
    viewpoint: str = ""

    _parents: dict = field(init=False, repr=False, default_factory=dict)
    _children: dict = field(init=False, repr=False, default_factory=dict)

    _controller: Controller | None = field(init=False, repr=False, default=None)

    def __hash__(self):
        return hash(
            self.id
            + self.description
            + self.context.__str__()
            + self.world.__str__()
            + self.contract.__str__()
        )

    def __post_init__(self):
        if self.id == "":
            self.id = generate_goal_id(repr(self.contract))

        if len(self.world) == 0:
            self.world = World(typeset=self.contract.typeset)
        else:
            self.world = World(typeset=self.contract.typeset + self.world.typeset)

        if self.viewpoint == "":
            self.viewpoint: str = self.contract.typeset.extract_viewpoint()

    @property
    def controller(self) -> Controller | None:
        return self._controller

    def realize(self):
        self._controller = Controller(
            self.contract.assumptions, self.contract.guarantees
        )


if __name__ == "__main__":
    g = Goal(contract=Contract(LTL("Ga")))
    print(g.world)
