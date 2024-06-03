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
        print("Loading data into the graph...")
        if isinstance(self.data, pd.DataFrame):
            print("Data is a valid DataFrame.")
            print(f"Data columns: {self.data.columns}")
            print(f"Data sample:\n{self.data.head()}")

            try:
                self.nodos = self.data[['id']].drop_duplicates()
                self.aristas = self.data[['id', 'link_id', 'speed', 'travel_time', 'status']].drop_duplicates()
                print("Nodes data prepared:")
                print(self.nodos.head())
                print("Edges data prepared:")
                print(self.aristas.head())
            except KeyError as e:
                print(f"KeyError: {e}")
                raise ValueError("The DataFrame does not contain the required columns.")
        else:
            raise ValueError("Debe proporcionar un DataFrame válido.")
        
        self.grafo = nx.DiGraph()
        
        print("Adding nodes to the graph...")
        for _, row in self.nodos.iterrows():
            self.grafo.add_node(row['id'])
        print("Nodes added successfully.")
        
        print("Adding edges to the graph...")
        for _, row in self.aristas.iterrows():
            self.grafo.add_edge(row['id'], row['link_id'], weight=row['speed'])
        print("Edges added successfully.")
        print("Graph created successfully.")

    def obtener_camino_mas_corto(self, inicio, fin):
        print(f"Finding shortest path from {inicio} to {fin}...")
        camino = nx.shortest_path(self.grafo, source=inicio, target=fin, weight='weight')
        longitud = nx.shortest_path_length(self.grafo, source=inicio, target=fin, weight='weight')
        print("Shortest path found successfully.")
        return camino, longitud
    
    def bee_algorithm(self, start_node, end_node, num_bees=50, num_iterations=100):
        print("Running bee algorithm...")
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

        print("Bee algorithm completed.")
        return best_path, best_path_length

    def coords_to_node(self, coords):
        if self.grafo is None:
            raise ValueError("El grafo no ha sido inicializado.")
        return ox.distance.nearest_nodes(self.grafo, coords[1], coords[0])
