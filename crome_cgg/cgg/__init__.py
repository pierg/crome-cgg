import json
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Any

from igraph import Graph, plot
from matplotlib import pyplot as plt

from crome_cgg.goal import Goal
from crome_cgg.shared.paths import output_folder_cgg
from crome_cgg.tools.strings import tab, tabar
from crome_logic.tools.crome_io import save_to_file


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
    _graph: Graph = field(
        init=False, repr=False, default_factory=lambda: Graph(directed=True)
    )

    def __post_init__(self):
        self._build_graph()

    def _build_graph(self) -> None:
        from crome_cgg.cgg.context_based_clustering import context_based_goal_clustering

        context_based_goal_clustering(self.init_goals, self)

    @property
    def graph(self):
        return self._graph

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
    def leaves_dict(self) -> dict[str, Goal]:
        leaves: dict[str, Goal] = dict()
        for goal_id in self.goal_ids:
            if len(self._graph.es.select(_target=goal_id)) == 0:
                leaves[goal_id] = self.get_goal_by_id(goal_id)
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
            return tab(self._print_node(self.root), how_many=2)

    def _print_node(self, node: Goal, level=0):
        if node in self.leaves:
            return tabar(str(node), how_many=level)
        res = []
        for link, goals in self.get_children_of(node).items():
            res.append(tabar(str(node), how_many=level))
            res.append(f"{tabar('', level)}|---LINK: {link.name}")
            res.append(f"{tabar('', level+1)}|")
            for goal in goals:
                res.append(self._print_node(goal, level + 1))
        return "\n".join(res)

    def draw(self):
        """TODO: Better draw function"""
        if self.n_nodes > 0:
            layout = self._graph.layout("kk")
            fig, ax = plt.subplots()
            plot(self._graph, layout=layout, target=ax)
            plt.savefig(output_folder_cgg / "cgg.pdf")

    def export_to_json(self, project_path: Path | None = None) -> dict[str, Any]:
        json_content = {"nodes": [], "edges": []}
        for node in self.nodes:
            json_content["nodes"].append({"id": node["goal"].id})

        for edge in self._graph.es:
            source_vertex_id = edge.source
            target_vertex_id = edge.target
            source_node_id = self.nodes[source_vertex_id]["goal"].id
            target_node_id = self.nodes[target_vertex_id]["goal"].id
            json_content["edges"].append(
                {
                    "from": source_node_id,
                    "to": target_node_id,
                    "link": edge["link"].name,
                }
            )

        if project_path is not None:
            json_formatted = json.dumps(json_content, indent=4, sort_keys=True)
            save_to_file(
                file_content=json_formatted,
                file_name="cgg.json",
                absolute_folder_path=project_path,
            )

        return json_content
