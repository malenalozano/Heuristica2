import math
from abierta import Abierta
from cerrada import Cerrada

class AlgoritmoAEstrella:
    def __init__(self, mapa):
        self.mapa = mapa

    #distancia entre dos puntos --> raiz((x1-x2)^2 + (y1-y2)^2)
    def heuristica(self, nodo_actual, nodo_destino):
        pos_a = self.mapa.get_posicion(nodo_actual)
        pos_b = self.mapa.get_posicion(nodo_destino)
        
        if pos_a == (0,0) or pos_b == (0,0): # Si no hay coordenadas se le devolvemos 0 
            return 0
            
        
        dx = pos_a[0] - pos_b[0]
        dy = pos_a[1] - pos_b[1]
        return math.sqrt(dx**2 + dy**2)

    def resolver(self, origen, destino):
        
        abierta = Abierta()
        cerrada = Cerrada()
        padres = {} 
        nodos_expandidos = 0
        
        h_inicial = self.heuristica(origen, destino)
        abierta.put(origen, h_inicial, 0, None) 
        
       
        
        
        while not abierta.is_empty():
            
            f, actual, g, padre = abierta.pop()
            
            
            if cerrada.contains(actual):
                if g >= cerrada.get_g(actual):
                    continue
                
            cerrada.add(actual, g) # Lo marcamos como visitado
            padres[actual] = padre
            nodos_expandidos += 1
            
            
            if actual == destino:                                       #Se ha llegado al destino
                camino = self.reconstruir_camino(padres, destino)
                return camino, g, nodos_expandidos
            
            
            vecinos = self.mapa.get_vecinos(actual)                     # Si no, miramos a sus vecinos
            for vecino in vecinos:
                coste_tramo = self.mapa.get_coste(actual, vecino)
                nuevo_g = g + coste_tramo
                
                
                if cerrada.contains(vecino) and cerrada.get_g(vecino) <= nuevo_g:
                    continue
                
                
                h = self.heuristica(vecino, destino)                    # Calculamos la prioridad f = g + h
                nuevo_f = nuevo_g + h
                
                # Lo añadimos a pendientes
                abierta.put(vecino, nuevo_f, nuevo_g, actual)
                
        
        return None, 0, nodos_expandidos                                # Si salimos del bucle, es que no hay camino posible

    def reconstruir_camino(self, padres, destino):  #Reconstruye la ruta yendo hacia atras desde el destino

        camino = []
        actual = destino

        while actual is not None:
            camino.append(actual)
            actual = padres.get(actual) # Buscamos a su padre


        return camino[::-1] # Le damos la vuelta a la lista