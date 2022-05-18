from __future__ import annotations

import itertools
from collections import Counter
from dataclasses import dataclass
from functools import reduce

from crome_cgg.goal import Goal
from crome_cgg.goal.operations.composition import g_composition
from crome_logic.typeset import Typeset


@dataclass
class Library:

    def __init__(self, goals: set[Goal] | None):
        if goals is None:
            self._goals = set()
        else:
            self._goals: set[Goal] = goals

        self._typeset = Typeset()

        for goal in self.goals:
            self._typeset += goal.contract.typeset

    @property
    def goals(self) -> set[Goal]:
        return self._goals

    @property
    def typeset(self) -> Typeset:
        return self._typeset

    def add_goals(self, goals: set[Goal]):
        self._goals |= goals
        for goal in goals:
            self._typeset |= goal.contract.typeset

    def get_candidate_composition(self, goal_to_refine: Goal):

        candidates = Counter()
        best_similar_types = 0

        for n in range(1, len(self.goals)):
            for subset in itertools.combinations(self.goals, n):
                n_compositions = len(subset)
                if n_compositions == 1:
                    subset_typeset = subset[0].specification.typeset
                else:
                    subset_typeset = reduce(
                        (lambda x, y: x | y), [g.specification.typeset for g in subset]
                    )
                similar_types = self.covers(goal_to_refine, subset_typeset)[1]
                if similar_types > best_similar_types:
                    candidates = Counter()
                    best_similar_types = similar_types
                elif similar_types == best_similar_types:
                    candidates[g_composition(subset)] = n_compositions

        print(
            f"There are {len(candidates.keys())} candidates with the same number of similar types: {best_similar_types}"
        )

        for node, count in candidates.items():
            print(f"{node.name}: {count}")

        # Filtering candidates with too many goals composed
        new_candidates = [
            x for x, count in candidates.items() if count == min(candidates.values())
        ]

        print("filtering...")
        print("\n".join(e.name for e in new_candidates))

        winner = self.get_most_refined(new_candidates)
        print(f"{winner.id} is the most refined candidate")
        return winner

    def get_most_refined(self, goals: list[Goal]) -> Goal:

        scores = Counter()

        for a, b in itertools.permutations(goals, 2):
            if a <= b:
                scores[a] += 1

        print("ratings")
        for node, count in scores.items():
            print(f"{node.name}: {count}")

        return scores.most_common(1)[0][0]

    def search_refinement(self, goal_to_refine: Goal) -> Goal | None:
        """Finds a composition of goals that refine 'goal_to_refine'.

        MOCK UP OF GREEDY ALGORITHM IN COGOMO, TODO: integrate here
        """

        print(f"Searching refinements for {goal_to_refine.id}")

        for n in range(1, len(self.goals)):
            for subset in itertools.combinations(self.goals, n):
                if len(subset) == 1:
                    subset_typeset = subset[0].contract.typeset
                else:
                    subset_typeset = reduce(
                        (lambda x, y: x | y), [g.contract.typeset for g in subset]
                    )
                if not self.covers(goal_to_refine, subset_typeset)[0]:
                    continue
                g = g_composition(subset)
                print(f"Composition:\n{g}")
                if g.contract <= goal_to_refine.contract:
                    return g

        return None

    def covers(self, goal: Goal, typeset: Typeset = None) -> (bool, int):
        """Return true if all the types of the goal are covered by the same
        type or refinements.

        It also returns the number of similar types
        """
        if typeset is None:
            typeset = self._typeset
        n_t_covered = 0
        for t_goal in goal.contract.typeset.values():
            t_covered = False
            for t_lib in typeset.values():
                if t_lib <= t_goal:
                    t_covered = True
                    continue
            if not t_covered:
                return False, n_t_covered
            else:
                n_t_covered += 1

        if n_t_covered == goal.contract.typeset.size:
            return True, n_t_covered
        return False, n_t_covered
