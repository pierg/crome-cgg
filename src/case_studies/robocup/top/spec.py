
from crome_cgg.src.case_studies.robocup.world.world_top import w_top
from crome_cgg.src.crome_cgg.goal import Goal
from crome_contracts.src.crome_contracts.contract import Contract
from crome_logic.src.crome_logic.patterns.basic import *
from crome_logic.src.crome_logic.patterns.robotic_movement import *
from crome_logic.src.crome_logic.patterns.robotic_triggers import *
from crome_logic.src.crome_logic.specification.temporal import LTL



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
            _guarantees=LTL(InstantaneousReaction(pre="lg & oj", post="dp"), _typeset=w_top.typeset)
        ),
        world=w_top
    ),
    Goal(
        id="remove",
        description="remove all the objects continuously",
        contract=Contract(
            _guarantees=LTL(InfOft("!ob"), _typeset=w_top.typeset)
        ),
        world=w_top
    )
}