from typing import List, Optional, Set
from src.domain.models import Grid, Node, NodeType, Position


def get_node_color(
    node: Node,
    start: Node,
    end: Node,
    path_positions: Set[Position],
) -> str:
    """Define a cor CSS de cada célula com base no seu estado atual."""
    if node == start:
        return "#22c55e"  # Verde (Início)
    if node == end:
        return "#ef4444"  # Vermelho (Fim)
    if node.position in path_positions:
        return "#eab308"  # Amarelo dourado (Caminho mais curto)
    if node.is_wall():
        return "#334155"  # Cinza escuro/Chumbo (Parede)
    if node.visited:
        return "#38bdf8"  # Azul claro (Visitado pelo algoritmo)
    return "#f8fafc"      # Branco suave (Caminho livre)


def render_grid_html(
    grid: Grid,
    start_node: Node,
    end_node: Node,
    path: Optional[List[Node]] = None,
) -> str:
    """
    Gera um container HTML com CSS Grid responsivo desenhando as células.
    """
    path_positions: Set[Position] = (
        {n.position for n in path} if path else set()
    )

    cell_size = 24  # pixels por célula
    grid_width = grid.cols * (cell_size + 2)

    cells_html = []
    for row in grid.nodes:
        for node in row:
            color = get_node_color(node, start_node, end_node, path_positions)
            cells_html.append(
                f'<div style="'
                f'width: {cell_size}px; '
                f'height: {cell_size}px; '
                f'background-color: {color}; '
                f'border-radius: 4px; '
                f'box-shadow: inset 0 0 0 1px rgba(0,0,0,0.1);'
                f'"></div>'
            )

    html = f"""
    <div style="display: flex; justify-content: center; margin: 15px 0;">
        <div style="
            display: grid;
            grid-template-columns: repeat({grid.cols}, {cell_size}px);
            gap: 2px;
            background-color: #e2e8f0;
            padding: 8px;
            border-radius: 8px;
            width: fit-content;
        ">
            {''.join(cells_html)}
        </div>
    </div>
    """
    return html