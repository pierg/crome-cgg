from __future__ import annotations

import uuid
from copy import copy
from dataclasses import dataclass

from crome_logic.specification.temporal import LTL
from crome_logic.typeset import Typeset
from crome_logic.typesimple import CromeType
from crome_logic.typesimple.subtype.robotic.action import BooleanAction
from crome_logic.typesimple.subtype.robotic.context import ContextType
from crome_logic.typesimple.subtype.robotic.location import Location
from crome_logic.typesimple.subtype.robotic.sensor import BooleanSensor


@dataclass
class World(dict):
    typeset: Typeset
    project_name: str = str(uuid.uuid4())

    def __attrs_post_init__(self):
        self._generate_atoms()

    def _generate_atoms(self) -> None:
        for crome_type in self.typeset.values():
            self._add_atom(crome_type)

    def _add_atom(self, crome_type: CromeType):
        atom = LTL(crome_type.name)
        super().__setitem__(crome_type.name, atom)
        super().__setitem__(f"!{crome_type.name}", ~atom)

    def add_type(self, crome_type: CromeType):
        self.typeset += crome_type
        self._add_atom(crome_type)

    def new_boolean_action(self, name: str, mutex: str = ""):
        crome_type = BooleanAction(name, mutex)
        self.add_type(crome_type)

    def new_boolean_sensor(self, name, mutex: str = ""):
        crome_type = BooleanSensor(name, mutex)
        self.add_type(crome_type)

    def new_boolean_location(
        self, name, mutex: str = "", adjacency: set[str] | None = None
    ):
        crome_type = Location(name, mutex, adjacency)
        self.add_type(crome_type)

    def new_boolean_context(self, name, mutex: str = ""):
        crome_type = ContextType(name, mutex)
        self.add_type(crome_type)

    def adjacent_types(self, location: Location) -> set[Location]:

        adjacent_types = set()
        for class_name in location.adjacency_set:
            for t in self.typeset.values():
                if type(t).__name__ == class_name:
                    adjacent_types.add(t)

        return adjacent_types

    def __iadd__(self, element: World) -> World:
        """Updates self with self += element."""
        self.typeset += element.typeset
        self._generate_atoms()
        return self
