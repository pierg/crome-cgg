from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from crome_contracts.contract.exceptions import ContractException
from crome_synthesis.controller.exceptions import ControllerException

from crome_cgg.goal import Goal


class GoalFailOperations(Enum):
    composition = 0
    conjunction = 1
    refinement = 2
    synthesis = 3
    merging = 4
    quotient = 5
    separation = 6


class GoalFailMotivations(Enum):
    goal_not_found = 0
    inconsistent = 1
    incompatible = 2
    unfeasible = 3
    wrong_refinement = 4


@dataclass
class GoalException(Exception):
    message: str

    def __post_init__(self):
        header = "*** GOAL EXCEPTION ***"
        print(f"{header}\n{self.message}")


@dataclass
class GoalAlgebraOperationFail(GoalException):
    goals: set[Goal]
    operation: GoalFailOperations
    contr_ex: ContractException

    def __post_init__(self):
        message = (
            f"A failure has occurred while performing '{self.operation.name}' on goals:\n"
            f"{', '.join(g.name for g in self.goals)}"
        )
        super().__init__(message)


@dataclass
class GoalSharedWorldFail(GoalException):
    goals: set[Goal]

    def __post_init__(self):
        message = "The goals involved in the operation have different world variables"
        super().__init__(message)


@dataclass
class GoalSynthesisFail(GoalException):
    goal: Goal
    controller_ex: ControllerException

    def __post_init__(self):
        message = f"A failure has occurred while performing trying to realize the goal '{self.goal.name}'"
        super().__init__(message)
