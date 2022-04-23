from crome_logic.specification.temporal import LTL


class Context(LTL):
    pass


def group_conjunction(elements: set[Context]) -> Context:
    # TODO: Implement
    return next(iter(elements))


def group_disjunction(elements: set[Context]) -> Context:
    # TODO: Implement
    return next(iter(elements))
