import numpy as np
import networkx as nx
import time
import matplotlib.pyplot as plt

# 1. Gerar pontos (bairros)
def gerar_pontos(n=40):
    """Gera n pontos aleatórios (x, y)."""
    pontos = np.random.rand(n, 2) * 100
    return pontos

# 2. Construir grafo completo
def construir_grafo(pontos):
    """Constrói grafo completo com pesos = distância euclidiana."""
    G = nx.Graph()
    for i in range(len(pontos)):
        for j in range(i+1, len(pontos)):
            dist = np.linalg.norm(pontos[i] - pontos[j])
            G.add_edge(i, j, weight=dist)
    return G

# 3. Rodar MST com Kruskal
def mst_kruskal(G):
    t0 = time.time()
    mst = nx.minimum_spanning_tree(G, algorithm="kruskal")
    t1 = time.time()
    tempo = (t1 - t0) * 1000  # ms
    custo = sum(nx.get_edge_attributes(mst, 'weight').values())
    return tempo, custo

# 4. Rodar MST com Prim
def mst_prim(G):
    t0 = time.time()
    mst = nx.minimum_spanning_tree(G, algorithm="prim")
    t1 = time.time()
    tempo = (t1 - t0) * 1000  # ms
    custo = sum(nx.get_edge_attributes(mst, 'weight').values())
    return tempo, custo

# 5. Executar experimento
def executar_experimento(repeticoes=10):
    tempos_kruskal = []
    tempos_prim = []
    custos = []

    for _ in range(repeticoes):
        pontos = gerar_pontos()
        G = construir_grafo(pontos)

        tk, ck = mst_kruskal(G)
        tp, cp = mst_prim(G)

        tempos_kruskal.append(tk)
        tempos_prim.append(tp)
        custos.append(ck)

    return tempos_kruskal, tempos_prim, custos


# Rodar o experimento
tempos_kruskal, tempos_prim, custos = executar_experimento()

# 6. Imprimir resultados

print("===== RESULTADOS MÉDIOS =====")
print(f"Tempo médio Kruskal: {np.mean(tempos_kruskal):.3f} ms")
print(f"Tempo médio Prim:    {np.mean(tempos_prim):.3f} ms")
print(f"Custo médio MST:     {np.mean(custos):.3f}")

print("\n===== TABELA COMPLETA =====")
print("Exec | Kruskal (ms) | Prim (ms) | Custo da MST")
for i in range(len(tempos_kruskal)):
    print(f"{i+1:>4} | {tempos_kruskal[i]:>12.3f} | {tempos_prim[i]:>9.3f} | {custos[i]:>12.3f}")

# 7. Gráfico de comparação
plt.figure(figsize=(10, 5))
plt.plot(tempos_kruskal, label="Kruskal")
plt.plot(tempos_prim, label="Prim")
plt.title("Comparação do Tempo de Execução - Kruskal vs Prim")
plt.xlabel("Execução")
plt.ylabel("Tempo (ms)")
plt.legend()
plt.grid(True)
plt.show()
