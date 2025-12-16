class Cerrada:
    def __init__(self):
        
        self.visitados = {} # Diccionario para guardar {nodo: coste_g_para_llegar_aqui}

    def add(self, nodo, g): #Marca un nodo como visitado con su coste g
        
        self.visitados[nodo] = g

    def contains(self, nodo):  #Comprueba si ya hemos visitado este nodo
        
        return nodo in self.visitados

    def get_g(self, nodo):   #Devuelve el coste con el que hemos visitado el nodo
        
        return self.visitados.get(nodo, float('inf'))