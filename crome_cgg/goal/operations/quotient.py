from crome_contracts.contract.exceptions import ContractException
from crome_contracts.operations.quotient import quotient

from crome_cgg.context import group_conjunction
from crome_cgg.goal import Goal
from crome_cgg.goal.exceptions import GoalAlgebraOperationFail, GoalFailOperations
from crome_cgg.goal.operations._shared import (
    GoalOperation,
    generate_goal_operations_name_description,
    generate_shared_world,
)


def g_quotient(dividend: Goal, divisor: Goal) -> Goal:
    if dividend is None:
        raise Exception("No dividend specified in the quotient")
    if divisor is None:
        raise Exception("No divisor specified in the quotient")

    world = generate_shared_world({dividend, divisor})

    name, description = generate_goal_operations_name_description(
        [dividend, divisor], GoalOperation.Quotient
    )

    context = group_conjunction(set(map(lambda g: g.context, {dividend, divisor})))

    try:
        contract = quotient(dividend.contract, divisor.contract)

    except ContractException as e:

        raise GoalAlgebraOperationFail(
            goals={dividend, divisor}, operation=GoalFailOperations.quotient, contr_ex=e
        )

    goal = Goal(
        contract=contract,
        name=name,
        description=description,
        context=context,
        world=world,
    )

    return goal
