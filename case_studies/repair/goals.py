from case_studies.repair.world import world
from crome_cgg.cgg import Cgg
from crome_cgg.goal import Goal
from crome_contracts.contract import Contract
from crome_logic.patterns.basic import GF
from crome_logic.patterns.robotic_movement import StrictOrderedPatrolling, Patrolling, OrderedPatrolling
from crome_logic.patterns.robotic_triggers import BoundReaction, PromptReaction, InstantaneousReaction
from crome_logic.specification.temporal import LTL
from crome_synthesis.controller import Controller

w = world

goals = {
    # Goal(
    #     id="day_patrolling",
    #     description="During the day keep visiting the `front' locations",
    #     contract=Contract(_guarantees=LTL(Patrolling(["lf"]), w.typeset)),
    #     world=w,
    # ),
    Goal(
        id="always_wave",
        description="Always, immediately wave only when seeing a person",
        contract=Contract(_assumptions=LTL(GF("ps"), w.typeset),
                          _guarantees=LTL(BoundReaction("ps", "wa"), w.typeset)),
        world=w,
    ),
    Goal(
        id="night_patrolling",
        description="During the patrol locations in order",
        contract=Contract(_guarantees=LTL(OrderedPatrolling(["l1", "l3", "l5"]), w.typeset)),
        world=w,
    ),
    Goal(
        id="night_visit",
        description="During the night keep visiting the charging location",
        contract=Contract(_guarantees=LTL(Patrolling(["lc"]), w.typeset)),
        world=w,
    ),
    Goal(
        id="night_report",
        description="During the night promptly send a report when in the 'back' location",
        contract=Contract(_assumptions=LTL(GF("lb"), w.typeset),
                          _guarantees=LTL(PromptReaction("lb", "re"), w.typeset)),
        world=w,
    ),
    Goal(
        id="night_charge",
        description="During the night, when in the store front, go promptly charging in the charging location",
        contract=Contract(_assumptions=LTL(GF("lc"), w.typeset),
                          _guarantees=LTL(PromptReaction("lf", "lc & ch"), w.typeset)),
        world=w,
    ),
    Goal(
        id="always_picture",
        description="Always take a picture when a person is detected",
        contract=Contract(_assumptions=LTL(GF("ps"), w.typeset),
                          _guarantees=LTL(InstantaneousReaction("ps", "pc"), w.typeset)),
        world=w,
    ),
}


for g in goals:
    print(g)


cgg = Cgg(goals)

print(cgg.root.contract.assumptions)

print(cgg.root.contract.guarantees)

cgg.root.realize()
if cgg.root.controller is not None:
    print(str(cgg.root.controller.mealy))


