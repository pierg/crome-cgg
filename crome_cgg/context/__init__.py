from __future__ import annotations

from dataclasses import dataclass

from crome_logic.specification import and_, or_
from crome_logic.specification.temporal import LTL
from crome_logic.typeset import Typeset


class Context(LTL):
    pass


def group_conjunction(elements: set[Context]) -> Context:
    typeset = Typeset.from_typesets([c.typeset for c in elements])
    formula = and_([c.formula for c in elements])
    context = Context(_init_formula=formula, _typeset=typeset)

    return context


def group_disjunction(elements: set[Context]) -> Context:
    typeset = Typeset.from_typesets([c.typeset for c in elements])
    formula = or_([c.formula for c in elements])
    context = Context(_init_formula=formula, _typeset=typeset)

    return context


@dataclass(kw_only=True)
class ContextException(Exception):
    def __init__(self, contexts: set[Context] | Context, formula: str = None):
        if type(contexts) == Context:
            self.message = (
                "*** ContextException EXCEPTION ***\n"
                + f"A failure has occurred on context, it is not "
                f"satifaisable. The formula is : {contexts.formula}."
            )
        else:

            contexts_str = "\n\t".join(c.formula for c in contexts)
            self.message = (
                "*** ContextException EXCEPTION ***\n"
                + f"A failure has occurred on contexts, their are not "
                f"compatible.\nThe desired formula is : {formula}.\nThe contexts used are :\n\t{contexts_str} "
            )
        super().__init__(self.message)
