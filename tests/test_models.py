import pytest
from src.domain.models import Grid, Node, NodeType, Position


def test_position_creation():
    """Testa se a coordenada (linha, coluna) é salva corretamente."""
    pos = Position(row=2, col=5)
    assert pos.row == 2
    assert pos.col == 5


def test_node_initial_state():
    """Testa se o nó nasce com valores padrão corretos (distância infinita, não visitado)."""
    pos = Position(row=0, col=0)
    node = Node(position=pos)
    assert node.distance == float("inf")
    assert node.visited is False
    assert node.node_type == NodeType.EMPTY
    assert not node.is_wall()
    assert node.previous_node is None


def test_node_priority_comparison():
    """
    Testa se o operador '<' compara pela distância.
    O nó com menor distância deve ser considerado menor (prioridade na fila do Dijkstra).
    """
    node_a = Node(position=Position(0, 0), distance=10.0)
    node_b = Node(position=Position(0, 1), distance=5.0)
    assert node_b < node_a


def test_grid_initialization_and_valid_node():
    """Testa se a grade cria as dimensões certas e retorna um nó válido."""
    grid = Grid(rows=10, cols=10)
    assert grid.rows == 10
    assert grid.cols == 10

    node = grid.get_node(0, 0)
    assert node.position == Position(0, 0)


def test_grid_out_of_bounds_raises_error():
    """Testa se tentar acessar posições fora do tabuleiro sobe IndexError."""
    grid = Grid(rows=10, cols=10)

    # Linha muito grande
    with pytest.raises(IndexError):
        grid.get_node(99, 0)

    # Coluna muito grande
    with pytest.raises(IndexError):
        grid.get_node(0, 99)

    # Linha ou coluna negativa
    with pytest.raises(IndexError):
        grid.get_node(-1, 0)
    with pytest.raises(IndexError):
        grid.get_node(0, -1)


def test_grid_neighbors_and_wall_filtering():
    """Testa se get_neighbors ignora paredes e traz os vizinhos ortogonais corretos."""
    grid = Grid(rows=3, cols=3)
    center = grid.get_node(1, 1)

    # O nó central (1, 1) tem 4 vizinhos: cima, baixo, esquerda, direita
    neighbors = grid.get_neighbors(center)
    assert len(neighbors) == 4

    # Agora transformamos o vizinho de cima (0, 1) em parede
    grid.get_node(0, 1).node_type = NodeType.WALL

    # Agora devem sobrar apenas 3 vizinhos válidos
    filtered_neighbors = grid.get_neighbors(center)
    assert len(filtered_neighbors) == 3
    assert all(not n.is_wall() for n in filtered_neighbors)