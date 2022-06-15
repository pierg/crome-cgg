from case_studies.minimal.world.world_ref import w_ref
from case_studies.minimal.world.world_top import w_top
from crome_logic.specification.temporal import LTL

""""
|a1 | b1|
|a2 | b2|

G(a <-> (a1 | a2) & G(b <-> (b1 | b2)
"""

phi1 = LTL("a & X b", _typeset=w_top.typeset)
phi2 = LTL("a1 & X b1", _typeset=w_ref.typeset)

assert phi2 <= phi1

phi1 = LTL("a & X b", _typeset=w_top.typeset)
phi2 = LTL("a1 & X b2", _typeset=w_ref.typeset)

assert not phi2 <= phi1


phi1 = LTL("a & X b", _typeset=w_top.typeset)
phi2 = LTL("a1 & F b1", _typeset=w_ref.typeset)

assert not phi2 <= phi1


phi1 = LTL("a & X b", _typeset=w_top.typeset)
phi2 = LTL("a1 & F b1", _typeset=w_ref.typeset)

assert not phi2 <= phi1

