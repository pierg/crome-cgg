from src.crome_cgg.goal import Goal
from src.crome_synthesis.world import World
from src.crome_contracts.contract import Contract
from src.crome_logic.patterns.robotic_movement import Patrolling, OrderedPatrolling
from src.crome_logic.specification.temporal import LTL
from src.crome_logic.typelement.robotic import (
    BooleanLocation,
)
from src.crome_logic.typeset import Typeset

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
                name="lc", description="charge", refinement_of={"lf"}
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
                name="l2", mutex_group="locations", adjacency_set={"l1", "l4"}, refinement_of={"lc"}
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


def incompatible_library():
    top = Goal(contract=Contract(LTL(_init_formula=Patrolling(["lf", "lc"]), _typeset=abs_world.typeset)),
               world=abs_world)
    ref = Goal(contract=Contract(LTL(_init_formula=Patrolling(["l5", "l3"]), _typeset=lib_world.typeset)),
               world=lib_world)
    ref_score = top.compare_with(ref)
    print(f"REFINEMENT SCORE:\n{ref_score}")


def refinement_completed():
    top = Goal(contract=Contract(LTL(_init_formula=Patrolling(["lf", "lc"]), _typeset=abs_world.typeset)),
               world=abs_world)
    ref = Goal(contract=Contract(LTL(_init_formula=OrderedPatrolling(["l5", "l2"]), _typeset=lib_world.typeset)),
               world=lib_world)
    ref_score = top.compare_with(ref)
    print(f"REFINEMENT SCORE:\n{ref_score}")


def search():
    pass


def repair():
    pass



print(ref <= top)

def refinement_score(top: Goal, ref: Goal) -> float:
    top.compare_with(ref)
    print(top)
    print(top.boolean)
    print(ref)
    print(ref.boolean)
    print("WAIT")



if __name__ == '__main__':
    refinement_score(top, ref)