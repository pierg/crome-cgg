from crome_cgg.goal import Goal
from crome_cgg.goal.operations.merging import g_merging
from crome_cgg.goal.operations.separation import g_separation
from crome_cgg.world import World
from crome_contracts.contract import Contract
from crome_logic.patterns.robotic_movement import StrictOrderedPatrolling, Patrolling, OrderedPatrolling
from crome_logic.specification.temporal import LTL
from crome_logic.tools.string_manipulation import latexit
from crome_logic.typelement.robotic import (
    BooleanLocation,
)
from crome_logic.typeset import Typeset



top_spec = Goal(contract=Contract(_assumptions=LTL("a1"), _guarantees=LTL("g1")))

print(f"TOP_SPEC:\n{top_spec}")

lib_spec = Goal(contract=Contract(_assumptions=LTL("a2"), _guarantees=LTL("g2")))


print(f"LIB_SPEC:\n{lib_spec}")



sep = g_separation(lib_spec, top_spec)
print(f"M1:\n{sep}")


new = g_merging({top_spec, sep})
print(f"M2:\n{new}")

print(new.contract.assumptions.boolean.dnf)
print(new.contract.guarantees.boolean.cnf)
