# funciones.py
import random

def pedir_coordenadas():
    while True:
        try:
            fila = int(input("Introduce la fila (1-10): ")) - 1
            columna = int(input("Introduce la columna (1-10): ")) - 1
            if 0 <= fila < 10 and 0 <= columna < 10:
                return fila, columna
            else:
                print("Coordenadas inválidas. Deben estar entre 1 y 10.")
        except ValueError:
            print("Entrada inválida. Por favor, introduce números enteros.")

def elegir_dificultad():
    while True:
        try:
            dificultad = int(input("Elige la dificultad de la máquina (1-3): "))
            if 1 <= dificultad <= 10:
                return dificultad
            else:
                print("Por favor, elige una dificultad entre 1 y 3.")
        except ValueError:
            print("Entrada inválida. Por favor, introduce un número entero.")

def generar_coordenadas_aleatorias():
    return random.randint(0, 9), random.randint(0, 9)
