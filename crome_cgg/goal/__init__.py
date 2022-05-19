from __future__ import annotations

from dataclasses import dataclass, field

from crome_cgg.context import Context
from crome_cgg.tools.names import generate_goal_id
from crome_cgg.world import World
from crome_contracts.contract import Contract
from crome_logic.specification.temporal import LTL
from crome_synthesis.controller import Controller
from tools.strings import tab


@dataclass
class Goal:
    contract: Contract
    id: str = ""
    description: str = ""
    context: Context = Context(_init_formula="TRUE")
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

    def __le__(self: Goal, other: Goal):
        return self.contract <= other.contract

    @property
    def controller(self) -> Controller | None:
        return self._controller

    def realize(self):
        self._controller = Controller(self.contract.assumptions, self.contract.guarantees)

    def __str__(self):
        res = []

        res.append(tab(f"GOAL {self.id}", how_many=0, init_character="|---"))
        if not self.context.is_true_expression:
            res.append(tab("CONTEXT", how_many=1, init_character="|"))
            res.append(tab(str(self.context), how_many=2, init_character="|"))

        res.append(tab(str(self.contract), how_many=1, init_character="|"))

        return "\n".join(res)

if __name__ == "__main__":
    g = Goal(contract=Contract(LTL("Ga")))
    print(g)
