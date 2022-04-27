from crome_cgg.cgg import Cgg
from crome_cgg.tools.persistence import dump_world, load_world, dump_goals, load_goals, dump_cgg, load_cgg
from crome_contracts.contract import Contract
from crome_logic.patterns.robotic_movement import StrictOrderedPatrolling
from crome_logic.specification.temporal import LTL
from crome_logic.typeelement.robotic import (
    BooleanAction,
    BooleanContext,
    BooleanLocation,
    BooleanSensor,
)
from crome_logic.typeset import Typeset

from crome_cgg.goal import Goal
from crome_cgg.world import World

project_name = "gridworld_persistence"

w = World(
    project_name=project_name,
    typeset=Typeset(
        {
            BooleanAction(name="greet"),
            BooleanLocation(
                name="r1", mutex_group="locations", adjacency_set={"r2", "r5"}
            ),
            BooleanLocation(
                name="r3", mutex_group="locations", adjacency_set={"r2", "r5"}
            ),
            BooleanSensor(name="person"),
            BooleanContext(name="day", mutex_group="time"),
            BooleanContext(name="night", mutex_group="time")
        }
    ),
)

dump_world(w, folder_name=project_name)
w_retrieved = load_world(folder_name=project_name)
assert w == w_retrieved

goals = {Goal(
    id="day_patrol_12",
    description="During context day => start from r1, patrol r1, r2 in strict order,\n"
                "Strict Ordered Patrolling Location r1, r2",
    context=w["day"],
    contract=Contract(
        LTL(
            StrictOrderedPatrolling(locations=["r1"]).__str__(),
            typeset=w.typeset,
        )
    ),
    world=w),
    Goal(
        id="night_patrol_34",
        description="During context night => start from r3, patrol r3, r4 in strict order,\n"
                    "Strict Ordered Patrolling Location r3, r4",
        context=w["night"],
        contract=Contract(
            LTL(
                StrictOrderedPatrolling(locations=["r3"]).__str__(),
                typeset=w.typeset,
            )
        ),
        world=w,
    )
}

dump_goals(goals, folder_name=project_name)
goals_retrieved = load_goals(folder_name=project_name)
assert goals == goals_retrieved


cgg = Cgg(init_goals=goals)

dump_cgg(cgg, folder_name=project_name)
cgg_retrieved = load_cgg(folder_name=project_name)
# TODO: [PIER] Check why objects are slightly different
assert cgg == cgg_retrieved
