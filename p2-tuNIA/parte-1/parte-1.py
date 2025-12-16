import sys
from constraint import *



def encuadrado(filas):
    n = len(filas)
    top = "+" + "-" * n + "+"
    body = "\n".join("|" + fila + "|" for fila in filas)
    return f"{top}\n{body}\n{top}"

def main():
    #Verificamos los argumentos
    if len(sys.argv) != 3:
        print("Error, debes ejecutarlo con el siguiente formato: python parte-1.py entrada salida")
        return



    entrada = sys.argv[1] #archivo de entrada
    salida = sys.argv[2] #archivo de salida

    #leemos el trablero entero
    try:
        with open(entrada, 'r') as f:
            lines = [l.strip() for l in f.readlines() if l.strip()]

            n = len(lines)

            if n % 2 != 0:
                print(f"Error: n={n} es impar. No puede haber el mismo número de X y O por fila/columna.")
                return

            for i, line in enumerate(lines):
                if len(line) != n:
                    raise ValueError(f"Instancia no es NxN: fila {i} tiene longitud {len(line)} y n={n}.")
	#error de lectura
    except FileNotFoundError:
        print("Error: No se encuentra el archivo de entrada.")
        return

    
    
    print(encuadrado(lines)) #instancia original
    
    

    #redactamos las restricciones 
    p = Problem()
    
    for r in range(n):
        for c in range(n):

            #normalizado los carácteres por si hay errores

   
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
                #esto se puede hacer así?

    #Equilibrio (suma = n/2)
    target_sum = n // 2
    for i in range(n):
        p.addConstraint(ExactSumConstraint(target_sum), [(i, c) for c in range(n)])
        p.addConstraint(ExactSumConstraint(target_sum), [(r, i) for r in range(n)])

    #No puede haber triples
    def no_triple(a, b, c):
        return (a + b + c) != 0 and (a + b + c) != 3

    for r in range(n):
        for c in range(n - 2):
            p.addConstraint(no_triple, [(r, c), (r, c+1), (r, c+2)])
    for c in range(n):
        for r in range(n - 2):
            p.addConstraint(no_triple, [(r, c), (r+1, c), (r+2, c)])

    #Busqueda de soluciones
    
    solutions = p.getSolutions() 

    # Mostrar soluciones
    num_soluciones = len(solutions)
    print(f"{num_soluciones} soluciones encontradas")





    if num_soluciones > 0:
        # Guardamos solo la primera solucion
        solucion_final = solutions[0]
            
            
        solucion_rows = []
        for r in range(n):
            fila = ""
            for c in range(n):
                val = solucion_final[(r, c)]
                fila += "O" if val == 0 else "X"
            solucion_rows.append(fila)

            # imprimir SOLO una solución al final
        print(encuadrado(solucion_rows))
        
        
        with open(salida, 'w', encoding='utf-8') as f:
            f.write(encuadrado(lines) + "\n")
            f.write(encuadrado(solucion_rows) + "\n")
        
    else:
        print("No se encontro ninguna solución.")

if __name__ == "__main__":
    main()