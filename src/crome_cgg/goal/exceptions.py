from __future__ import annotations

from dataclasses import dataclass
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


@dataclass(kw_only=True)
class GoalException(Exception):
    goals: set[Goal]
    message: str

    def __post_init__(self):
        self.message += (
            f"*** GoalException EXCEPTION ***\n"
            f"Goals involved in the failure:\n"
            f"{', '.join(g.id for g in self.goals)}"
        )
        print(self.message)


@dataclass(kw_only=True)
class GoalAlgebraOperationFail(GoalException):
    operation: GoalFailOperations
    contr_ex: ContractException
    message: str = "*** GoalAlgebraOperationFail EXCEPTION ***\n"

    def __post_init__(self):
        self.message += (
            f"A failure has occurred while performing '{self.operation.name}'"
        )


@dataclass(kw_only=True)
class GoalSharedWorldFail(GoalException):
    message: str = (
        "*** GoalSharedWorldFail EXCEPTION ***\n"
        "The goals have different world variables"
    )


@dataclass(kw_only=True)
class GoalSynthesisFail(GoalException):
    controller_ex: ControllerException
    message: str = (
        "*** GoalSynthesisFail EXCEPTION ***\n"
        "A failure has occurred while performing trying to realize the goal"
    )
