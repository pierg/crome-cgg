from crome_cgg.src.crome_cgg.goal import Goal
from crome_cgg.src.crome_cgg.library import Library
from crome_synthesis.src.crome_synthesis.world import World
from crome_contracts.src.crome_contracts.contract import Contract
from crome_logic.src.crome_logic.patterns.robotic_movement import Patrolling, OrderedPatrolling, Visit
from crome_logic.src.crome_logic.specification.temporal import LTL
from crome_logic.src.crome_logic.typelement.robotic import (
    BooleanLocation, BooleanSensor, BooleanAction,
)
from crome_logic.src.crome_logic.typeset import Typeset

project_name = "mission_repair"

abs_world = World(
    project_name=project_name,
    typeset=Typeset(
        {
            BooleanLocation(name="lf",
                            description="front", mutex_group="abstract_locs", adjacency_set={"lb"}
                            ),
            BooleanLocation(name="lb",
                            description="back", mutex_group="abstract_locs", adjacency_set={"lf"}
                            ),
            BooleanLocation(
                name="le", description="entrance", refinement_of={"lf"}
            ),
            BooleanSensor(
                name="s", description="person detected"
            ),
            BooleanAction(
                name="g", description="greeting"
            ),
        }
    ),
)

lib_world = World(
    project_name=project_name,
    typeset=Typeset(
        {
            BooleanLocation(
                name="l1", mutex_group="locations", adjacency_set={"l3", "l2"}, refinement_of={"lf"}
            ),
            BooleanLocation(
                name="l2", mutex_group="locations", adjacency_set={"l1", "l4"}, refinement_of={"le"}
            ),
            BooleanLocation(
                name="l3", mutex_group="locations", adjacency_set={"l1", "l4", "l5"}, refinement_of={"lf"}
            ),
            BooleanLocation(
                name="l4", mutex_group="locations", adjacency_set={"l3", "l2"}, refinement_of={"lf"}
            ),
            BooleanLocation(
                name="l5", mutex_group="locations", adjacency_set={"l3"}, refinement_of={"lb"}
            ),
        }
    ),
)

library_goals = {
    Goal(
        id="l1",
        contract=Contract(LTL(Patrolling(["l1", "l5"]), lib_world.typeset)),
        world=lib_world,
    ),
    Goal(
        id="l2",
        contract=Contract(LTL(Patrolling(["l3"]), lib_world.typeset)),
        world=lib_world,
    ),
    Goal(
        id="l3",
        contract=Contract(LTL(Visit(["l3", "l1"]), lib_world.typeset)),
        world=lib_world,
    ),
    Goal(
        id="l4",
        contract=Contract(LTL(Visit(["l5"]), lib_world.typeset)),
        world=lib_world,
    ),
}


goal_to_refine = Goal(
    id="ordered_patrolling",
    contract=Contract(
        # _assumptions=LTL(GF("s")),
        _guarantees=LTL(f'{OrderedPatrolling(["lf", "lb"])}', abs_world.typeset)),
    world=abs_world,
)

print(goal_to_refine)

library = Library(library_goals)

candidate_composition = library.get_candidate_composition(goal_to_refine=goal_to_refine)

print(candidate_composition)

print(candidate_composition.contract <= goal_to_refine.contract)
