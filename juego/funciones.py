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
        print(f"Valor de dificultad ingresado: {dificultad}")  # Verifique o valor aqui
        
        try:
            if dificultad in ["1", "2", "3", "4"]:
                return dificultad
            else:
                mensaje_lento("Comando inválido")
        except ValueError:
            mensaje_lento("Entrada inválida. Por favor, seleccione una opción válida (1, 2, 3 o 4)")


# Función que define el turno del usuario.
def turno_usuario(tablero_maquina, vidas_maquina):
    tablero_maquina.imprimir_tablero(mostrar_barcos=False, es_usuario=False)
    
    coordenadas = input("Introduce las coordenadas para disparar (ejemplo: 3,4): ")
    try:
        fila, columna = [int(coord) for coord in coordenadas.split(",")]
        resultado = tablero_maquina.disparo(fila, columna)

        if resultado == 0:  # Falló el objetivo
            mensaje_lento("¡Fallaste el objetivo, mejora tu puntería!")
            tablero_maquina.tablero_disparos[fila, columna] = SIMBOLOS["fallo"]
        elif resultado == 1:  # Alcanzó un barco
            mensaje_lento("¡BOOOM! Objetivo alcanzado, buen disparo.")
            tablero_maquina.tablero_disparos[fila, columna] = SIMBOLOS["impacto"]
            vidas_maquina -= 1  # Decrementa las vidas de la máquina
        elif resultado == 2:  # Ya disparó aquí
            mensaje_lento("Ya disparaste en esta posición.")
        elif resultado == 3:  # Barco hundido
            mensaje_lento("¡BOOOM! Barco hundido por la máquina.")
            vidas_maquina -= 1  # Decrementa las vidas de la máquina

    except ValueError:
        mensaje_lento("Coordenadas inválidas. Introduzca en el formato correcto (ejemplo: 3,4).")
    except IndexError:
        mensaje_lento("Coordenadas fuera de los límites del tablero. Introduzca valores entre 0 y 9.")
    except Exception as error_2:
        mensaje_lento("Error al procesar las coordenadas, por favor introduzca valores entre 0 y 9.", error_2)

    return vidas_maquina  # Retorna el valor actualizado de las vidas de la máquina


# Función que define el turno de la máquina.
def turno_maquina(tablero_usuario, vidas_usuario, dificultad):
    tablero_usuario.imprimir_tablero(mostrar_barcos=True, es_usuario=True)

    # Definir el número de intentos según la dificultad
    if dificultad == "1":
        intentos = 1
    elif dificultad == "2":
        intentos = 2
    elif dificultad == "3":
        intentos = 3
    elif dificultad == "4":
        intentos = 5
    else:
        mensaje_lento("Dificultad inválida, se asignará el valor predeterminado (1).")
        intentos = 1  # Asignando el valor predeterminado para intentos en caso de error

    #print(f"Dificultad seleccionada: {dificultad}, intentos asignados: {intentos}")

    ultimo_resultado = None  # Variable para registrar el último resultado de los intentos
    ultima_fila, ultima_columna = None, None  # Coordenadas del último disparo

    # Lista para almacenar las coordenadas ya disparadas
    coordenadas_disparadas = []

    for i in range(intentos):
        # Generar coordenadas aleatorias
        filas, columnas = random.randint(0, 9), random.randint(0, 9)

        # Verificar si las coordenadas ya han sido disparadas
        while (filas, columnas) in coordenadas_disparadas:
            filas, columnas = random.randint(0, 9), random.randint(0, 9)  # Generar nuevas coordenadas

        # Registrar las coordenadas disparadas para no repetirlas
        coordenadas_disparadas.append((filas, columnas))

        try:
            resultado = tablero_usuario.disparo(filas, columnas)
            ultimo_resultado = resultado  # Actualiza el último resultado
            ultima_fila, ultima_columna = filas, columnas  # Guarda las últimas coordenadas

            if resultado == 1:  # Alcanzó un barco
                mensaje_lento("¡BOOOM! Parece que has sido alcanzado. Prepárate para la batalla")
                vidas_usuario -= 1  
                break  # Detiene el bucle si acertó
            elif resultado == 0: 
                mensaje_lento("PUUUUF. Qué suerte, ese ha pasado cerca.")
            elif resultado == 3:  # Barco hundido
                mensaje_lento("¡BOOOM! Barco hundido por la máquina.")
                vidas_usuario -= 1
                break  # Detiene el bucle si hundió un barco

        except IndexError:
            mensaje_lento("Error: coordenadas fuera del tablero.")
        except Exception as error_3:
            mensaje_lento(f"Error al procesar el disparo de la máquina: {error_3}")

    # Marca el último resultado en el tablero
    if ultimo_resultado == 0:  # Fallo
        tablero_usuario.tablero[ultima_fila][ultima_columna] = SIMBOLOS["fallo"]
    elif ultimo_resultado == 1:  # Impacto
        tablero_usuario.tablero[ultima_fila][ultima_columna] = SIMBOLOS["impacto"]
    elif ultimo_resultado == 3:  # Barco hundido
        tablero_usuario.tablero[ultima_fila][ultima_columna] = SIMBOLOS["impacto"]

    return vidas_usuario  # Retorna el valor actualizado de las vidas del usuario