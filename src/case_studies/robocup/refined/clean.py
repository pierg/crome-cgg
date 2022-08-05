import os
from pathlib import Path

from crome_cgg.src.case_studies.robocup.world.world_ref import w_ref
from crome_cgg.src.crome_cgg.goal import Goal
from crome_cgg.src.crome_cgg.goal.operations.composition import g_composition
from crome_contracts.src.crome_contracts.contract import Contract
from crome_logic.src.crome_logic.patterns.robotic_triggers import InstantaneousReaction, InitInstantaneousReaction
from crome_logic.src.crome_logic.specification.temporal import LTL
from crome_logic.src.crome_logic.tools.crome_io import save_to_file
from crome_synthesis.src.crome_synthesis.rule import Rule

folder_spec_name: str = "clean"
output_folder: Path = Path(os.path.dirname(__file__)).parent / "output" / "ref" / folder_spec_name

"""Environment Rules"""
w_ref.environment_rules = {
    Rule(
        description="Place garbage in location l1, l5 and h1",
        specification=LTL(InitInstantaneousReaction.iterate_over_preconditions(["l1", "l5", "h1"], "oj"), _typeset=w_ref.typeset)
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
        specification=LTL("G((hl & !dp) -> X hl)", _typeset=w_ref.typeset)
    ),
    Rule(
        description="if it drops the object then it does not hold anymore in the next step",
        specification=LTL("G(dp -> X !hl)", _typeset=w_ref.typeset)
    ),
    Rule(
        description="if it drops an object in the next step then it is holding an object currently",
        specification=LTL("G((X dp) -> hl)", _typeset=w_ref.typeset)
    ),
}


goals = {
    Goal(
        id="g1",
        description="drop only when you are in the garbage location and you're holding an object",
        contract=Contract(
            _guarantees=LTL(InstantaneousReaction(pre="dp", post="k3 & hl"), _typeset=w_ref.typeset)
        ),
        world=w_ref
    )
}

g = g_composition(goals)
g.realize()
save_to_file(file_content=g.controller.spec.to_str, file_name="spec", absolute_folder_path=output_folder)
g.controller.save("png", file_name="spec", absolute_folder_path=output_folder)
simulation = g.controller.simulate(50)
save_to_file(file_content=simulation, file_name=f"run", absolute_folder_path=output_folder)
print(g.controller.mealy)
print(simulation)