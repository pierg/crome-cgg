from dataclasses import dataclass, field
from enum import Enum, auto

from igraph import Graph, plot
from matplotlib import pyplot as plt

from crome_cgg.cgg.exceptions import GoalAlreadyPresent
from crome_cgg.goal import Goal
from crome_cgg.shared.paths import output_folder
from tools.strings import tab


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
    _graph: Graph = field(init=False, repr=False, default_factory=lambda: Graph(directed=True))

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
    def root(self) -> Goal:
        for goal_id in self.goal_ids:
            if len(self._graph.es.select(_source=goal_id)) == 0:
                return self.get_goal_by_id(goal_id)
        raise Exception("No Root")

    @property
    def leaves(self) -> set[Goal]:
        leaves: set[Goal] = set()
        for goal_id in self.goal_ids:
            if len(self._graph.es.select(_target=goal_id)) == 0:
                leaves.add(self.get_goal_by_id(goal_id))
        return leaves

    @property
    def goals(self) -> set[Goal | None]:
        if self.n_nodes > 0:
            return set(self._graph.vs()["goal"])
        return set()

    @property
    def goal_ids(self) -> set[str]:
        return set(self._graph.vs()["name"])

    def add_node(self, goal: Goal):
        if self.get_goal_by_id(goal_id=goal.id) is None:
            self._graph.add_vertex(name=goal.id, goal=goal)

    def add_edge(self, node_a: Goal, node_b: Goal, link: Link):
        if self.get_goal_by_id(node_a.id) is None:
            self.add_node(node_a)
        if self.get_goal_by_id(node_b.id) is None:
            self.add_node(node_b)
        self._graph.add_edge(source=node_a.id, target=node_b.id, link=link)

    def get_goal_by_id(self, goal_id: str) -> Goal | None:
        if self.n_nodes > 0:
            if len(self._graph.vs.select(name=goal_id)) == 1:
                return self._graph.vs.select(name=goal_id)["goal"][0]
        return None

    def get_parents_of(self, goal: Goal) -> dict[Link, set[Goal]] | None:
        if len(self._graph.es.select(_source=goal.id)) > 0:
            connections_map: dict[Link, set[Goal]] = {}
            for edge in self._graph.es.select(_source=goal.id):
                if edge["link"] in connections_map.keys():
                    connections_map[edge["link"]].add(edge.target_vertex["goal"])
                else:
                    connections_map[edge["link"]] = {edge.target_vertex["goal"]}
            return connections_map
        return None

    def get_children_of(self, goal: Goal) -> dict[Link, set[Goal]] | None:
        if len(self._graph.es.select(_target=goal.id)) > 0:
            connections_map: dict[Link, set[Goal]] = {}
            for edge in self._graph.es.select(_target=goal.id):
                if edge["link"] in connections_map.keys():
                    connections_map[edge["link"]].add(edge.source_vertex["goal"])
                else:
                    connections_map[edge["link"]] = {edge.source_vertex["goal"]}
            return connections_map
        return None

    def __str__(self):
        if self.get_children_of(self.root) is not None:
            return self._print_node(self.root)


    def _print_node(self, node: Goal, level=1):
        if node in self.leaves:
            return tab(str(node), how_many=level)
        res = ""
        for link, goals in self.get_children_of(node).items():
            res += ("\t" * level) + f"{link.name}\n"
            for goal in goals:
                res += self._print_node(goal, level+1)
        return res



    def draw(self):
        """TODO: Better draw function"""
        if self.n_nodes > 0:
            layout = self._graph.layout("kk")
            fig, ax = plt.subplots()
            plot(self._graph, layout=layout, target=ax)
            plt.savefig(output_folder / "cgg.pdf")
