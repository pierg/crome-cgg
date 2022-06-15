from case_studies.robocup.world.world_ref import w_ref
from case_studies.robocup.world.world_top import w_top
from crome_logic.patterns.robotic_movement import *
from crome_logic.specification.temporal import LTL


phi1 = LTL(OrderedPatrolling(["lb", "lv"]), _typeset=w_top.typeset)
phi2 = LTL(OrderedPatrolling(["b2", "l2"]), _typeset=w_ref.typeset)

print(OrderedPatrolling(["lb", "lv"]))
print(OrderedPatrolling(["b2", "l2"]))

assert phi2 <= phi1

# phi1 = LTL("!lb & Flb", _typeset=w_top.typeset)
# phi2 = LTL("l3 & F(b1)", _typeset=w_ref.typeset)
#
# print(phi1)
# print(phi2)
#
# assert phi2 <= phi1
