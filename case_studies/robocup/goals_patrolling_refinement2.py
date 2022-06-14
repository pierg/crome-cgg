from case_studies.robocup.world.world_ref import w_ref
from case_studies.robocup.world.world_top import w_top
from crome_cgg.goal import Goal
from crome_cgg.goal.operations.composition import g_composition
from crome_contracts.contract import Contract
from crome_logic.patterns.basic import *
from crome_logic.patterns.robotic_movement import *
from crome_logic.patterns.robotic_triggers import *
from crome_logic.specification.temporal import LTL
from crome_synthesis.controller import Controller

c = Contract(_guarantees=LTL(OrderedPatrolling(["lb", "lv"]), _typeset=w_top.typeset))

goals_top = {
    Goal(
        id="init",
        contract=Contract(_guarantees=LTL(Init("lb"), _typeset=w_top.typeset)),
        world=w_top
    ),
    Goal(
        id="order_patrol",
        contract=Contract(_guarantees=LTL(OrderedPatrolling(["lb", "lv"]), _typeset=w_top.typeset)),
        world=w_top
    ),
    Goal(
        id="cleanup",
        contract=Contract(_guarantees=LTL(InstantaneousReaction("oj", "hl"), _typeset=w_top.typeset)),
        world=w_top
    ),
    Goal(
        id="drop",
        description="drop only when you are in the garbage location and you're holding an object",
        contract=Contract(
            _guarantees=LTL(InstantaneousReaction(pre="lg & oj", post="dp"), _typeset=w_ref.typeset)
        ),
        world=w_ref
    ),
    Goal(
        id="remove",
        description="remove all the objects continuously",
        contract=Contract(
            _guarantees=LTL(InfOft("!ob"), _typeset=w_ref.typeset)
        ),
        world=w_ref
    )
}

goals = g_composition(goals_top)
goals.realize()

goals_ref = {
    Goal(
        id="init",
        contract=Contract(_guarantees=LTL(Init("b1"), _typeset=w_ref.typeset)),
        world=w_ref
    ),
    Goal(
        id="g1",
        contract=Contract(_guarantees=LTL(OrderedPatrolling(["(b1 | b2 | b3)", "(l1 | l2 | l3 | l4 | l5 | l6)"]),
                                          _typeset=w_ref.typeset)),
        world=w_ref
    ),
    Goal(
        id="g1",
        contract=Contract(_guarantees=LTL(OrderedPatrolling(["b2", "l2"]),
                                          _typeset=w_ref.typeset)),
        world=w_ref
    )
}

phi1 = LTL(OrderedPatrolling(["lb", "lv"]), _typeset=w_top.typeset)

Controller.from_ltl(phi1)

phi2 = LTL(OrderedPatrolling(["b2", "l2"]), _typeset=w_ref.typeset)

Controller.from_ltl(phi2)

print(phi2 <= phi1)

print(phi1)
print(OrderedPatrolling(["lb", "lv"]))
print(phi2)
print(OrderedPatrolling(["b2", "l2"]))
