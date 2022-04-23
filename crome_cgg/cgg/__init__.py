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
    quotient_dividend = auto()
    quotient_divisor = auto()
    separation_dividend = auto()
    separation_divisor = auto()


@dataclass
class Cgg:
    init_goals: set[Goal]
    _graph: Graph = field(init=False, repr=False, default_factory=lambda: Graph())

    def __post_init__(self):
        self._build_graph()

    def _build_graph(self) -> None:
        from crome_cgg.cgg.context_based_clustering import context_based_goal_clustering
        context_based_goal_clustering(self.init_goals, self)

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
            self._graph.add_vertex(name=goal.id, goal=goal)

    def add_edge(self, node_a: Goal, node_b: Goal, link: Link):
        if self.get_goal(node_a.id) is None:
            self.add_node(node_a)
        if self.get_goal(node_b.id) is None:
            self.add_node(node_b)
        self._graph.add_edge(source=node_a.id, target=node_b.id, link=link)

    def get_goal(self, id: str) -> Goal | None:
        if self.n_nodes > 0:
            if len(self._graph.vs.select(name=id)) == 1:
                return self._graph.vs.select(name=id)["goal"][0]
        return None

    def draw(self):
        if self.n_nodes > 0:
            layout = self._graph.layout("kk")
            fig, ax = plt.subplots()
            plot(self._graph, layout=layout, target=ax)
            plt.savefig(output_folder / "cgg.pdf")
