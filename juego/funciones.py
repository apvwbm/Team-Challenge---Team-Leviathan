# funciones.py
import numpy as np
import random
import time
from clases import Tablero, Barco
from variables import SIMBOLOS


def mensaje_lento(mensaje, delay=0.01):             # Imprimir mensaje en pantalla lentamente
    for caracter in mensaje:
        print(caracter, end='', flush=True)
        time.sleep(delay)
    print()

# Menú de selección del juego optimizado con Try/Except para control de errores
def menu_principal():                               
    while True:
        print("\nMenú Principal:")
        print("1. Jugar")
        print("2. Salir, aún no estoy preparado.")
        eleccion = input("Seleccione una opción (1 o 2): ")
        
        try:
            if eleccion == "1":
                mensaje_lento("¡Prepárate para la batalla!")
                return True
            elif eleccion == "2":
                mensaje_lento("Entendido, vuelve cuando tengas confianza.")
                return False
            else:
                mensaje_lento("Comando inválido")
        except Exception as error_1:
            mensaje_lento("No te entendí, por favor pulsa una opción 1 o 2: ", error_1)

# Seleccionar dificultad del juego. Elegí 4 en lugar de las 3 sugeridas por el desafío,
# solo para que no sea idéntico al de los demás.
def seleccionar_dificultad():
    while True:
        mensaje_lento("\nSelecciona el nivel de dificultad:")
        print("1. Fácil")
        print("2. Medio")
        print("3. Difícil")
        print("4. Exterminador")
        dificultad = input("Seleccione una opción (1, 2, 3 o 4): ")
        
        try:
            if dificultad in ["1", "2", "3", "4"]:
                return int(dificultad)
            else:
                mensaje_lento("Comando inválido")
        except ValueError:
            mensaje_lento("Entrada inválida. Por favor, seleccione una opción válida (1, 2, 3 o 4)")


# Función que define el turno del usuario. Es necesario verificar las salidas de los métodos de clase 
# de barco y tablero para redefinir las entradas y el procesamiento de datos, pero creo que la lógica es esa.
def turno_usuario(tablero_maquina, vidas_maquina):

    while True: # Se utilizó `While True` para controlar los turnos, 
                # ya que quien acierta el barco tiene la oportunidad de jugar nuevamente hasta que falle.
        coordenadas = input("Introduce las coordenadas para disparar (ejemplo: 3,4): ")
        try:
            fila, columna = [int(coord) for coord in coordenadas.split(",")]

            if (fila, columna) in tablero_maquina.barcos:      
                                                  #Sustituir posiciones_barcos_maquina con los valores de la clase.
            
                mensaje_lento("¡BOOOM! Objetivo alcanzado, buen disparo. Dispara de nuevo.")
                tablero_maquina.tablero[fila][columna] = "O"
                vidas_maquina -= 1
                if vidas_maquina == 0:
                    return True, vidas_maquina
            else:
                mensaje_lento("¡Fallaste el objetivo, mejora tu puntería!")
                tablero_maquina.tablero[fila][columna] = "X"
                return False, vidas_maquina
        except ValueError:
            mensaje_lento("Coordenadas inválidas. Introduzca en el formato correcto (ejemplo: 3,4).")
        except IndexError:
            mensaje_lento("Coordenadas fuera de los límites del tablero. Introduzca valores entre 0 y 9.")
        except Exception as error_2:
            mensaje_lento("Error al procesar las coordenadas, por favor introduzca valores entre 0 y 9.: ", error_2)


# Función que define el turno de la maquina con la dificultad de la partida 
# en base a la elección realizada en el menú. Lo único que cambia es el número 
# de intentos que tiene la máquina para acertar el barco.
def turno_maquina(tablero_usuario, vidas_usuario, dificultad):
    if dificultad == "1":
        intentos = 1
    elif dificultad == "2":
        intentos = 2
    elif dificultad == "3":
        intentos = 3
    if dificultad == "4":
        intentos = 5 

    for i in range(intentos):
        filas, columnas = random.randint(0, 9), random.randint(0, 9)
        try:
            if (filas, columnas) in tablero_usuario.barcos:   # JY: Se modifico barco en vez de barcos
                print("¡BOOOM! Parece que has sido alcanzado. Prepárate para la batalla")
                tablero_usuario.tablero[filas][columnas] = "O"
                vidas_usuario -= 1
                if vidas_usuario == 0:
                    return True, vidas_usuario          # Si alcanza el barco devuelve True y encerra el bucle
                break
            else:
                if i == intentos - 1:         # Si no alcanza el barco devuelve sigue intentando hasta que se terminen los intentos
                    print("PUUUUF. Qué suerte, ese ha pasado cerca.")
                tablero_usuario.tablero[filas][columnas] = "X"
        except IndexError:
            mensaje_lento("Error: coordenadas fuera del tablero.")
        except Exception as error_3:
            mensaje_lento("Error al procesar el disparo de la máquina: ", error_3)
    return False, vidas_usuario