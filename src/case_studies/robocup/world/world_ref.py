from crome_cgg.src.case_studies.robocup.world.world_top import w_top
from crome_synthesis.src.crome_synthesis.world import World

from crome_logic.src.crome_logic.typelement.robotic import BooleanLocation, BooleanAction, BooleanSensor
from crome_logic.src.crome_logic.typeset import Typeset


w_ref = World(
    project_name="ref",
    typeset=Typeset(
        {
            BooleanLocation(
                name="l1", mutex_group="locations", adjacency_set={"l2", "l4"}, refinement_of={w_top.typeset["lv"]}
            ),
            BooleanLocation(
                name="l2", mutex_group="locations", adjacency_set={"l1", "l3", "l5", "h1", "b2"}, refinement_of={w_top.typeset["lv"]}
            ),
            BooleanLocation(
                name="l3", mutex_group="locations", adjacency_set={"l2", "l6", "k1", "h2"}, refinement_of={w_top.typeset["lv"]}
            ),
            BooleanLocation(
                name="l4", mutex_group="locations", adjacency_set={"l1", "l5"}, refinement_of={w_top.typeset["lv"]}
            ),
            BooleanLocation(
                name="l5", mutex_group="locations", adjacency_set={"l4", "l2", "l6"}, refinement_of={w_top.typeset["lv"]}
            ),
            BooleanLocation(
                name="l6", mutex_group="locations", adjacency_set={"l5", "l3"}, refinement_of={w_top.typeset["lv"]}
            ),
            BooleanLocation(
                name="b1", mutex_group="locations", adjacency_set={"b2", "b3"}, refinement_of={w_top.typeset["lb"]}
            ),
            BooleanLocation(
                name="b2", mutex_group="locations", adjacency_set={"b1", "b3", "l2"}, refinement_of={w_top.typeset["lb"]}
            ),
            BooleanLocation(
                name="b3", mutex_group="locations", adjacency_set={"b1", "b2"}, refinement_of={w_top.typeset["lb"]}
            ),
            BooleanLocation(
                name="h1", mutex_group="locations", adjacency_set={"l2", "h2"}, refinement_of={w_top.typeset["lh"]}
            ),
            BooleanLocation(
                name="h2", mutex_group="locations", adjacency_set={"h1", "l3", "e2"}, refinement_of={w_top.typeset["lb"]}
            ),
            BooleanLocation(
                name="e1", mutex_group="locations", adjacency_set={"e2"}, refinement_of={w_top.typeset["le"]}
            ),
            BooleanLocation(
                name="e2", mutex_group="locations", adjacency_set={"e1", "h2"}, refinement_of={w_top.typeset["le"]}
            ),
            BooleanLocation(
                name="r1", mutex_group="locations", adjacency_set={"l3", "r2"}, refinement_of={w_top.typeset["lr"]}
            ),
            BooleanLocation(
                name="r2", mutex_group="locations", adjacency_set={"r1"}, refinement_of={w_top.typeset["lr"]}
            ),
            BooleanLocation(
                name="k1", mutex_group="locations", adjacency_set={"l3", "k2", "k3"}, refinement_of={w_top.typeset["lk"]}
            ),
            BooleanLocation(
                name="k2", mutex_group="locations", adjacency_set={"k1", "k3"}, refinement_of={w_top.typeset["lk"]}
            ),
            BooleanLocation(
                name="k3", mutex_group="locations", adjacency_set={"k2", "k1"}, refinement_of={w_top.typeset["lg"]}
            ),
            BooleanAction(
                name="hl", description="hold an object"
            ),
            BooleanAction(
                name="dp", description="drop an object in the current location", mutex_group="actions"
            ),
            BooleanAction(
                name="pu", description="pickup the object in the current location", mutex_group="actions"
            ),
            BooleanSensor(
                name="oj", description="object detected in the current location"
            ),

        }
    ),
)