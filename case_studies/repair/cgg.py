from case_studies.repair.goals import goals
from case_studies.repair.world import world
from crome_cgg.cgg import Cgg, Link
from crome_cgg.goal import Goal
from crome_cgg.library import Library
from crome_contracts.contract import Contract
from crome_logic.patterns.robotic_movement import Patrolling
from crome_logic.specification.temporal import LTL

w = world

cgg = Cgg(goals)

print(cgg)

l1 = Goal(
    id="patrol_l1_l2",
    description="Keep visiting l1 and l2",
    contract=Contract(LTL(Patrolling(["l1", "l2"]), w.typeset)),
    world=w,
)

l2 = Goal(
    id="patrol_l1_l2_l3_l4",
    description="Keep visiting l1 and l2",
    contract=Contract(LTL(Patrolling(["l1", "l2", "l3", "l4"]), w.typeset)),
    world=w,
)


library = Library({l1, l2})

leaves = cgg.leaves

candidate_goals = set()
for goal in leaves:
    if library.covers(goal):
        candidate_goals.add(goal)
print(
    f"Candidate goals which are covered by the library:\n{[g.id for g in list(candidate_goals)]}"
)


refined_goals = set()

for goal in leaves:
    refinement = library.search_refinement(goal)
    if refinement is not None:
        print(f"{refinement.id}\trefines\t{goal.id}")
        """We attach the refinement to the existing goal"""
        cgg.add_edge(goal, refinement, Link.refinement)
        refined_goals.add(goal)

print(
    f"There are still {len(candidate_goals - refined_goals)} goals that are covered by the library "
    f"but are have no refinement"
)




