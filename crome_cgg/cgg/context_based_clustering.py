import itertools
from copy import deepcopy

from crome_cgg.cgg import Cgg
from crome_cgg.context import Context
from crome_cgg.goal import Goal
from crome_cgg.goal.operations.composition import g_composition
from crome_cgg.goal.operations.conjunction import g_conjunction
from crome_cgg.goal.operations.merging import g_merging


def context_based_goal_clustering(init_goals: set[Goal], cgg: Cgg):
    contexts: set[Context] = {
        g.context for g in filter(lambda g: not g.context.is_valid, init_goals)
    }

    """Extract all combinations of context which are consistent"""
    saturated_combinations = []
    for i in range(0, len(contexts)):
        """Extract all combinations of i context and saturate it."""
        combinations = itertools.combinations(contexts, (i + 1) % (len(contexts)))
        for combination in combinations:
            if len(combination) == 0:
                continue
            saturated_combination = deepcopy(combination[0])
            for element in combination[1:]:
                saturated_combination &= element
            for context in contexts:
                if context not in combination:
                    saturated_combination &= ~context
            if not saturated_combination.is_satisfiable:
                continue
            else:
                saturated_combinations.append(saturated_combination)

    """Group combinations"""
    saturated_combinations_grouped = list(saturated_combinations)
    for c_a in saturated_combinations:
        for c_b in saturated_combinations:
            if (
                    c_a is not c_b
                    and c_a <= c_b
                    and c_b in saturated_combinations_grouped
            ):
                saturated_combinations_grouped.remove(c_b)

    print(
        "\nCONTEXT MUTEX:\t"
        + ",\t".join(str(x) for x in saturated_combinations)
        + "\n"
    )

    """Map to goals"""
    mapped_goals = set()
    context_goal_map: dict[Context, dict[str, set[Goal]]] = {}
    for goal in init_goals:
        for combination in saturated_combinations_grouped:
            add_goal = False
            if goal.context is not None:
                if combination <= goal.context:
                    add_goal = True
            else:
                add_goal = True
            if add_goal:
                if combination in context_goal_map:
                    if goal.viewpoint in context_goal_map[combination]:
                        context_goal_map[combination][goal.viewpoint].add(goal)
                    else:
                        context_goal_map[combination][goal.viewpoint] = {goal}
                else:
                    context_goal_map[combination] = {}
                    context_goal_map[combination][goal.viewpoint] = {goal}
                mapped_goals.add(goal)

    if mapped_goals != init_goals:
        raise Exception("Not all goals have been mapped!")
    print("All goals have been mapped to mutually exclusive context")

    """Building the cgg..."""
    merged_goals = set()
    for mutex_context, cluster in context_goal_map.items():
        composed_goals = set()
        for viewpoint, goals in cluster.items():
            new_goal = g_composition(cluster[viewpoint], cgg=cgg)
            new_goal.context = mutex_context
            composed_goals.add(new_goal)
        new_goal = g_merging(composed_goals, cgg=cgg)
        new_goal.context = mutex_context
        merged_goals.add(new_goal)

    g_conjunction(merged_goals, cgg=cgg)

    cgg.draw()