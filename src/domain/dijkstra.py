import heapq

from src.domain.models import Node, Grid

def reconstruct_path(node: Node) -> list[Node]:
    path = [node]
    if node.previous_node:
        path = reconstruct_path(node.previous_node) + path

    return path


def dijkstra_search(grid: Grid, start_node: Node, end_node: Node):
    grid.reset_search()
    start_node.distance = 0.0
    priority_queue = []
    heapq.heappush(priority_queue, (0.0, start_node))

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node.visited:
            continue

        current_node.visited = True
        yield "visiting", current_node

        if current_node == end_node:
            path = reconstruct_path(current_node)
            yield "finished", path
            return

        for neighbor in grid.get_neighbors(current_node):
            if neighbor.visited:
                continue

            new_distance = current_distance + 1.0
            if new_distance < neighbor.distance:
                neighbor.distance = new_distance
                neighbor.previous_node = current_node
                heapq.heappush(priority_queue, (new_distance, neighbor))

    yield "no_path", []
