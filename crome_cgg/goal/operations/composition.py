from crome_cgg.contract.exceptions import ContractException
from crome_cgg.operations.composition import composition

from crome_cgg.cgg import Cgg, Link
from crome_cgg.context import group_conjunction
from crome_cgg.goal import Goal
from crome_cgg.goal.exceptions import GoalAlgebraOperationFail, GoalFailOperations
from crome_cgg.goal.operations._shared import (
    GoalOperation,
    generate_goal_operations_name_description,
    generate_shared_world,
)


def g_composition(goals: set[Goal], cgg: Cgg | None = None) -> Goal:
    if len(goals) == 1:
        goal = next(iter(goals))
        if cgg is not None:
            cgg.add_node(goal=goal)
        return goal
    if len(goals) == 0:
        raise Exception("No goal specified in the composition")

    world = generate_shared_world(goals)

    id, description = generate_goal_operations_name_description(
        list(goals), GoalOperation.Composition
    )

    context = group_conjunction(set(map(lambda g: g.context, goals)))

    try:
        contract = composition(set(map(lambda g: g.contract, goals)))

    except ContractException as e:

        raise GoalAlgebraOperationFail(
            goals=goals, operation=GoalFailOperations.composition, contr_ex=e
        )

    goal = Goal(
        contract=contract,
        id=id,
        description=description,
        context=context,
        world=world,
    )

    goals_ids = ", ".join(g.id for g in goals)
    print(f"{goal.id} -- composition of -- {goals_ids}")
    # Fix Cgg
    if cgg is not None:
        for g in goals:
            cgg.add_edge(node_a=g, node_b=goal, link=Link.composition)

    return goal
