# main.py
from clases import Tablero
from funciones import elegir_dificultad, pedir_coordenadas, generar_coordenadas_aleatorias
from variables import *

def main():
    print("¡Bienvenido a Hundir la Flota!")
    
    # Elegir dificultad
    dificultad = elegir_dificultad()

    # Inicializar tableros
    tablero_jugador = Tablero(jugador_id="Jugador", dimensiones=TABLERO_DIMENSIONES, barcos=BARCOS)
    tablero_maquina = Tablero(jugador_id="Máquina", dimensiones=TABLERO_DIMENSIONES, barcos=BARCOS)

    tablero_jugador.inicializar_tablero()
    tablero_maquina.inicializar_tablero()

    while True:
        # Turno del jugador
        while True:
            print("\nTu turno! Elige una opción:")
            print("1. Disparar")
            print("2. Ver tu tablero")
            print("3. Ver el tablero enemigo")
            print("4. Salir del juego")
            opcion = input("Elige una opción: ")

            if opcion == "1":
                fila, col = pedir_coordenadas()
                disparo = tablero_maquina.disparo(fila, col)
                if disparo == 1:  # Impacto
                    print("¡Impacto!")
                    if tablero_maquina.vidas == 0:
                        print("¡Felicidades! Hundiste todos los barcos enemigos.")
                        return
                    # Después de un impacto, vuelve a pedir coordenadas sin mostrar el menú
                    continue
                elif disparo == 2:  # Ya disparado
                    print("Ya has disparado antes a esta casilla. Inténtalo de nuevo.")
                    continue  # Vuelve a pedir coordenadas sin romper el ciclo
                else:  # Agua
                    print("¡Agua!")
                    break  # Sale del ciclo de disparos y vuelve al menú de opciones

            elif opcion == "2":
                print("\nTu tablero:")
                tablero_jugador.imprimir_tablero(mostrar_barcos=True)
            elif opcion == "3":
                print("\nTablero enemigo:")
                tablero_maquina.imprimir_tablero()
            elif opcion == "4":
                print("Saliendo del juego...")
                return
            else:
                print("Opción no válida. Inténtalo de nuevo.")

        # Turno de la máquina
        disparos_realizados = 0
        impactos = 0
        print("\nTurno de la máquina.")
        while disparos_realizados < dificultad:
            fila, col = generar_coordenadas_aleatorias()
            disparo = tablero_jugador.disparo(fila, col)

            if disparo == 1:  # Impacto
                impactos += 1
                disparos_realizados += 1  # Solo incrementa los disparos si hubo impacto
            elif disparo == 2:  # Ya disparado
                continue  # Vuelve a disparar
            else:  # Agua
                disparos_realizados += 1  # Incrementa el turno de disparo aunque falle

        # Al final del turno de la máquina, mostramos el resumen
        if impactos > 0:
            print(f"La máquina disparó {disparos_realizados} veces e impactó {impactos}.")
        else:
            print("La máquina falló todos sus disparos.")
        
        # Verifica si la máquina ganó
        if tablero_jugador.vidas == 0:
            print("¡Perdiste! La máquina hundió todos tus barcos.")
            return

if __name__ == "__main__":
    main()
