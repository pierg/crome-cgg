from crome_cgg.case_studies.repair.world import world
from crome_cgg.cgg import Cgg
from crome_contracts.contract import Contract
from crome_cgg.goal import Goal
from crome_logic.patterns.basic import GF
from crome_logic.patterns.robotic_movement import Patrolling, StrictOrderedPatrolling
from crome_logic.patterns.robotic_triggers import BoundReaction, PromptReaction
from crome_logic.specification.temporal import LTL

w = world

goals = {
    # Goal(
    #     id="day_patrolling",
    #     description="During the day keep visiting the `front' locations",
    #     contract=Contract(_guarantees=LTL(Patrolling(["lf"]), w.typeset)),
    #     world=w,
    # ),
    Goal(
        id="wave",
        description="Always, immediately wave only when seeing a person",
        contract=Contract(
            _assumptions=LTL(GF("ps"), w.typeset),
            _guarantees=LTL(BoundReaction("ps", "wa"), w.typeset),
        ),
        world=w,
    ),
    # Goal(
    #     id="front_patrolling_abs",
    #     description="Patrol front location in strict order",
    #     contract=Contract(_guarantees=LTL(StrictOrderedPatrolling(["lf"]), w.typeset)),
    #     world=w,
    # ),
    Goal(
        id="front_patrolling_impl",
        description="Patrol front location in strict order",
        contract=Contract(
            _guarantees=LTL(
                StrictOrderedPatrolling(["l1", "l2", "l4", "l3"]), w.typeset
            )
        ),
        world=w,
    ),
    # Goal(
    #     id="visit_back_abs",
    #     description="Patrol back location",
    #     contract=Contract(_guarantees=LTL(Patrolling(["lb"]), w.typeset)),
    #     world=w,
    # ),
    Goal(
        id="visit_back_impl",
        description="Patrol back location",
        contract=Contract(_guarantees=LTL(Patrolling(["l5"]), w.typeset)),
        world=w,
    ),
    # Goal(
    #     id="charge_abs",
    #     description="Charge battery when in the front",
    #     contract=Contract(_assumptions=LTL(GF("lc"), w.typeset),
    #                       _guarantees=LTL(PromptReaction("lf", "lc & ch"), w.typeset)),
    #     world=w,
    # ),
    Goal(
        id="charge_impl",
        description="Charge battery when in the front",
        contract=Contract(
            _assumptions=LTL(GF("lc"), w.typeset),
            _guarantees=LTL(PromptReaction("l2", "l2 & ch"), w.typeset),
        ),
        world=w,
    ),
}

for g in goals:
    print(g)

cgg = Cgg(goals)

cgg.root.realize()
cgg.root.controller.save(format="pdf")

if cgg.root.controller is not None:
    print(str(cgg.root.controller.mealy))
