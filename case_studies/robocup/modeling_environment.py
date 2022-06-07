from core.specification import FormulaOutput
from core.specification.atom import Atom
from core.world import World
from robocup.variables import *


class RobocupHome(World):

    def __init__(self):
        super().__init__(
            actions={
                Hold(),
                Drop(),
                Reply(),
                Store()
            },
            locations={
                # L1(),
                # L2(),
                L3(),
                # L4(),
                # L5(),
                # L6(),
                # B1(),
                # B2(),
                # B3(),
                # H1(),
                H2(),
                E1(),
                E2(),
                K1(),
                # K2(),
                K3(),
                # R1(),
                # R2(),
            },
            sensors={
                ObjectRecognized(),
                Alexa(),
                GroceriesRecognized()
            },
            contexts={
                Housekeeping(),
                Party(),
                Cleanup(),
                Groceries(),
                Garbage()
            })


if __name__ == '__main__':
    w = RobocupHome()
    a_rules, a_ts = Atom.extract_mutex_rules(w.typeset, output=FormulaOutput.ListCNF)
    m_rules, m_ts = Atom.extract_adjacency_rules(w.typeset, output=FormulaOutput.ListCNF)

    print("\n".join(m_rules))
    print(", ".join(m_ts.keys()))
    print("\n\n")
    print("\n".join(a_rules))
    print(", ".join(a_ts.keys()))
