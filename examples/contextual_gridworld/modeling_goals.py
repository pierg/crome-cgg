from crome_contracts.contract import Contract
from crome_logic.patterns.robotic_movement import StrictOrderedPatrolling
from crome_logic.patterns.robotic_triggers import BoundDelay, BoundReaction
from crome_logic.specification.temporal import LTL

from crome_cgg.cgg.exceptions import CggException
from crome_cgg.goal import Goal
from crome_cgg.tools.persistence import dump_goals
from examples.contextual_gridworld import project_name
from examples.contextual_gridworld.modeling_world import gridworld

w = gridworld

try:

    """Modeling the set of goals using robotic robotic.json."""
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

    """Save set of goals so that they can be loaded later"""
    dump_goals(goals, folder_name=project_name)

except CggException as e:
    raise e
