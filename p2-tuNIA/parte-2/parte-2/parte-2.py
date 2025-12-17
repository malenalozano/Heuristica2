#Parte 2 de la segunda practica de la asignatura de Heurística. Ing.Inf

#Autores: Lucas Ruiz Y Malena Lozano


import sys
import time
from pathlib import Path
from grafo import Grafo
from algoritmo import AlgoritmoAEstrella




def main():

    # parte-2.py vertice 1 vertice 2 nombre del mapa fichero salida

    if len(sys.argv) != 5:
        print("Uso: python3 parte-2.py vertice1 vertice2 nombre del mapa fichero-salida")
        return


    #Comprobamos los valores pasados de los vertices
    origen_str = sys.argv[1]
    destino_str = sys.argv[2]

    origen = None
    destino = None

    if origen_str.isdigit():
        origen = int(origen_str)
    else:
        print("Error: vertice1 debe ser un entero")
        return

    if destino_str.isdigit():
        destino = int(destino_str)
    else:
        print("Error: vertice2 debe ser un entero")
        return



    mapa = sys.argv[3]
    archivosalida = sys.argv[4]



    fichero_grafo, fichero_coordenadas = nombre_a_rutas(mapa)
    
    if not fichero_grafo.exists():
        print(f"Error: no se encuentra el fichero de grafo: {fichero_grafo}")
        return
    if not fichero_coordenadas.exists():
        print(f"Error: no se encuentra el fichero de coordenadas: {fichero_coordenadas}")
        return
    

    archivo_salida_dir = dir_salida(archivosalida)

    num_vertices, num_arcos = contar_lineas(fichero_coordenadas, fichero_grafo)

    # Cargar grafo y resolver
    mapa = Grafo(str(fichero_grafo), str(fichero_coordenadas))
    solver = AlgoritmoAEstrella(mapa)

    t0 = time.time()
    camino, coste, expandidos = solver.resolver(origen, destino)
    t1 = time.time()
    tiempo_total = t1 - t0

    # Salida por pantalla (formato del enunciado)
    print(f"Vertices --> {num_vertices}")
    print(f"Arcos --> {num_arcos}")

    if camino:

        print(f"Solución óptima encontrada con coste {coste}")

        #Al ser valores tan pequeños queremos sacar muchos decimales para el tiempo de ejecucion

        print(f"Tiempo de ejecucion: {tiempo_total:.6f} segundos")


        if tiempo_total > 0:
            rate = expandidos / tiempo_total
        else:
            rate = 0.0


        #Sacamos 6 decimales aquí meramente por tema de consistencia
        print(f"Expansiones : {expandidos} ({rate:.6f} nodes/sec)")

        # Escribir fichero salida con costes de arcos
        costes = costes_arcos(fichero_grafo, camino)

        escribirsolucion(archivo_salida_dir, camino, costes)


    else:

        with open(archivo_salida_dir, "w") as f:
            f.write("")
        print("No se encontró ningún camino entre estos dos puntos")



def nombre_a_rutas(mapa: str):

    mapa_path = Path(mapa)

    # Si no se ha puesto carpeta, asumimos que esta en la misma carpeta del archivo de python
    if not mapa_path.parent or str(mapa_path.parent) == ".":
        mapa_path = Path(__file__).parent / mapa_path

    fichero_grafo = str(mapa_path) + ".gr"
    fichero_coordenadas = str(mapa_path) + ".co"

    return Path(fichero_grafo), Path(fichero_coordenadas)


def dir_salida(archivosalida: str):

    p = Path(archivosalida)


    #Si no se ha especificado una carpeta lo guardamos donde el archivo de python
    if str(p.parent) == ".":       

        p = Path(__file__).parent / p 

    return p


def contar_lineas(fichero_coordenadas: Path, fichero_grafo: Path):

    vertices = 0
    arcos = 0

    #Abrimos y leemos el numero de vertices
    with open(fichero_coordenadas, "r") as f:

        for line in f:

            if line.startswith("v "):

                vertices += 1


    #Abrimos y leemos el numero de arcos
    with open(fichero_grafo, "r") as f:

        for line in f:

            if line.startswith("a "):

                arcos += 1

    return vertices, arcos


def costes_arcos(fichero_grafo: Path, path: list[int]):

    # Si la ruta tiene 0 o 1 nodo no hay arcos
    if len(path) < 2:
        return {}

    # Diccionario de arcos que necesitamos: (u,v) --> True
    arcos_necesitados = {}

    for i in range(len(path) - 1):
        u = path[i]                             #ORIGEN
        v = path[i + 1]                         #DESTINO
        arcos_necesitados[(u, v)] = True        #Guardamos una entrada en el dic. con esta clave

    costes = {}

    with open(fichero_grafo, "r") as f:

        for linea in f:
            if not linea.startswith("a "):
                continue

            #Separamos la linea
            parts = linea.split()

            #ORIGEN
            u = int(parts[1])

            #DESTINO
            v = int(parts[2])

            #COSTE
            w = int(parts[3])

            if (u, v) in arcos_necesitados:
                costes[(u, v)] = w

                # Si ya hemos encontrado todos, paramos
                if len(costes) == len(arcos_necesitados):
                    break

    return costes


def escribirsolucion(ruta_salida: Path, camino: list[int], costes: dict[tuple[int, int], int]):

    # Si no hay camino, dejamos el fichero vacio
    if not camino:

        with open(ruta_salida, "w") as f:

            f.write("")

        return

    partes = [str(camino[0])]  # empezamos por el nodo inicial

    for i in range(len(camino) - 1):

        origen = camino[i]
        destino = camino[i + 1]

        coste = costes.get((origen, destino))

        if coste is None:

            raise ValueError(f"No se encontró el coste del arco {origen} -> {destino} en el .gr")

        partes.append(f"({coste})")
        partes.append(str(destino))

    with open(ruta_salida, "w") as f:
        f.write(" - ".join(partes) + "\n")



if __name__ == "__main__":
    main()
