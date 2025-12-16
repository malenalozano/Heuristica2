import math

class Grafo:
    def __init__(self, fichero_grafo, fichero_coordenadas):


        self.adyacencias = {} # Diccionario: ( nodo_origen: {nodo_destino: coste, etc) )
        self.coordenadas = {} # Diccionario: ( nodo_id: (longitud, latitud) )
        
        # Leemos los dos ficheros al arrancar
        self._leer_grafo(fichero_grafo)
        self._leer_coordenadas(fichero_coordenadas)

    def _leer_grafo(self, fichero):
        print(f"Cargando mapa (arcos) {fichero}")
        try:
            with open(fichero, 'r') as f:
                for linea in f: # El formato es a (origen) (destino) (coste)
                    
                    partes = linea.split()
                    if len(partes) >= 4 and partes[0] == 'a':
                        u = int(partes[1])
                        v = int(partes[2])
                        coste = int(partes[3])
                        
                        # Guardamos la carretera u -> v
                        if u not in self.adyacencias:
                            self.adyacencias[u] = {}
                        self.adyacencias[u][v] = coste
                        
        except FileNotFoundError:
            print(f"Error -> No encuentro el fichero {fichero}")

    def _leer_coordenadas(self, fichero):
        print(f"Cargando mapa (coordenadas) {fichero}")
        try:
            with open(fichero, 'r') as f:
                for linea in f: # El formato es v (id) (lon) (lat)
                    
                    partes = linea.split()
                    if len(partes) >= 4 and partes[0] == 'v':
                        nodo_id = int(partes[1])
                        
                        
                        lon = int(partes[2])
                        lat = int(partes[3])
                        self.coordenadas[nodo_id] = (lon, lat)
                        
        except FileNotFoundError:
            print(f"Error -> No encuentro el fichero {fichero}")
            
    
    #Metodos que usamos para el gps
    def get_vecinos(self, nodo): #Devuelvo todos los nodos a los que puedo ir desde Nodo
        
        return self.adyacencias.get(nodo, {}).keys()

    def get_coste(self, u, v): #Deulvo la distancia entre u y v
        
        return self.adyacencias.get(u, {}).get(v, float('inf'))

    def get_posicion(self, nodo): #Devuelco el lon y el lat (coordenadas) de un nodo
        
        return self.coordenadas.get(nodo, (0, 0))