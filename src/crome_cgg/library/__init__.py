from __future__ import annotations

import itertools
from collections import Counter
from dataclasses import dataclass
from functools import reduce

from src.crome_cgg.goal import Goal
from src.crome_cgg.goal.operations.composition import g_composition
from src.crome_logic.typeset import Typeset


@dataclass
class Library:
    goals: set[Goal]

    @property
    def typeset(self) -> Typeset:
        typeset = Typeset()
        for goal in self.goals:
            typeset += goal.contract.typeset
        return typeset

    def get_candidate_composition(self, goal_to_refine: Goal):

        candidates = Counter()
        best_similarity_score = 0

        for n in range(1, len(self.goals)):
            for subset in itertools.combinations(self.goals, n):
                n_compositions = len(subset)
                if n_compositions == 1:
                    subset_typeset = subset[0].contract.typeset
                else:
                    subset_typeset = reduce(
                        (lambda x, y: x + y), [g.contract.typeset for g in subset]
                    )
                similarity_score = subset_typeset.similarity_score(goal_to_refine.contract.typeset)
                print(similarity_score)
                if similarity_score > best_similarity_score:
                    candidates = Counter()
                    best_similarity_score = similarity_score
                elif similarity_score == best_similarity_score:
                    candidates[g_composition(set(subset))] = n_compositions

        print(
            f"There are {len(candidates.keys())} candidates with the same number of similar types: {best_similarity_score}"
        )

        for goal, count in candidates.items():
            print(f"{goal.id}: {count}")

        # Filtering candidates with too many goals composed
        new_candidates = [
            x for x, count in candidates.items() if count == min(candidates.values())
        ]

        print("filtering...")
        print("\n".join(e.id for e in new_candidates))

        winner = self.get_most_refined(new_candidates)
        print(f"{winner.id} is the most refined candidate")
        return winner

    def get_most_refined(self, goals: list[Goal]) -> Goal:

        if len(goals) == 1:
            return goals[0]

        scores = Counter()

        for g in goals:
            scores[g] = 0
        for a, b in itertools.permutations(goals, 2):
            if a <= b:
                scores[a] += 1

        for goal, count in scores.items():
            scores[goal] = count/len(goals) * 100

        print("ratings")
        for goal, count in scores.items():
            print(f"{goal.id}: {count}")

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

    def covers(self, goal: Goal) -> float:
        """Returns the percentage of "coverage" of the library to 'goal'. I.e. the ratio of how many types are similar
        """
        return self.typeset.similarity_score(goal.contract.typeset)

