from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class NodeType(Enum):
    EMPTY = "empty"
    START = "start"
    END = "end"
    WALL = "wall"

@dataclass(frozen=True)
class Position:
    row: int
    col: int

@dataclass
class Node:
    position: Position
    node_type: NodeType = NodeType.EMPTY
    distance: float = float("inf")
    visited: bool = False
    previous_node: Optional["Node"] = field(default=None, repr=False)

    def __lt__(self, other):
        return self.distance < other.distance

    def reset_state(self):
        self.distance = float("inf")
        self.visited = False
        self.previous_node = None

    def is_wall(self):
        return self.node_type == NodeType.WALL

class Grid:
    def __init__(self, rows: int, cols: int):
        if rows == 0 or cols == 0:
            raise ValueError("Valor para 'rows' ou 'cols' deve ser diferente de 0(zero).")

        self.rows = rows
        self.cols = cols
        self.nodes = [[Node(position=Position(r, c))  for c in range(self.cols)]for r in range(self.rows)]


    def get_node(self, row: int, col:int) -> Node:
        if (0 <= row < self.rows) and (0 <= col < self.cols):
            return self.nodes[row][col]

        raise IndexError(f"Posição ({row}x{col}) fora do limite do Grid.")


    def get_neighbors(self, node: Node) -> list[Node]:
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        node_row = node.position.row
        node_col = node.position.col
        neighbors = []

        for dr, dc in directions:
            try:
                dr = node_row + dr
                dc = node_col + dc
                neighbor = self.get_node(dr, dc)
                if not neighbor.is_wall():
                    neighbors.append(neighbor)
            except IndexError:
                continue

        return neighbors

    def reset_search(self):
        for row in self.nodes:
            for node in row:
                node.reset_state()