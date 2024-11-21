import numpy as np
from random import randint, choice
from variables import SIMBOLOS

class Barco:
    def __init__(self, nombre, eslora):
        self.nombre = nombre
        self.eslora = eslora
        self.posiciones = []
        self.hundido = False

    def colocar(self, posiciones):
        self.posiciones = posiciones

    def recibir_disparo(self, fila, col):
        if (fila, col) in self.posiciones:
            self.posiciones.remove((fila, col))
            if len(self.posiciones) == 0:
                self.hundido = True
            return True
        return False


class Tablero:
    def __init__(self, jugador_id, dimensiones, barcos):
        self.jugador_id = jugador_id
        self.dimensiones = dimensiones if isinstance(dimensiones, tuple) else (dimensiones, dimensiones)
        self.tablero = np.full(self.dimensiones, SIMBOLOS["agua"], dtype=str)
        self.tablero_disparos = np.full(self.dimensiones, SIMBOLOS["agua"], dtype=str)
        self.barcos = []
        for nombre, (eslora, cantidad) in barcos.items():
            for _ in range(cantidad):
                self.barcos.append(Barco(nombre, eslora))
        self.vidas = sum(barco.eslora for barco in self.barcos)

    def posicionar_barcos(self):
        for barco in self.barcos:
            colocado = False
            while not colocado:
                x = randint(0, self.dimensiones[0] - 1)
                y = randint(0, self.dimensiones[1] - 1)
                orientacion = choice(["H", "V"])
                posiciones = self.generar_posiciones(x, y, barco.eslora, orientacion)
                if self.validar_posiciones(posiciones):
                    self.colocar_barco(barco, posiciones)
                    colocado = True

    def generar_posiciones(self, fila, col, eslora, orientacion):
        posiciones = []
        if orientacion == "H":
            for i in range(eslora):
                posiciones.append((fila, col + i))
        elif orientacion == "V":
            for i in range(eslora):
                posiciones.append((fila + i, col))
        return posiciones

    def validar_posiciones(self, posiciones):
        for fila, col in posiciones:
            if fila < 0 or fila >= self.dimensiones[0] or col < 0 or col >= self.dimensiones[1]:
                return False
            if self.tablero[fila, col] != SIMBOLOS["agua"]:
                return False
        return True

    def colocar_barco(self, barco, posiciones):
        barco.colocar(posiciones)
        for fila, col in posiciones:
            self.tablero[fila, col] = SIMBOLOS["barco"]

    def disparo(self, fila, col):
        if self.tablero_disparos[fila, col] != SIMBOLOS["agua"]:
            return 2

        for barco in self.barcos:
            if barco.recibir_disparo(fila, col):
                self.tablero[fila, col] = SIMBOLOS["impacto"]
                self.tablero_disparos[fila, col] = SIMBOLOS["impacto"]
                self.vidas -= 1
                if barco.hundido:
                    return 3
                return 1

        self.tablero[fila, col] = SIMBOLOS["fallo"]
        self.tablero_disparos[fila, col] = SIMBOLOS["fallo"]
        return 0

    def imprimir_tablero(self, mostrar_barcos=False, es_usuario=True):
        tablero_a_exibir = self.tablero if mostrar_barcos else self.tablero_disparos
        if es_usuario:
            print("Tablero del Usuario:")
        else:
            print("Tablero de la Máquina:")
        for fila in tablero_a_exibir:
            print(" ".join(fila))
        print()
