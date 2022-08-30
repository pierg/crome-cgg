from crome_synthesis.src.crome_synthesis.world import World

from crome_cgg.case_studies.minimal.world.world_top import w_top
from crome_logic.typelement.robotic import BooleanLocation
from crome_logic.typeset import Typeset

w_ref = World(
    project_name="ref",
    typeset=Typeset(
        {
            BooleanLocation(
                name="a1",
                mutex_group="locations",
                adjacency_set={"a2", "b1"},
                refinement_of={w_top.typeset["a"]},
            ),
            BooleanLocation(
                name="a2",
                mutex_group="locations",
                adjacency_set={"a1", "b2"},
                refinement_of={w_top.typeset["a"]},
            ),
            BooleanLocation(
                name="b1",
                mutex_group="locations",
                adjacency_set={"b2", "a1"},
                refinement_of={w_top.typeset["b"]},
            ),
            BooleanLocation(
                name="b2",
                mutex_group="locations",
                adjacency_set={"b1", "a2"},
                refinement_of={w_top.typeset["b"]},
            ),
        }
    ),
)
