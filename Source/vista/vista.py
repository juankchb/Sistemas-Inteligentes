import networkx as nx
import matplotlib.pyplot as plt
import osmnx as ox
import seaborn as sns

class GrafoVista:
    def mostrar_camino(self, grafo, camino, longitud):
        pos = {nodo: (datos['longitud'], datos['latitud']) for nodo, datos in grafo.nodes(data=True)}
        nx.draw(grafo, pos, with_labels=True, node_size=50, node_color='blue', font_size=8, font_color='black')
        path_edges = list(zip(camino, camino[1:]))
        nx.draw_networkx_nodes(grafo, pos, nodelist=camino, node_color='red', node_size=100)
        nx.draw_networkx_edges(grafo, pos, edgelist=path_edges, edge_color='red', width=2)
        plt.title(f'Camino más corto: {longitud:.2f} metros')
        plt.show()
        
    def mostrar_histograma(self, path_lengths):
        plt.hist(path_lengths)
        plt.xlabel("Longitud del camino")
        plt.ylabel("Frecuencia")
        plt.title("Histograma de rendimiento del algoritmo de forrajeo de abejas")
        plt.show()

    def mostrar_mejor_ruta(self, grafo, best_path, best_path_length):
        node_positions = {node: (data['x'], data['y']) for node, data in grafo.nodes(data=True)}
        
        fig, ax = plt.subplots(figsize=(12, 12))
        ox.plot_graph(grafo, node_size=10, edge_linewidth=0.5, show=False, ax=ax)

        if best_path:
            best_route_edges = list(zip(best_path[:-1], best_path[1:]))
            nx.draw_networkx_edges(grafo, pos=node_positions, edgelist=best_route_edges, edge_color='r', width=2, ax=ax)
            plt.title(f"Mejor ruta encontrada con longitud {best_path_length}")
        else:
            plt.title("No se encontró un camino entre los nodos seleccionados.")

        plt.show()
