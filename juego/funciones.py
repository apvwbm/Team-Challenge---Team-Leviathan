import time
from random import randint
from variables import SIMBOLOS

def mensaje_lento(mensaje, delay=0.0):
    for caracter in mensaje:
        print(caracter, end='', flush=True)
        time.sleep(delay)
    print()

def menu_principal():
    while True:
        print("\nMenú Principal:")
        print("1. Jugar")
        print("2. Salir")
        eleccion = input("Seleccione una opción (1 o 2): ")
        if eleccion == "1":
            mensaje_lento("¡Prepárate para la batalla!")
            return True
        elif eleccion == "2":
            mensaje_lento("Entendido, vuelve cuando tengas confianza.")
            return False
        else:
            mensaje_lento("Comando inválido, intenta de nuevo.")
            
def mostrar_menu_turno(tablero_usuario, tablero_maquina):
    while True:
        print("\nOpciones:")
        print("1. Disparar")
        print("2. Mostrar tablero del jugador")
        print("3. Mostrar tablero de la máquina")
        print("4. Salir del juego")
        opcion = input("Elige una opción (1-4): ")

        if opcion == "1":
            return "disparar"
        elif opcion == "2":
            tablero_usuario.imprimir_tablero(mostrar_barcos=True, es_usuario=True)
        elif opcion == "3":
            tablero_maquina.imprimir_tablero(mostrar_barcos=False, es_usuario=False)
        elif opcion == "4":
            mensaje_lento("Saliendo del juego. ¡Hasta pronto!")
            exit()
        else:
            mensaje_lento("Opción inválida. Intenta de nuevo.")

def seleccionar_dificultad():
    while True:
        mensaje_lento("\nSelecciona el nivel de dificultad:")
        print("1. Fácil")
        print("2. Medio")
        print("3. Difícil")
        print("4. Extremo")
        print("5. Derrota asegurada")
        dificultad = input("Seleccione una opción (1, 2, 3, 4 o 5): ")
        if dificultad in ["1", "2", "3", "4", "5"]:
            return dificultad
        else:
            mensaje_lento("Comando inválido, por favor elige un número entre 1 y 4.")

def turno_usuario(tablero_maquina, vidas_maquina, tablero_usuario):
    while True:
        accion = mostrar_menu_turno(tablero_usuario, tablero_maquina)
        if accion == "disparar":
            break

    tablero_maquina.imprimir_tablero(mostrar_barcos=False, es_usuario=False)
    while True:
        try:
            # Pedimos del 1 - 10 para que sea más fácil para el usuario
            fila = int(input("Introduce la fila (1-10): "))
            columna = int(input("Introduce la columna (1-10): "))

            # Convertimos a coordenadas internas del programa (0-9)
            fila -= 1
            columna -= 1

            if not (0 <= fila < 10 and 0 <= columna < 10):
                mensaje_lento("Coordenadas fuera del rango. Por favor, introduce valores entre 1 y 10.")
                continue  # Repite el turno

            resultado = tablero_maquina.disparo(fila, columna)

            if resultado == 0:
                mensaje_lento("¡Agua! ¡Mejora esa puntería!")
                break
            elif resultado == 1:
                mensaje_lento("Les hemos dado, buen disparo.")
                vidas_maquina -= 1
            elif resultado == 2:
                mensaje_lento("Ya has disparado en esta posición. Inténtalo de nuevo.")
            elif resultado == 3:
                mensaje_lento("¡BOOOM! Has hundido un barco!.")
                vidas_maquina -= 1
            if resultado in [1, 3]:  # Repite turno si acierta
                continue
        except ValueError:
            mensaje_lento("Entrada inválida. Por favor, introduce números enteros entre 1 y 10.")
    return vidas_maquina

def turno_maquina(tablero_usuario, vidas_usuario, dificultad):
    intentos = {
        "1": 1,
        "2": 3,
        "3": 5,
        "4": 10,
        "5": 25,
    }.get(dificultad, 1)

    acierto = False
    hundido = False

    for _ in range(intentos):
        valido = False
        while not valido:
            filas, columnas = randint(0, 9), randint(0, 9)

            # Verificar si la posición ya fue disparada
            if tablero_usuario.tablero_disparos[filas, columnas] == SIMBOLOS["agua"]:
                valido = True  # Coordenada válida encontrada

        # Realizar el disparo en una posición válida
        resultado = tablero_usuario.disparo(filas, columnas)
        if resultado == 0:
            continue  # La máquina sigue intentando
        elif resultado == 1:
            acierto = True
            vidas_usuario -= 1  # Resta vidas por impacto
        elif resultado == 3:
            acierto = True
            hundido = True
            vidas_usuario -= 1  # Resta vidas por impacto y hundimiento
            break  # La máquina deja de disparar si hunde un barco
        
    # Mensajes finales
    if acierto:
        if hundido:
            mensaje_lento("¡BOOOM! Barco hundido por la máquina.")
        else:
            mensaje_lento("¡BOOOM! Parece que has sido alcanzado. Prepárate para la batalla.")
    else:
        mensaje_lento("PUUUUF. Qué suerte, ese ha pasado cerca.")

    # Mostrar el tablero actualizado inmediatamente
    tablero_usuario.imprimir_tablero(mostrar_barcos=True, es_usuario=True)

    return vidas_usuario