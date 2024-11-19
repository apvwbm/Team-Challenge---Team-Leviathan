import numpy as np
import random
import time
from clases import Tablero

# Imprimir mensaje en pantalla lentamente
def mensaje_lenta(mensaje, delay=0.15):
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
                mensaje_lenta("¡Prepárate para la batalla!")
                return True
            elif eleccion == "2":
                mensaje_lenta("Entendido, vuelve cuando tengas confianza.")
                return False
            else:
                mensaje_lenta("Comando inválido")
        except Exception as error_1:
            mensaje_lenta(
                "No te entendí, por favor pulsa una opción 1 o 2: ", error_1)


# Seleccionar dificultad del juego. Elegí 4 en lugar de las 3 sugeridas por el desafío,
# solo para que no sea idéntico al de los demás.
def seleccionar_dificultad():
    while True:
        mensaje_lenta("\nSelecciona el nivel de dificultad:")
        print("1. Fácil")
        print("2. Medio")
        print("3. Difícil")
        print("4. Exterminador")
        dificuldad = input("Seleccione una opción (1, 2, 3 o 4): ")

        try:
            if dificuldad in ["1", "2", "3", "4"]:
                return int(dificuldad)
            else:
                mensaje_lenta("Comando inválido")
        except ValueError:
            mensaje_lenta(
                "Entrada inválida. Por favor, seleccione una opción válida (1, 2, 3 o 4)")


# Función que define el turno del usuario. Es necesario verificar las salidas de los métodos de clase
# de barcos y tablero para redefinir las entradas y el procesamiento de datos, pero creo que la lógica es esa.
def turno_usuario(tablero_maquina, vidas_maquina):

    while True:           # "Se utilizó `While True` para controlar los turnos,
        # ya que quien acierta el barco tiene la oportunidad de jugar nuevamente hasta que falle."
        coordenadas = input(
            "Introduce las coordenadas para disparar (ejemplo: 3,4): ")
        try:
            fila, columna = [int(coord) for coord in coordenadas.split(",")]

            if (fila, columna) in tablero_maquina.posiciones_barcos_maquina:
                # Sustituir posiciones_barcos_maquina con los valores de la clase.

                mensaje_lenta(
                    "¡BOOOM! Objetivo alcanzado, buen disparo. Dispara de nuevo.")
                tablero_maquina.tablero_maquina[fila][columna] = "O"
                vidas_maquina -= 1
                if vidas_maquina == 0:
                    return True, vidas_maquina
            else:
                mensaje_lenta("¡Fallaste el objetivo, mejora tu puntería!")
                tablero_maquina.tablero_maquina[fila][columna] = "X"
                return False, vidas_maquina
        except ValueError:
            mensaje_lenta(
                "Coordenadas inválidas. Introduzca en el formato correcto (ejemplo: 3,4).")
        except IndexError:
            mensaje_lenta(
                "Coordenadas fuera de los límites del tablero. Introduzca valores entre 0 y 9.")
        except Exception as error_2:
            mensaje_lenta(
                "Error al procesar las coordenadas, por favor introduzca valores entre 0 y 9.: ", error_2)


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
            if (filas, columnas) in tablero_usuario.posiciones_barco_usuario:
                print("¡BOOOM! Parece que has sido alcanzado. Prepárate para la batalla")
                tablero_usuario.tablero_usuario[filas][columnas] = "O"
                vidas_usuario -= 1
                if vidas_usuario == 0:
                    # Si alcanza el barco devuelve True y encerra el bucle
                    return True, vidas_usuario
                break
            else:
                if i == intentos - 1:         # Si no alcanza el barco devuelve sigue intentando hasta que se terminen los intentos
                    print("PUUUUF. Qué suerte, ese ha pasado cerca.")
                tablero_usuario.tablero_usuario[filas][columnas] = "X"
        except IndexError:
            mensaje_lenta("Error: coordenadas fuera del tablero.")
        except Exception as error_3:
            mensaje_lenta(
                "Error al procesar el disparo de la máquina: ", error_3)
    return False, vidas_usuario


def juego_principal():

    menu_principal()

    dificultad_partida = seleccionar_dificultad()
    tablero_usuario = Tablero()
    tablero_maquina = Tablero()

    # vidas_usuario = 20
    # vidas_maquina = 20

    print("\nTablero del usuario:")
    tablero_usuario.mostrar_tablero(tablero_usuario.tablero_usuario)

    while vidas_usuario > 0 and vidas_maquina > 0:
        usuario_gana, vidas_maquina = turno_usuario(
            tablero_maquina, vidas_maquina)
        if usuario_gana:
            print("¡ENHORABUENA! Eres un maestro de la artillería. ¡Adelante!")
            break

        maquina_gana, vidas_usuario = turno_maquina(
            tablero_usuario, vidas_usuario, dificultad_partida)
        if maquina_gana:
            print("Capitán, nos estamos hundiendo. Esta vez no ha podido ser.")
            break
