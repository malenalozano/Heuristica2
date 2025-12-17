import sys
import time  # <--- 1. AÑADIDO ESTO
from constraint import *

# Funcion auxiliar para ayuda en la impresion
def encuadrado(filas):
    n = len(filas)
    top = "+" + "-" * n + "+"
    body = "\n".join("|" + fila + "|" for fila in filas)
    return f"{top}\n{body}\n{top}"

def main():
    if len(sys.argv) != 3:
        print("Error, debes ejecutarlo con el siguiente formato: python parte-1.py entrada salida")
        return

    entrada = sys.argv[1] 
    salida = sys.argv[2] 

    try:
        with open(entrada, 'r') as f:
            lines = [l.strip() for l in f.readlines() if l.strip()]
            n = len(lines)
            if n % 2 != 0:
                print(f"Error: n={n} es impar.")
                return
            for i, line in enumerate(lines):
                if len(line) != n:
                    raise ValueError(f"Instancia no es NxN.")
    except FileNotFoundError:
        print("Error: No se encuentra el archivo de entrada.")
        return

    print(f"--- Resolviendo tablero de {n}x{n} ---") # <--- AÑADIDO PARA QUE SE VEA CLARO
    print(encuadrado(lines)) 

    p = Problem()
    
    for r in range(n):
        for c in range(n):
            char = lines[r][c].upper()
            if char == '.':
                p.addVariable((r, c), [0, 1])
            elif char == 'O':
                p.addVariable((r, c), [0])
            elif char == 'X':
                p.addVariable((r, c), [1])
            else:
                print("Error: Caracter invalodo")
                return

    target_sum = n // 2
    for i in range(n):
        p.addConstraint(ExactSumConstraint(target_sum), [(i, c) for c in range(n)])
        p.addConstraint(ExactSumConstraint(target_sum), [(r, i) for r in range(n)])

    def no_triple(a, b, c):
        return (a + b + c) != 0 and (a + b + c) != 3

    for r in range(n):
        for c in range(n - 2):
            p.addConstraint(no_triple, [(r, c), (r, c+1), (r, c+2)])
    for c in range(n):
        for r in range(n - 2):
            p.addConstraint(no_triple, [(r, c), (r+1, c), (r+2, c)])

    # --- ZONA MODIFICADA PARA LA CAPTURA ---
    print("Buscando soluciones (esto puede tardar)...")
    inicio = time.time()       # <--- Empezamos a cronometrar
    
    # IMPORTANTE: Para demostrar la "explosión", pedimos solo la primera solución en tableros grandes
    # Si pedimos TODAS en un 12x12 vacío, nunca acabará.
    # getSolution() devuelve UNA, getSolutions() devuelve TODAS.
    # Para tu prueba de estrés usamos getSolution() para ver si al menos encuentra una rápido.
    
    if n >= 8:
        # Si es muy grande, buscamos solo una para ver si es capaz
        solutions = [p.getSolution()] if p.getSolution() else []
    else:
        # Si es pequeño, buscamos todas
        solutions = p.getSolutions() 

    final = time.time()        # <--- Paramos cronómetro
    tiempo_total = final - inicio
    print(f"TIEMPO DE RESOLUCIÓN: {tiempo_total:.4f} segundos") # <--- IMPRIMIMOS EL DATO CLAVE
    # ---------------------------------------

    num_soluciones = len(solutions)
    if solutions and solutions[0] is None: num_soluciones = 0 # Ajuste por si getSolution devuelve None

    print(f"{num_soluciones} soluciones encontradas (o al menos 1 encontrada)")

    if num_soluciones > 0:
        solucion_final = solutions[0]
        solucion_rows = []
        for r in range(n):
            fila = ""
            for c in range(n):
                val = solucion_final[(r, c)]
                fila += "O" if val == 0 else "X"
            solucion_rows.append(fila)
        print(encuadrado(solucion_rows))
        
        with open(salida, 'w', encoding='utf-8') as f:
            f.write(encuadrado(lines) + "\n")
            f.write(encuadrado(solucion_rows) + "\n")
    else:
        print("No se encontro ninguna solución.")

if __name__ == "__main__":
    main()