from __future__ import annotations

from dataclasses import dataclass, field

from crome_logic.specification import Specification


@dataclass
class Rule:
    specification: Specification
    name: str = field(default="")
    description: str = field(default="")

    def __hash__(self):
        return hash(self.name + str(self.specification))
