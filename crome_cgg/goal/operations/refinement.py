from crome_cgg.contract.exceptions import ContractException

from crome_cgg.cgg import Cgg, Link

from crome_cgg.goal import Goal
from crome_cgg.goal.exceptions import GoalAlgebraOperationFail, GoalFailOperations


def g_refinement(goal_b: Goal, goal_t: Goal, cgg: Cgg | None = None) -> Cgg:
    if not(isinstance(goal_b, Goal) and isinstance(goal_t, Goal)):
        raise Exception("Two goals must be provided")

    try:
        goal_b.contract <= goal_t.contract

    except ContractException as e:

        raise GoalAlgebraOperationFail(
            goals={goal_b, goal_t}, operation=GoalFailOperations.refinement, contr_ex=e
        )

    if cgg is None:
        cgg = Cgg(init_goals={goal_b, goal_t})

    cgg.add_edge(goal_b, goal_t, Link.refinement)

    return cgg
