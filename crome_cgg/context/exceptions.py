from __future__ import annotations
from crome_cgg.context import Context
from dataclasses import dataclass


@dataclass(kw_only=True)
class ContextException(Exception):
    contexts: set[Context]

    def __post_init(self):
        contexts_str = "\n\n".join(repr(c) for c in self.contexts)
        message = "*** ContextException EXCEPTION ***\n" + f"A failure has occurred on contexts, their are not " \
                                                           f"compatible:\n {contexts_str} "
        print(message)
