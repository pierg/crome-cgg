from __future__ import annotations

from dataclasses import dataclass

from crome_cgg.src.crome_cgg.goal import Goal


@dataclass(kw_only=True)
class CggException(Exception):
    message: str

    def __post_init__(self):
        self.message += f"*** CggException EXCEPTION ***\n"
        print(self.message)


@dataclass(kw_only=True)
class GoalAlreadyPresent(CggException):
    goal: Goal
    message: str = "*** GoalAlreadyPresent EXCEPTION ***\n"

    def __post_init__(self):
        self.message += f"The goal '{self.goal.id}' is already present in the graph"
