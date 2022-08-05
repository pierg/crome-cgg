from crome_synthesis.src.crome_synthesis.rule import Rule
from crome_synthesis.src.crome_synthesis.world import World
from crome_logic.src.crome_logic.specification.temporal import LTL

from crome_logic.src.crome_logic.typelement.robotic import BooleanLocation, BooleanAction, BooleanSensor
from crome_logic.src.crome_logic.typeset import Typeset

w_top = World(
    project_name="top",
    typeset=Typeset(
        {
            BooleanLocation(
                name="lb", mutex_group="toplocs", adjacency_set={"lv"}
            ),
            BooleanLocation(
                name="le", mutex_group="toplocs", adjacency_set={"lh"}
            ),
            BooleanLocation(
                name="lh", mutex_group="toplocs", adjacency_set={"le", "lv"}
            ),
            BooleanLocation(
                name="lv", mutex_group="toplocs", adjacency_set={"lb", "lh", "lr", "lk"}
            ),
            BooleanLocation(
                name="lr", mutex_group="toplocs", adjacency_set={"lv"}
            ),
            BooleanLocation(
                name="lk", mutex_group="toplocs", adjacency_set={"lg"}
            ),
            BooleanLocation(
                name="lg", mutex_group="toplocs", adjacency_set={"lk"}
            ),
            BooleanSensor(
                name="oj", description="object detected"
            ),
            BooleanAction(
                name="hl", description="hold an object"
            ),
            BooleanAction(
                name="dp", description="drop an object in the current location", mutex_group="actions"
            ),
        }
    ))



"""System Rules"""
w_top.system_rules = {
    Rule(
        description="If you drop next, then you must hold",
        specification=LTL("G(X dp -> hl)", _typeset=w_top.typeset)
    ),
    Rule(
        description="If you not hold next, then you must drop",
        specification=LTL("G(X ! hl -> dp)", _typeset=w_top.typeset)
    )
}

"""Environment Rules"""
w_top.environment_rules = {
    # Rule(
    #     description="Objects disappears if gets dropped",
    #     specification=LTL("G(!oj -> dp)", _typeset=w_top.typeset)
    # ),
    Rule(
        description="Show objects randomly",
        specification=LTL("GF(oj) & GF(!oj)", _typeset=w_top.typeset)
    )
}
