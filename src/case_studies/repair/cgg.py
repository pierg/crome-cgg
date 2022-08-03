from src.case_studies.repair.goals import goals
from src.case_studies.repair.world import world
from src.crome_cgg.cgg import Cgg, Link
from src.crome_cgg.goal import Goal
from src.crome_cgg.goal.operations.composition import g_composition
from src.crome_cgg.goal.operations.quotient import g_quotient
from src.crome_cgg.library import Library
from src.crome_contracts.contract import Contract
from src.crome_logic.patterns.robotic_movement import Patrolling
from src.crome_logic.specification.temporal import LTL

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

print(f"There are {len(refined_goals)} goals refined")

print(
    f"There are still {len(candidate_goals - refined_goals)} goals that are covered by the library "
    f"but are have no refinement"
)

candidate_goals = set()
for goal in leaves - refined_goals:
    if library.covers(goal):
        candidate_goals.add(goal)

print(
    f"Candidate goals which are covered by the library:\n{[g.id for g in list(candidate_goals)]}"
)
leaves_dict = cgg.leaves_dict


print(
    f"Library goal '{l2.id}' covers CGG leaf '{leaves_dict['night_patrolling'].id}'"
)
assert not l2 <= leaves_dict["night_patrolling"]

quotient = g_quotient(l2, leaves_dict["night_patrolling"])
print(f"The quotient is: \n'{quotient}'")

composition = g_composition({quotient, leaves_dict["night_patrolling"]})
print(f"Their composition is: \n'{composition}'")

assert composition <= leaves_dict["night_patrolling"]
print(
    f"Library goal '{l2.id}' composed with the quotient refines the CGG leaf '{leaves_dict['night_patrolling'].id}'"
)

print("Searching for refinements of the quotient...")
print("No refinement has been found...")

print(
    "Modifying existing goal of CGG such that the current library goal can refine it, using separation and merging"
)
