from crome_cgg.world import World
from crome_logic.typelement.robotic import (
    BooleanAction,
    BooleanContext,
    BooleanLocation,
    BooleanSensor,
)
from crome_logic.typeset import Typeset

project_name = "mission_repair"

# WORLD MODELING
world = World(
    project_name=project_name,
    typeset=Typeset(
        {
            BooleanAction(name="pc", description="picture"),
            BooleanAction(name="ch", description="charge"),
            BooleanAction(name="re", description="report"),
            BooleanAction(name="wa", description="wave"),
            BooleanLocation(name="lf",
                            description="front", mutex_group="abstract_locs", adjacency_set={"lb"}
                            ),
            BooleanLocation(name="lb",
                            description="back", mutex_group="abstract_locs", adjacency_set={"lf"}
                            ),
            BooleanLocation(
                name="l1", mutex_group="locations", adjacency_set={"l3", "l2"}, refinement_of={"lf"}
            ),
            BooleanLocation(
                name="l2", mutex_group="locations", adjacency_set={"l1", "l4"}, refinement_of={"lf"}
            ),
            BooleanLocation(
                name="l3", mutex_group="locations", adjacency_set={"l1", "l4", "l5"}, refinement_of={"lf"}
            ),
            BooleanLocation(
                name="l4", mutex_group="locations", adjacency_set={"l3", "l2"}, refinement_of={"lf"}
            ),
            BooleanLocation(
                name="l5", mutex_group="locations", adjacency_set={"l3"}, refinement_of={"lb"}
            ),
            BooleanLocation(
                name="lc", description="charge", adjacency_set={"r1", "r5"}, refinement_of={"l2"}
            ),
            BooleanSensor(name="ps", description="person"),
            BooleanContext(name="dy", description="day", mutex_group="time"),
            BooleanContext(name="nt", description="night", mutex_group="time"),
        }
    ),
)
