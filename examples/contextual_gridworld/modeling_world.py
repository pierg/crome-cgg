from crome_logic.typeelement.robotic import (
    BooleanAction,
    BooleanContext,
    BooleanLocation,
    BooleanSensor,
)
from crome_logic.typeset import Typeset

from crome_cgg.world import World
from examples.contextual_gridworld import project_name

gridworld = World(
    project_name=project_name,
    typeset=Typeset(
        {
            BooleanAction(name="greet"),
            BooleanAction(name="register"),
            BooleanLocation(
                name="r1", mutex_group="locations", adjacency_set={"r2", "r5"}
            ),
            BooleanLocation(
                name="r2", mutex_group="locations", adjacency_set={"r1", "r5"}
            ),
            BooleanLocation(
                name="r3", mutex_group="locations", adjacency_set={"r4", "r5"}
            ),
            BooleanLocation(
                name="r4", mutex_group="locations", adjacency_set={"r3", "r5"}
            ),
            BooleanLocation(
                name="r5",
                mutex_group="locations",
                adjacency_set={"r1", "r2", "r3", "r4"},
            ),
            BooleanSensor(name="person"),
            BooleanContext(name="day", mutex_group="time"),
            BooleanContext(name="night", mutex_group="time"),
        }
    ),
)
