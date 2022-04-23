# type: ignore
import os

import dill as dill
from crome_synthesis.controller import Controller

from crome_cgg.cgg import Cgg
from crome_cgg.goal import Goal
from crome_cgg.shared.paths import persistence_path
from crome_cgg.world import World


def _make_path(folder_name: str = ""):
    if not os.path.exists(persistence_path / folder_name):
        os.makedirs(persistence_path / folder_name)


def dump_cgg(cgg: Cgg, folder_name: str = ""):
    _make_path(folder_name)

    with open(persistence_path / folder_name / "cgg.dat", "wb") as stream:
        dill.dump(cgg, stream)


def load_cgg(folder_name: str = "") -> Cgg | None:
    if not os.path.exists(persistence_path / folder_name / "cgg.dat"):
        return None

    with open(persistence_path / folder_name / "cgg.dat", "rb") as stream:
        cgg = dill.load(stream)
    return cgg


def dump_world(world: World, folder_name: str = ""):
    _make_path(folder_name)

    with open(persistence_path / folder_name / "world.dat", "wb") as stream:
        dill.dump(world, stream)


def load_world(folder_name: str = "") -> World | None:
    if not os.path.exists(persistence_path / folder_name / "world.dat"):
        return None

    with open(persistence_path / folder_name / "world.dat", "rb") as stream:
        world = dill.load(stream)
    return world


def dump_goals(goals: set[Goal], folder_name: str = ""):
    _make_path(folder_name)

    with open(persistence_path / folder_name / "goals.dat", "wb") as stream:
        dill.dump(goals, stream)


def load_goals(folder_name: str = "") -> set[Goal] | None:
    if not os.path.exists(persistence_path / folder_name / "goals.dat"):
        return None

    with open(persistence_path / folder_name / "goals.dat", "rb") as stream:
        goals = dill.load(stream)
    return goals


def dump_controller(controller: Controller, folder_name: str = ""):
    _make_path(folder_name)

    with open(persistence_path / folder_name / "controller.dat", "wb") as stream:
        dill.dump(controller, stream)


def load_controller(folder_name: str = "") -> Controller | None:
    if not os.path.exists(persistence_path / folder_name / "controller.dat"):
        return None
    with open(persistence_path / folder_name / "controller.dat", "rb") as stream:
        controller = dill.load(stream)
    return controller
