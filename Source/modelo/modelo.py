import pandas as pd
import networkx as nx
import random
import osmnx as ox

class GrafoModelo:
    def __init__(self, data):
        self.data = data
        self.grafo = None
        self.nodos = None
        self.aristas = None
        self.cargar_datos()

    def cargar_datos(self):
        if isinstance(self.data, pd.DataFrame):
            self.nodos = self.data[['id', 'speed', 'travel_time']].drop_duplicates()
            self.aristas = self.data[['id', 'link_id', 'speed']].drop_duplicates()
        else:
            raise ValueError("Debe proporcionar un DataFrame válido.")

        self.grafo = nx.DiGraph()
        
        for _, row in self.nodos.iterrows():
            self.grafo.add_node(row['id'], speed=row['speed'], travel_time=row['travel_time'])

        for _, row in self.aristas.iterrows():
            self.grafo.add_edge(row['id'], row['link_id'], weight=row['speed'])

    def obtener_camino_mas_corto(self, inicio, fin):
        camino = nx.shortest_path(self.grafo, source=inicio, target=fin, weight='weight')
        longitud = nx.shortest_path_length(self.grafo, source=inicio, target=fin, weight='weight')
        return camino, longitud
    
    def bee_algorithm(self, start_node, end_node, num_bees=50, num_iterations=100):
        best_path = None
        best_path_length = float('inf')

        for iteration in range(num_iterations):
            paths = []
            path_lengths = []

            for bee in range(num_bees):
                try:
                    path = nx.shortest_path(self.grafo, source=start_node, target=end_node, weight='weight')
                    path_length = nx.shortest_path_length(self.grafo, source=start_node, target=end_node, weight='weight')
                    paths.append(path)
                    path_lengths.append(path_length)

                    if random.random() < 0.1:
                        u, v = random.choice(list(self.grafo.edges()))
                        if 'traffic' in self.grafo[u][v]:
                            self.grafo[u][v]['traffic'] = max(1, self.grafo[u][v]['traffic'] - 1)

                except nx.NetworkXNoPath:
                    continue

            if paths:
                min_length_index = path_lengths.index(min(path_lengths))

                if path_lengths[min_length_index] < best_path_length:
                    best_path = paths[min_length_index]
                    best_path_length = path_lengths[min_length_index]

                for path in paths:
                    for i in range(len(path) - 1):
                        u, v = path[i], path[i + 1]
                        if 'traffic' in self.grafo[u][v]:
                            self.grafo[u][v]['traffic'] += 1

        return best_path, best_path_length

    def coords_to_node(self, coords):
        if self.grafo is None:
            raise ValueError("El grafo no ha sido inicializado.")
        return ox.distance.nearest_nodes(self.grafo, coords[1], coords[0])
