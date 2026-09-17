import time
import streamlit as st
import sys
from pathlib import Path

# Adiciona a raiz do projeto ao PYTHONPATH para reconhecer 'src'
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))


from src.domain.models import Grid, NodeType, Position
from src.domain.dijkstra import dijkstra_search
from src.services.maze_service import MazeService
from src.ui.components import render_grid_html

st.set_page_config(
    page_title="Visualizador do Algoritmo de Dijkstra",
    page_icon="🧭",
    layout="wide",
)

st.title("🧭 Visualizador Interativo: Algoritmo de Dijkstra")
st.markdown(
    "Demonstração visual do algoritmo de menor caminho em grafos bidimensionais. "
    "Construído com **Clean Architecture** e **Python puro**."
)

# ---------------------------------------------------------
# 1. Configurações na Barra Lateral
# ---------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Configurações da Malha")


    rows = st.slider("Linhas", min_value=10, max_value=25, value=15, step=1)
    cols = st.slider("Colunas", min_value=10, max_value=35, value=25, step=1)

    st.markdown("---")
    st.subheader("📍 Posição de Início e Fim")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        start_row = st.number_input("Linha Início", min_value=0, max_value=rows - 1, value=1, step=1)
    with col_s2:
        start_col = st.number_input("Coluna Início", min_value=0, max_value=cols - 1, value=1, step=1)

    col_e1, col_e2 = st.columns(2)
    with col_e1:
        end_row = st.number_input("Linha Fim", min_value=0, max_value=rows - 1, value=rows - 2, step=1)
    with col_e2:
        end_col = st.number_input("Coluna Fim", min_value=0, max_value=cols - 1, value=cols - 2, step=1)

    speed = st.slider(
        "Velocidade da Animação (delay em seg)",
        min_value=0.00,
        max_value=0.10,
        value=0.02,
        step=0.01,
        help="0 é o mais rápido possível",
    )

    st.markdown("---")
    st.header("🧱 Controle de Paredes")

    density = st.slider("Densidade de Paredes", 0.10, 0.40, 0.25, 0.05)

    if st.button("🎲 Gerar Labirinto Aleatório", use_container_width=True):
        if "grid" in st.session_state:
            MazeService.generate_random_walls(
                st.session_state.grid,
                st.session_state.start,
                st.session_state.end,
                wall_density=density,
            )
            st.session_state.last_path = None
            st.session_state.visited_count = 0

    if st.button("🧹 Limpar Paredes e Busca", use_container_width=True):
        if "grid" in st.session_state:
            MazeService.clear_walls(st.session_state.grid)
            st.session_state.grid.reset_search()
            st.session_state.last_path = None
            st.session_state.visited_count = 0

    st.markdown("---")
    st.header("🎨 Legenda")
    st.markdown(
        """
        - 🟢 **Verde**: Início
        - 🔴 **Vermelho**: Fim
        - ⬛ **Cinza Escuro**: Parede (Obstáculo)
        - 🔵 **Azul Claro**: Nós Visitados (Fronteira)
        - 🟡 **Amarelo**: Menor Caminho Encontrado
        """
    )

# ---------------------------------------------------------
# 2. Inicialização do Estado (Session State)
# ---------------------------------------------------------
# Se o tamanho mudou ou se ainda não criamos a grade, inicializa uma nova grade:
if (
    "grid" not in st.session_state
    or st.session_state.grid.rows != rows
    or st.session_state.grid.cols != cols
):
    st.session_state.grid = Grid(rows=rows, cols=cols)
    st.session_state.start = st.session_state.grid.get_node(start_row, start_col)
    st.session_state.start.node_type = NodeType.START

    st.session_state.end = st.session_state.grid.get_node(end_row, end_col)
    st.session_state.end.node_type = NodeType.END

    st.session_state.last_path = None
    st.session_state.visited_count = 0
else:
    # A grade já existe: verifica se o usuário alterou a posição do Início ou do Fim
    grid = st.session_state.grid

    # Se o Início mudou de lugar
    if st.session_state.start.position != Position(start_row, start_col):
        st.session_state.start.node_type = NodeType.EMPTY
        st.session_state.start = grid.get_node(start_row, start_col)
        st.session_state.start.node_type = NodeType.START
        st.session_state.last_path = None

    # Se o Fim mudou de lugar
    if st.session_state.end.position != Position(end_row, end_col):
        st.session_state.end.node_type = NodeType.EMPTY
        st.session_state.end = grid.get_node(end_row, end_col)
        st.session_state.end.node_type = NodeType.END
        st.session_state.last_path = None

grid = st.session_state.grid
start = st.session_state.start
end = st.session_state.end

# ---------------------------------------------------------
# 3. Painel Central de Controle e Métricas
# ---------------------------------------------------------
col_btn, col_m1, col_m2, col_m3 = st.columns([2, 1, 1, 1])

with col_btn:
    start_clicked = st.button(
        "🚀 Iniciar Busca do Dijkstra", type="primary", use_container_width=True
    )

m1_metric = col_m1.empty()
m2_metric = col_m2.empty()
m3_metric = col_m3.empty()

m1_metric.metric("Nós Visitados", st.session_state.visited_count)
m2_metric.metric(
    "Tamanho da Rota",
    len(st.session_state.last_path) if st.session_state.last_path else 0,
)
m3_metric.metric(
    "Custo Total",
    f"{end.distance:.0f}" if end.distance != float("inf") else "-",
)

# Placeholder para o desenho do tabuleiro na tela
grid_placeholder = st.empty()

# Desenha a grade com o estado atual
grid_placeholder.markdown(
    render_grid_html(grid, start, end, path=st.session_state.last_path),
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 4. Execução da Busca e Animação
# ---------------------------------------------------------
if start_clicked:
    grid.reset_search()
    st.session_state.last_path = None
    visited_counter = 0
    start_time = time.time()

    # Consome os eventos que o yield do dijkstra_search vai emitindo!
    for event, data in dijkstra_search(grid, start, end):
        if event == "visiting":
            visited_counter += 1
            # Atualiza métricas e renderiza a tela a cada passo
            m1_metric.metric("Nós Visitados", visited_counter)
            grid_placeholder.markdown(
                render_grid_html(grid, start, end),
                unsafe_allow_html=True,
            )
            if speed > 0:
                time.sleep(speed)

        elif event == "finished":
            elapsed = time.time() - start_time
            st.session_state.last_path = data
            st.session_state.visited_count = visited_counter

            m1_metric.metric("Nós Visitados", visited_counter)
            m2_metric.metric("Tamanho da Rota", len(data))
            m3_metric.metric("Custo Total", f"{end.distance:.0f}")

            # Renderiza o caminho final em amarelo dourado!
            grid_placeholder.markdown(
                render_grid_html(grid, start, end, path=data),
                unsafe_allow_html=True,
            )
            st.success(
                f"🎯 Menor caminho encontrado em {elapsed:.2f} segundos! "
                f"Distância total: {end.distance:.0f} passos."
            )
            break

        elif event == "no_path":
            st.error(
                "❌ Não foi possível encontrar um caminho até o destino. "
                "O nó final está completamente bloqueado por paredes!"
            )
            break