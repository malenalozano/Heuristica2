import sys
import time
from grafo import Grafo
from algoritmo import AlgoritmoAEstrella

def main():
    # comprobacion de arguemntos
    if len(sys.argv) != 5:
        print("Error")
        print("Por favor ejectue el comando de esta manera: python parte-2.py grafo.gr coords.co origen destino")
        return

    print(f"Calculando ruta de {origen} a {destino}")


	#cargamos los argumentos	
    fichero_grafo = sys.argv[1]
    fichero_coordenadas = sys.argv[2]
    origen = int(sys.argv[3])
    destino = int(sys.argv[4])

    

    
    map = Grafo(fichero_grafo, fichero_coordenadas) #Cargamos el mapa
    gps = AlgoritmoAEstrella(map) #Inicializamos el algoritmo

    inicio = time.time() #Medimos el tiempo y ejecutamos
    camino, coste, expandidos = gps.resolver(origen, destino)
    final = time.time()
    
    tiempototal = final - inicio

    #Imprimimos resultados
    if camino:
        print(f"Ruta encontrada: {' -> '.join(map(str, camino))}")
        print(f"Coste total: {coste}")
        print(f"Nodos expandidos: {expandidos}")
        print(f"Tiempo: {tiempototal:.4f} segundos")
    else:
        print("No se encontro ningún camino entre esos dos puntos")

if __name__ == "__main__":
    main()