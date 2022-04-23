from dataclasses import dataclass, field
from enum import Enum, auto

from igraph import Graph, plot
from matplotlib import pyplot as plt

from crome_cgg.cgg.exceptions import GoalAlreadyPresent
from crome_cgg.goal import Goal
from crome_cgg.shared.paths import output_folder


class Link(Enum):
    refinement = auto()
    composition = auto()
    conjunction = auto()
    merging = auto()
    quotient = auto()
    separation = auto()


@dataclass
class Cgg:
    _graph: Graph = field(init=False, repr=False, default_factory=lambda: Graph())

    @property
    def graph(self):
        return list(self._graph)

    @property
    def n_nodes(self) -> int:
        return len(self._graph.vs)

    @property
    def n_edges(self) -> int:
        return len(self._graph.es)

    @property
    def nodes(self):
        return list(self._graph.vs)

    @property
    def goals(self) -> set[Goal | None]:
        if self.n_nodes > 0:
            return set(self._graph.vs()["goal"])
        return set()

    @property
    def goal_ids(self) -> set[str]:
        return set(self._graph.vs()["id"])

    def add_node(self, goal: Goal):
        if self.get_goal(id=goal.id) is None:
            self._graph.add_vertex(id=goal.id, goal=goal)
        else:
            raise GoalAlreadyPresent(goal=goal)

    def add_edge(self, node_a: Goal, node_b: Goal, link: Link):
        self._graph.add_edge(source=node_a.id, target=node_b.id, link=link)

    def get_goal(self, id: str) -> Goal | None:
        if len(self._graph.vs.select(id=id)) == 1:
            return self._graph.vs.select(id=id)["goal"][0]
        else:
            return None

    def draw(self):
        if self.n_nodes > 0:
            layout = self._graph.layout("kk")
            fig, ax = plt.subplots()
            plot(self._graph, layout=layout, target=ax)
            plt.savefig(output_folder / "cgg.pdf")
