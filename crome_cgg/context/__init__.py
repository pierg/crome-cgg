from __future__ import annotations
from crome_logic.specification import and_, or_
from crome_logic.specification.temporal import LTL
from crome_logic.typeset import Typeset
from dataclasses import dataclass


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


@dataclass(kw_only=True)
class ContextException(Exception):

    def __init__(self, contexts: set[Context]):
        contexts_str = "\n\t".join(repr(c) for c in contexts)
        self.message = "*** ContextException EXCEPTION ***\n" + f"A failure has occurred on contexts, their are not " \
                                                           f"compatible:\n\t{contexts_str} "
        super().__init__(self.message)
