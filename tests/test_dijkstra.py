from src.domain.dijkstra import dijkstra_search, reconstruct_path
from src.domain.models import Grid, NodeType, Position, Node


def test_reconstruct_path_single_node():
    """Testa reconstrução com apenas o nó inicial."""
    node = Node(position=Position(0, 0))
    path = reconstruct_path(node)
    assert len(path) == 1
    assert path[0] == node


def test_reconstruct_path_chain():
    """Testa se a ordem do caminho reconstruído fica correta: início -> meio -> fim."""
    start = Node(position=Position(0, 0))
    mid = Node(position=Position(0, 1), previous_node=start)
    end = Node(position=Position(0, 2), previous_node=mid)

    path = reconstruct_path(end)
    assert len(path) == 3
    assert path == [start, mid, end]


def test_dijkstra_straight_path():
    """Testa o menor caminho em linha reta numa grade 3x3 limpa."""
    grid = Grid(rows=3, cols=3)
    start = grid.get_node(0, 0)
    end = grid.get_node(0, 2)

    # Executa todos os passos do gerador até o final
    final_event = None
    final_path = []
    for event, data in dijkstra_search(grid, start, end):
        final_event = event
        if event == "finished":
            final_path = data

    assert final_event == "finished"
    assert len(final_path) == 3  # (0,0) -> (0,1) -> (0,2)
    assert final_path[0] == start
    assert final_path[-1] == end
    assert end.distance == 2.0


def test_dijkstra_navigates_around_wall():
    """
    Testa se o algoritmo desvia de uma parede:
    S . .
    # # .
    . . E
    """
    grid = Grid(rows=3, cols=3)
    start = grid.get_node(0, 0)
    end = grid.get_node(2, 2)

    # Cria parede bloqueando a passagem direta
    grid.get_node(1, 0).node_type = NodeType.WALL
    grid.get_node(1, 1).node_type = NodeType.WALL

    final_event = None
    final_path = []
    for event, data in dijkstra_search(grid, start, end):
        final_event = event
        if event == "finished":
            final_path = data

    assert final_event == "finished"
    assert final_path[-1] == end
    # Garante que nenhum nó do caminho é parede
    assert all(not node.is_wall() for node in final_path)


def test_dijkstra_no_path_when_blocked():
    """Testa se o algoritmo detecta que é impossível chegar se o destino estiver cercado."""
    grid = Grid(rows=3, cols=3)
    start = grid.get_node(0, 0)
    end = grid.get_node(2, 2)

    # Cerca completamente o nó final com paredes
    grid.get_node(1, 2).node_type = NodeType.WALL
    grid.get_node(2, 1).node_type = NodeType.WALL

    final_event = None
    for event, data in dijkstra_search(grid, start, end):
        final_event = event

    assert final_event == "no_path"