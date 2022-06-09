from __future__ import annotations

import uuid
from copy import copy
from dataclasses import dataclass, field

from crome_cgg.context import Context
from crome_cgg.rule import Rule
from crome_logic.specification.temporal import LTL
from crome_logic.typelement import CromeType, TypeKind
from crome_logic.typelement.robotic import (
    BooleanAction,
    BooleanContext,
    BooleanLocation,
    BooleanSensor,
)
from crome_logic.typeset import Typeset


@dataclass
class World(dict):
    project_name: str = str(uuid.uuid4())
    typeset: Typeset = field(default_factory=lambda: Typeset())
    environment_rules: set[Rule] = field(default_factory=set)
    system_rules: set[Rule] = field(default_factory=set)

    def __post_init__(self):
        self._generate_atoms()

    def _generate_atoms(self) -> None:
        for crome_type in self.typeset.values():
            self._add_atom(crome_type)

    def _add_atom(self, crome_type: CromeType):
        if crome_type.kind == TypeKind.CONTEXT:
            atom = Context(crome_type.name)
        else:
            atom = LTL(crome_type.name)
        super().__setitem__(crome_type.name, atom)
        super().__setitem__(f"!{crome_type.name}", ~atom)

    def add_type(self, crome_type: CromeType):
        self.typeset += crome_type
        self._add_atom(crome_type)

    def new_boolean_action(self, name: str, mutex: str = "") -> None:
        crome_type = BooleanAction(name=name, mutex_group=mutex)
        self.add_type(crome_type)

    def new_boolean_sensor(self, name: str, mutex: str = "") -> None:
        crome_type = BooleanSensor(name=name, mutex_group=mutex)
        self.add_type(crome_type)

    def new_boolean_location(
        self, name, mutex: str = "", adjacency: set[str] | None = None
    ) -> None:
        crome_type = BooleanLocation(name=name, mutex_group=mutex, adjacency_set=adjacency)
        self.add_type(crome_type)

    def new_boolean_context(self, name: str, mutex: str = "") -> None:
        crome_type = BooleanContext(name=name, mutex_group=mutex)
        self.add_type(crome_type)

    def get_rules(self, environment: bool, typeset: Typeset | None = None) -> tuple[list[tuple[str, str]], Typeset]:
        if typeset is None:
            typeset = self.typeset
        new_typeset: Typeset = Typeset()
        rules: list[tuple[str, str]] = []
        if environment:
            rules_list = self.environment_rules
        else:
            rules_list = self.system_rules
        for r in rules_list:
            if r.specification.typeset.n_elements_in_common_with(typeset) > 0:
                if not r.specification.is_true_expression:
                    rules.append((str(r.specification), r.description))
                    new_typeset += r.specification.typeset
        return rules, new_typeset


    def __add__(self, element: World) -> World:
        """Generate a shallow new World self + element."""
        world = copy(self)
        world += element
        return world

    def __iadd__(self, element: World) -> World:
        """Updates self with self += element."""
        self.typeset += element.typeset
        self._generate_atoms()
        return self

    def __reduce__(self):
        return self.__class__, (
            self.project_name,
            self.typeset,
        )
