# 🧭 Dijkstra Pathfinding Visualizer

Uma aplicação interativa para visualização e estudo do **Algoritmo de Dijkstra** em malhas bidimensionais, desenvolvida em **Python 3.12** com foco em **Clean Architecture**, **Orientação a Objetos**, **Testes Automatizados (Pytest)** e interface reativa com **Streamlit**.

---

## Sobre o Projeto

O objetivo principal deste projeto foi consolidar **fundamentos de Engenharia de Software e Estruturas de Dados**, aplicando boas práticas de arquitetura para desacoplar a lógica algorítmica pura da interface gráfica.

### Principais Recursos
- **Busca de Menor Caminho**: Execução passo a passo do algoritmo de Dijkstra com animação da fronteira de nós visitados.
- **Pontos Customizáveis**: Seleção dinâmica de nós de Início (*Start*) e Fim (*Target*) com validação estrita de limites de matriz.
- **Geração de Labirintos**: Algoritmo de densidade configurável para geração de obstáculos sem sobrescrever pontos de partida e chegada.
- **Métricas em Tempo Real**: Apresentação de nós visitados, custo total do menor trajeto e tempo de processamento.
- **Testes Automatizados**: Cobertura completa de modelos e casos de borda com Pytest.

---

## 🧮 Complexidade Algorítmica
Considerando uma malha com $V$ vértices (células) e $E$ arestas (conexões entre vizinhos ortogonais):
- **Complexidade de Tempo**: $O((V + E) \log V)$ utilizando a Fila de Prioridade com Heap Binário.
- **Complexidade de Espaço**: $O(V)$ para manter as distâncias, nós visitados e ponteiros encadeados de retorno (`previous_node`).

## Como Executar o Projeto
### Pré-requisitos
- **Python 3.10+** (recomendado Python 3.12)
- **Git**
### 1. Clonar o Repositório
```bash
git clone https://github.com/SEU_USUARIO/dijkstra-visualizer.git
cd dijkstra-visualizer

# Criar o ambiente virtual
python -m venv .venv
# Ativar no Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
# Instalar dependencias
pip install -r requirements.txt
# Executar a aplicação
streamlit run src/ui/app.py```