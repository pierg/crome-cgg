from crome_cgg.case_studies.minimal.world.world_ref import w_ref
from crome_cgg.case_studies.minimal.world.world_top import w_top
from crome_logic.patterns.robotic_movement import OrderedVisit, StrictOrderedVisit
from crome_logic.specification.temporal import LTL

""""
|a1 | b1|
|a2 | b2|

G(a <-> (a1 | a2) & G(b <-> (b1 | b2)
"""

# WORKING

phi1 = LTL(OrderedVisit(["a", "b"]), _typeset=w_top.typeset)
# Fa & Fb & (!b U a)

phi2 = LTL(StrictOrderedVisit(["a1", "b1"]), _typeset=w_ref.typeset)
# Fa1 & Fb1 & (!b1 U a1) & (!a1 U a1) & X(!a1 U b1)

assert phi2 <= phi1

# NOT WORKING


phi1 = LTL(StrictOrderedVisit(["a", "b"]), _typeset=w_top.typeset)
# Fa & Fb & (!b U a) & (!a U a) & X(!a U b)

phi2 = LTL(StrictOrderedVisit(["a1", "b1"]), _typeset=w_ref.typeset)
# Fa1 & Fb1 & (!b1 U a1) & (!a1 U a1) & X(!a1 U b1)


assert not phi2 <= phi1

# REPAIRING REFINEMENT

phi1 = LTL("Fa  & Fb  & (!b U a)  & X(!a U b)", _typeset=w_top.typeset)
phi2 = LTL("Fa1 & Fb1 & (!b1 U a1) & X(!(a1 | a2) U b1)", _typeset=w_ref.typeset)

assert phi2 <= phi1
