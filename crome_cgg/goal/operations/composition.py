from crome_contracts.contract.exceptions import ContractException
from crome_contracts.operations.composition import composition

from crome_cgg.context import group_conjunction
from crome_cgg.goal import Goal
from crome_cgg.goal.exceptions import GoalAlgebraOperationFail, GoalFailOperations
from crome_cgg.goal.operations._shared import (
    GoalOperation,
    generate_goal_operations_name_description,
    generate_shared_world,
)


def g_composition(goals: set[Goal]) -> Goal:
    if len(goals) == 1:
        return next(iter(goals))
    if len(goals) == 0:
        raise Exception("No goal specified in the composition")

    world = generate_shared_world(goals)

    name, description = generate_goal_operations_name_description(
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
        name=name,
        description=description,
        context=context,
        world=world,
    )

    return goal
