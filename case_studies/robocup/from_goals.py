import os
from pathlib import Path

from crome_cgg.goal import Goal
from crome_cgg.goal.operations.composition import g_composition
from crome_cgg.rule import Rule
from crome_cgg.world import World
from crome_contracts.contract import Contract
from crome_logic.patterns.robotic_triggers import InstantaneousReaction
from crome_logic.specification.temporal import LTL
from crome_logic.tools.crome_io import save_to_file
from crome_logic.typelement.robotic import BooleanLocation, BooleanAction, BooleanSensor
from crome_logic.typeset import Typeset

w = World(
    project_name="robotcup",
    typeset=Typeset(
        {
            BooleanLocation(
                name="l1", mutex_group="locations", adjacency_set={"l2", "l4"}, refinement_of={"lv"}
            ),
            BooleanLocation(
                name="l2", mutex_group="locations", adjacency_set={"l1", "l3", "l5", "h1", "b2"}, refinement_of={"lv"}
            ),
            BooleanLocation(
                name="l3", mutex_group="locations", adjacency_set={"l2", "l6", "k1", "h2"}, refinement_of={"lv"}
            ),
            BooleanLocation(
                name="l4", mutex_group="locations", adjacency_set={"l1", "l5"}, refinement_of={"lv"}
            ),
            BooleanLocation(
                name="l5", mutex_group="locations", adjacency_set={"l4", "l2", "l6"}, refinement_of={"lv"}
            ),
            BooleanLocation(
                name="l6", mutex_group="locations", adjacency_set={"l5", "l3"}, refinement_of={"lv"}
            ),
            BooleanLocation(
                name="b1", mutex_group="locations", adjacency_set={"b2", "b3"}, refinement_of={"lb"}
            ),
            BooleanLocation(
                name="b2", mutex_group="locations", adjacency_set={"b1", "b3", "l2"}, refinement_of={"lb"}
            ),
            BooleanLocation(
                name="b3", mutex_group="locations", adjacency_set={"b1", "b2"}, refinement_of={"lb"}
            ),
            BooleanLocation(
                name="h1", mutex_group="locations", adjacency_set={"l2", "h2"}, refinement_of={"lh"}
            ),
            BooleanLocation(
                name="h2", mutex_group="locations", adjacency_set={"h1", "l3", "e2"}, refinement_of={"lb"}
            ),
            BooleanLocation(
                name="e1", mutex_group="locations", adjacency_set={"e2"}, refinement_of={"le"}
            ),
            BooleanLocation(
                name="e2", mutex_group="locations", adjacency_set={"e1", "h2"}, refinement_of={"le"}
            ),
            BooleanLocation(
                name="r1", mutex_group="locations", adjacency_set={"l3", "r2"}, refinement_of={"lr"}
            ),
            BooleanLocation(
                name="r2", mutex_group="locations", adjacency_set={"r1"}, refinement_of={"lr"}
            ),
            BooleanLocation(
                name="k1", mutex_group="locations", adjacency_set={"l3", "k2", "k3"}, refinement_of={"lk"}
            ),
            BooleanLocation(
                name="k2", mutex_group="locations", adjacency_set={"k1", "k3"}, refinement_of={"lk"}
            ),
            BooleanLocation(
                name="k3", mutex_group="locations", adjacency_set={"k2", "k1"}, refinement_of={"lg"}
            ),
            BooleanAction(
                name="hl", description="hold an object"
            ),
            BooleanAction(
                name="dp", description="drop an object in the current location", mutex_group="actions"
            ),
            BooleanAction(
                name="pu", description="pickup the object in the current location", mutex_group="actions"
            ),
            BooleanAction(
                name="id", description="idle", mutex_group="actions"
            ),
            BooleanSensor(
                name="oj", description="object detected in the current location"
            ),

        }
    ),
)

"""Environment Rules"""
w.environment_rules = {
    Rule(
        description="if the robot has the object, then objects disappears",
        specification=LTL("G(hl -> !oj)", _typeset=w.typeset)
    )
}


"""System Rules"""
w.system_rules = {
    Rule(
        description="keep robots with free hands",
        specification=LTL("GF(!hl)", _typeset=w.typeset)
    ),
    Rule(
        description="keep holding unless the robot drops the object",
        specification=LTL("GF((hl & !dp) -> X hl)", _typeset=w.typeset)
    ),
    Rule(
        description="if it drops the object then it does not hold anymore in the next step",
        specification=LTL("G(dp -> X !hl)", _typeset=w.typeset)
    ),
    Rule(
        description="if it drops an object in the next step then it is holding an object currently",
        specification=LTL("G((X dp) -> hl)", _typeset=w.typeset)
    )
}


g1 = Goal(
        id="g1",
        description="drop only when you are in the garbage location and you're holding an object",
        contract=Contract(
            _guarantees=LTL(InstantaneousReaction(pre="k3 & hl", post="dp"), _typeset=w.typeset)
        ),
        world=w
    )

g2 = Goal(
        id="g2",
        description="",
        contract=Contract(
            _guarantees=LTL(InstantaneousReaction(pre="k3 & hl", post="dp"), _typeset=w.typeset)
        ),
        world=w
    )

goals = {
    Goal(
        id="g1",
        description="drop only when you are in the garbage location and you're holding an object",
        contract=Contract(
            _guarantees=LTL(InstantaneousReaction(pre="k3 & hl", post="dp"), _typeset=w.typeset)
        ),
        world=w
    ),
    Goal(
        id="g2",
        description="",
        contract=Contract(
            _guarantees=LTL(InstantaneousReaction(pre="k3 & hl", post="dp"), _typeset=w.typeset)
        ),
        world=w
    )
}

output_folder: Path = Path(os.path.dirname(__file__)) / "output"

g = g_composition(goals)
g.realize()
save_to_file(file_content=g.controller.spec.to_str, file_name="spec", absolute_folder_path=output_folder)
g.controller.save("png", file_name="mealy", absolute_folder_path=output_folder)
print(g.controller.mealy)
simulation = g.controller.mealy.simulate(50)
print(simulation)
save_to_file(file_content=simulation, file_name="simulation", absolute_folder_path=output_folder)

