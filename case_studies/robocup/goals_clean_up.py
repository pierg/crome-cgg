import os
from pathlib import Path

from case_studies.robocup.world.world_ref import w_ref
from crome_cgg.goal import Goal
from crome_cgg.goal.operations.composition import g_composition

from crome_contracts.contract import Contract
from crome_logic.patterns.robotic_triggers import InstantaneousReaction
from crome_logic.specification.temporal import LTL
from crome_logic.tools.crome_io import save_to_file
from crome_synthesis.rule import Rule

"""Environment Rules"""
w_ref.environment_rules = {
    Rule(
        description="if the robot has the object, then objects disappears",
        specification=LTL("G(hl -> !oj)", _typeset=w_ref.typeset)
    )
}

"""System Rules"""
w_ref.system_rules = {
    Rule(
        description="keep robots with free hands",
        specification=LTL("GF(!hl)", _typeset=w_ref.typeset)
    ),
    Rule(
        description="keep holding unless the robot drops the object",
        specification=LTL("GF((hl & !dp) -> X hl)", _typeset=w_ref.typeset)
    ),
    Rule(
        description="if it drops the object then it does not hold anymore in the next step",
        specification=LTL("G(dp -> X !hl)", _typeset=w_ref.typeset)
    ),
    Rule(
        description="if it drops an object in the next step then it is holding an object currently",
        specification=LTL("G((X dp) -> hl)", _typeset=w_ref.typeset)
    )
}

g1 = Goal(
    id="g1",
    description="drop only when you are in the garbage location and you're holding an object",
    contract=Contract(
        _guarantees=LTL(InstantaneousReaction(pre="k3 & hl", post="dp"), _typeset=w_ref.typeset)
    ),
    world=w_ref
)

g2 = Goal(
    id="g2",
    description="",
    contract=Contract(
        _guarantees=LTL(InstantaneousReaction(pre="k3 & hl", post="dp"), _typeset=w_ref.typeset)
    ),
    world=w_ref
)

goals = {
    Goal(
        id="g1",
        description="drop only when you are in the garbage location and you're holding an object",
        contract=Contract(
            _guarantees=LTL(InstantaneousReaction(pre="k3 & hl", post="dp"), _typeset=w_ref.typeset)
        ),
        world=w_ref
    ),
    Goal(
        id="g2",
        description="",
        contract=Contract(
            _guarantees=LTL(InstantaneousReaction(pre="k3 & hl", post="dp"), _typeset=w_ref.typeset)
        ),
        world=w_ref
    )
}

spec_name = "top"
output_folder: Path = Path(os.path.dirname(__file__)) / "output"

g = g_composition(goals)
g.realize()
save_to_file(file_content=g.controller.spec.to_str, file_name=spec_name, absolute_folder_path=output_folder)
g.controller.save("png", file_name=spec_name, absolute_folder_path=output_folder)
simulation = g.controller.mealy.simulate(50)
save_to_file(file_content=simulation, file_name=f"{spec_name}_run", absolute_folder_path=output_folder)
print(g.controller.mealy)
print(simulation)