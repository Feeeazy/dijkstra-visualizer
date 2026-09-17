import random
from src.domain.models import Grid, Node, NodeType


class MazeService:
    @staticmethod
    def generate_random_walls(grid: Grid, start: Node, end: Node, wall_density: float = 0.25):
        for row in grid.nodes:
            for node in row:
                if node == start or node == end:
                    continue

                if random.random() < wall_density:
                    node.node_type = NodeType.WALL
                else:
                    node.node_type = NodeType.EMPTY


    @staticmethod
    def clear_walls(grid: Grid):
        for row in grid.nodes:
            for node in row:
                if node.node_type == NodeType.WALL:
                    node.node_type = NodeType.EMPTY

