from crome_synthesis.world import World
from crome_contracts.contract import Contract
from crome_cgg.goal import Goal
from crome_cgg.goal.operations.merging import g_merging
from crome_cgg.goal.operations.separation import g_separation
from crome_logic.patterns.robotic_movement import OrderedPatrolling, Patrolling
from crome_logic.specification.temporal import LTL
from crome_logic.tools.string_manipulation import latexit
from crome_logic.typelement.robotic import BooleanAction, BooleanLocation, BooleanSensor
from crome_logic.typeset import Typeset

project_name = "mission_repair"

abs_world = World(
    project_name=project_name,
    typeset=Typeset(
        {
            BooleanLocation(
                name="lf",
                description="front",
                mutex_group="abstract_locs",
                adjacency_set={"lb"},
            ),
            BooleanLocation(
                name="lb",
                description="back",
                mutex_group="abstract_locs",
                adjacency_set={"lf"},
            ),
            BooleanLocation(name="lc", description="charge", refinement_of={"lf"}),
            BooleanSensor(name="s", description="person detected"),
            BooleanAction(name="g", description="greeting"),
        }
    ),
)

ordered_patrolling_top = LTL(
    _init_formula=OrderedPatrolling(["lf", "lb"]), _typeset=abs_world.typeset
)
print(latexit(ordered_patrolling_top.formula))

top_spec = Goal(contract=Contract(_guarantees=ordered_patrolling_top))


print(f"TOP_SPEC:\n{top_spec}")

lib_world = World(
    project_name=project_name,
    typeset=Typeset(
        {
            BooleanLocation(
                name="l1",
                mutex_group="locations",
                adjacency_set={"l3", "l2"},
                refinement_of={"lf"},
            ),
            BooleanLocation(
                name="l2",
                mutex_group="locations",
                adjacency_set={"l1", "l4"},
                refinement_of={"lc"},
            ),
            BooleanLocation(
                name="l3",
                mutex_group="locations",
                adjacency_set={"l1", "l4", "l5"},
                refinement_of={"lf"},
            ),
            BooleanLocation(
                name="l4",
                mutex_group="locations",
                adjacency_set={"l3", "l2"},
                refinement_of={"lf"},
            ),
            BooleanLocation(
                name="l5",
                mutex_group="locations",
                adjacency_set={"l3"},
                refinement_of={"lb"},
            ),
        }
    ),
)


lib_spec = Goal(
    contract=Contract(
        _guarantees=LTL(
            _init_formula=Patrolling(["l5", "l1"]), _typeset=lib_world.typeset
        )
    )
)

print(f"LIB_SPEC:\n{lib_spec}")

print(lib_spec <= top_spec)

assert not lib_spec <= top_spec
print(lib_spec <= top_spec)

sep = g_separation(lib_spec, top_spec)
print(f"SEPARATION:\n{sep}")
print(latexit(sep.contract.assumptions.formula))
print(latexit(sep.contract.guarantees.formula))

new = g_merging({top_spec, sep})
print(f"MERGING RES:\n{new}")
print(latexit(new.contract.assumptions.formula))
print(latexit(new.contract.guarantees.formula))

print("\n\n")
print(lib_spec)
print("REFINES")
print(new)
print(lib_spec <= new)
