from grafo import Grafo

# Intentamos cargar el mini mapa
mi_mapa = Grafo("test.gr", "test.co")

print("Probando lectura")
print(f"Vecinos del nodo 1: {list(mi_mapa.get_vecinos(1))}") # Debería salir [2, 3]
print(f"Coste de 1 a 2: {mi_mapa.get_coste(1, 2)}")           # Debera salir 100
print(f"Coordenadas del nodo 3: {mi_mapa.get_posicion(3)}")   # Debería salir (10, 10)