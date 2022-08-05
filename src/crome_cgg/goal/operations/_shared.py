from enum import Enum, auto

from crome_cgg.src.crome_cgg.goal import Goal
from crome_synthesis.src.crome_synthesis.world import World


class GoalOperation(Enum):
    Composition = auto()
    Conjunction = auto()
    Refinement = auto()
    Merging = auto()
    Quotient = auto()
    Separation = auto()


def generate_goal_operations_name_description(
    goals: list[Goal], operation: GoalOperation
) -> tuple[str, str]:
    goals_names = ", ".join(list(map(lambda g: g.id, goals)))

    if operation == GoalOperation.Composition:
        name = "||".join(list(map(lambda g: g.id, goals)))

    elif operation == GoalOperation.Conjunction:
        name = "/\\".join(list(map(lambda g: g.id, goals)))

    elif operation == GoalOperation.Merging:
        name = "**".join(list(map(lambda g: g.id, goals)))

    elif operation == GoalOperation.Quotient:
        name = "//".join(list(map(lambda g: g.id, goals)))

    elif operation == GoalOperation.Separation:
        name = "::".join(list(map(lambda g: g.id, goals)))

    elif operation == GoalOperation.Refinement:
        name = "->".join(list(map(lambda g: g.id, goals)))

    else:
        raise Exception("Operation not recognized")

    description = f"{operation.name} among {goals_names}"

    return name, description


def generate_shared_world(goals: set[Goal]) -> World:
    first_goal: Goal = next(iter(goals))
    new_world = first_goal.world
    for goal in goals - {first_goal}:
        new_world += goal.world
    return new_world
