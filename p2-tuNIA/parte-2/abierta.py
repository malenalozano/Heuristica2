import heapq

class Abierta:
    def __init__(self):
        
        self.cola = [] # Usamos una cola para sacar el mejor nodo 
        
    def put(self, nodo, f, g, padre):
        """
        Añade un nodo a la lista de pendientes.
        nodo: ID de la ciudad
        f: coste total estimado (distancia recorrida + distancia a meta)
        g: distancia real ya recorrida
        padre: de qué ciudad venimos (para luego reconstruir el camino)
        """
        # Guardamos una tupla
        heapq.heappush(self.cola, (f, nodo, g, padre))

    def pop(self):
        """Saca y devuelve el mejor nodo (el que tenga menor f)"""
        if self.is_empty():
            return None
        return heapq.heappop(self.cola)

    def is_empty(self):
        return len(self.cola) == 0