from crome_logic.specification import and_, or_
from crome_logic.specification.temporal import LTL
from crome_logic.typeset import Typeset


class Context(LTL):
    pass


def group_conjunction(elements: set[Context]) -> Context:
    typeset = Typeset.from_typesets([c.typeset for c in elements])
    formula = and_([c.formula for c in elements])

    return Context(_init_formula=formula, _typeset=typeset)


def group_disjunction(elements: set[Context]) -> Context:
    typeset = Typeset.from_typesets([c.typeset for c in elements])
    formula = or_([c.formula for c in elements])

    return Context(_init_formula=formula, _typeset=typeset)
