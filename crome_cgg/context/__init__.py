from crome_logic.specification.boolean import Bool


class Context(Bool):
    pass


def group_conjunction(elements: set[Context]) -> Context:
    # TODO: Implement
    return next(iter(elements))


def group_disjunction(elements: set[Context]) -> Context:
    # TODO: Implement
    return next(iter(elements))
