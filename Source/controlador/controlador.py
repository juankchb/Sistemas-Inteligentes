import random
import networkx as nx

class GrafoControlador:
    def __init__(self, modelo, vista):
        self.modelo = modelo
        self.vista = vista

    def ejecutar(self, inicio, fin):
        self.modelo.cargar_datos()
        camino, longitud = self.modelo.obtener_camino_mas_corto(inicio, fin)
        self.vista.mostrar_camino(self.modelo.grafo, camino, longitud)
        
    def ejecutar_abejas(self, inicio, fin, num_bees=50, num_iterations=100):
        self.modelo.cargar_datos()
        best_path, best_path_length = self.modelo.bee_algorithm(inicio, fin, num_bees, num_iterations)
        if best_path:
            self.vista.mostrar_mejor_ruta(self.modelo.grafo, best_path, best_path_length)
        else:
            print("No se encontró un camino entre los nodos seleccionados.")
