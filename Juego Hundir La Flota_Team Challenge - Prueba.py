import numpy as np
import time
from random import randint, choice

# VARIABLES ---------------------------------------------------------
TABLERO_DIMENSIONES = (10, 10)

BARCOS = {
    "portaaviones": (4, 1),
    "acorazados": (3, 2),
    "destructores": (2, 3),
    "submarinos": (1, 4)
}

SIMBOLOS = {
    "agua": "-",
    "barco": "B",
    "impacto": "X",
    "fallo": "O"
}

# FUNCIONES ---------------------------------------------------------


def mensaje_lenta(mensaje, delay=0.03):
    for caracter in mensaje:
        print(caracter, end='', flush=True)
        time.sleep(delay)
    print()


def menu_principal():
    while True:
        print("\nMenú Principal:")
        print("1. Jugar")
        print("2. Salir, aún no estoy preparado.")
        eleccion = input("Seleccione una opción (1 o 2): ")

        if eleccion == "1":
            mensaje_lenta("¡Prepárate para la batalla!")
            return True
        elif eleccion == "2":
            mensaje_lenta("Entendido, vuelve cuando tengas confianza.")
            return False
        else:
            mensaje_lenta("Comando inválido")


def seleccionar_dificultad():
    while True:
        mensaje_lenta("\nSelecciona el nivel de dificultad:")
        print("1. Fácil")
        print("2. Medio")
        print("3. Difícil")
        print("4. Exterminador")
        dificultad = input("Seleccione una opción (1, 2, 3 o 4): ")

        if dificultad in ["1", "2", "3", "4"]:
            return int(dificultad)
        else:
            mensaje_lenta("Comando inválido")


def turno_usuario(tablero_maquina, vidas_maquina):
    while True:
        coordenadas = input(
            "Introduce las coordenadas para disparar (ejemplo: 3,4): ")
        try:
            fila, columna = [int(coord) for coord in coordenadas.split(",")]

            if tablero_maquina.disparo(fila, columna) in [1, 3]:
                mensaje_lenta(
                    "¡BOOOM! Objetivo alcanzado, buen disparo. Dispara de nuevo.")
                vidas_maquina -= 1
                if vidas_maquina == 0:
                    return True, vidas_maquina
            else:
                mensaje_lenta("¡Fallaste el objetivo, mejora tu puntería!")
                return False, vidas_maquina
        except (ValueError, IndexError):
            mensaje_lenta("Coordenadas inválidas o fuera del tablero.")
        except Exception as e:
            mensaje_lenta(f"Error: {e}")


def turno_maquina(tablero_usuario, vidas_usuario, dificultad):
    intentos = dificultad

    for i in range(intentos):
        fila, columna = randint(0, 9), randint(0, 9)
        if tablero_usuario.disparo(fila, columna) in [1, 3]:
            print('¡Turno de máquina!')
            print("¡BOOOM! Parece que has sido alcanzado.")
            vidas_usuario -= 1
            if vidas_usuario == 0:
                return True, vidas_usuario
            break
        else:
            if i == intentos - 1:
                print('¡Turno de máquina!')
                print("PUUUUF. Qué suerte, ese ha pasado cerca.")
    return False, vidas_usuario

# CLASES ------------------------------------------------------------


class Tablero:
    def __init__(self, jugador_id, dimensiones, barcos):
        self.jugador_id = jugador_id
        self.dimensiones = dimensiones
        self.tablero = np.full(dimensiones, SIMBOLOS["agua"], dtype=str)
        self.barcos = []

        # Crear barcos
        for nombre, (eslora, cantidad) in barcos.items():
            for _ in range(cantidad):
                self.barcos.append(
                    {"nombre": nombre, "eslora": eslora, "posiciones": [], "hundido": False})

        # Calcular vidas como la suma de las esloras de todos los barcos
        self.vidas = sum(barco["eslora"] for barco in self.barcos)

    def posicionar_barcos(self):
        for barco in self.barcos:
            colocado = False
            while not colocado:
                fila, col = randint(
                    0, self.dimensiones[0] - 1), randint(0, self.dimensiones[1] - 1)
                orientacion = choice(["H", "V"])
                posiciones = self.generar_posiciones(
                    fila, col, barco["eslora"], orientacion)
                if self.validar_posiciones(posiciones):
                    self.colocar_barco(barco, posiciones)
                    colocado = True

    def generar_posiciones(self, fila, col, eslora, orientacion):
        if orientacion == "H":
            return [(fila, col + i) for i in range(eslora)]
        else:
            return [(fila + i, col) for i in range(eslora)]

    def validar_posiciones(self, posiciones):
        for fila, col in posiciones:
            if not (0 <= fila < self.dimensiones[0] and 0 <= col < self.dimensiones[1]):
                return False
            if self.tablero[fila, col] != SIMBOLOS["agua"]:
                return False
        return True

    def colocar_barco(self, barco, posiciones):
        barco["posiciones"] = posiciones
        for fila, col in posiciones:
            self.tablero[fila, col] = SIMBOLOS["barco"]

    def disparo(self, fila, col):
        for barco in self.barcos:
            if (fila, col) in barco["posiciones"]:
                barco["posiciones"].remove((fila, col))
                if not barco["posiciones"]:
                    barco["hundido"] = True
                return 3 if barco["hundido"] else 1
        return 0

    def imprimir_tablero(self, mostrar_barcos=False):
        for fila in self.tablero:
            print(" ".join(fila))


# JUEGO -------------------------------------------------------------
mensaje_lenta(
    "¡Bienvenido a Hundir la Flota! ¿Estás preparado para esta batalla?")

if menu_principal():
    dificultad_partida = seleccionar_dificultad()
    tablero_usuario = Tablero("Usuario", TABLERO_DIMENSIONES, BARCOS)
    tablero_maquina = Tablero("Máquina", TABLERO_DIMENSIONES, BARCOS)

    tablero_usuario.posicionar_barcos()
    tablero_maquina.posicionar_barcos()

    vidas_usuario = tablero_usuario.vidas
    vidas_maquina = tablero_maquina.vidas

    print("\nTablero del usuario:")
    tablero_usuario.imprimir_tablero(mostrar_barcos=True)

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
