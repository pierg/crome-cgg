from crome_cgg.cgg import Cgg
from crome_cgg.cgg.exceptions import CggException
from crome_contracts.contract import Contract
from crome_logic.patterns.robotic_movement import StrictOrderedPatrolling
from crome_logic.patterns.robotic_triggers import BoundDelay, BoundReaction
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

project_name = "gridworld"


# WORLD MODELING
gridworld = World(
    project_name=project_name,
    typeset=Typeset(
        {
            BooleanAction(name="greet"),
            BooleanAction(name="register"),
            BooleanLocation(
                name="r1", mutex_group="locations", adjacency_set={"r2", "r5"}
            ),
            BooleanLocation(
                name="r2", mutex_group="locations", adjacency_set={"r1", "r5"}
            ),
            BooleanLocation(
                name="r3", mutex_group="locations", adjacency_set={"r4", "r5"}
            ),
            BooleanLocation(
                name="r4", mutex_group="locations", adjacency_set={"r3", "r5"}
            ),
            BooleanLocation(
                name="r5",
                mutex_group="locations",
                adjacency_set={"r1", "r2", "r3", "r4"},
            ),
            BooleanSensor(name="person"),
            BooleanContext(name="day", mutex_group="time"),
            BooleanContext(name="night", mutex_group="time"),
        }
    ),
)

w = gridworld

# GOAL MODELING

try:
    goals = {
        Goal(
            id="day_patrol_12",
            description="During context day => start from r1, patrol r1, r2 in strict order,\n"
                        "Strict Ordered Patrolling Location r1, r2",
            context=w["day"],
            contract=Contract(
                LTL(
                    StrictOrderedPatrolling(locations=["r1", "r2"]).__str__(),
                    typeset=w.typeset,
                )
            ),
            world=w,
        ),
        Goal(
            id="night_patrol_34",
            description="During context night => start from r3, patrol r3, r4 in strict order,\n"
                        "Strict Ordered Patrolling Location r3, r4",
            context=w["night"],
            contract=Contract(
                LTL(
                    StrictOrderedPatrolling(locations=["r3", "r4"]).__str__(),
                    typeset=w.typeset,
                )
            ),
            world=w,
        ),
        Goal(
            id="greet_person",
            description="Always => if see a person, greet in the same step,\n"
                        "Only if see a person, greet immediately",
            contract=Contract(
                LTL(
                    BoundReaction(pre="person", post="greet").__str__(),
                    typeset=w.typeset,
                )
            ),
            world=w,
        ),
        Goal(
            id="register_person",
            description="During context day => if see a person, register in the next step,\n"
                        "Only if see a person, register in the next step",
            context=w["day"],
            contract=Contract(
                LTL(
                    BoundDelay(pre="person", post="register").__str__(),
                    typeset=w.typeset,
                )
            ),
            world=w,
        ),
    }

except CggException as e:
    raise e

# CGG BUILDING

cgg = Cgg(init_goals=goals)

