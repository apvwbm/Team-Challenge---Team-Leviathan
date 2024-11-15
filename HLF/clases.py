# clases.py
import numpy as np
from random import randint, choice
from variables import SIMBOLOS

class Tablero:
    def __init__(self, jugador_id, dimensiones, barcos):
        self.jugador_id = jugador_id
        self.dimensiones = dimensiones if isinstance(dimensiones, tuple) else (dimensiones, dimensiones)
        self.barcos = barcos
        self.tablero = np.full(self.dimensiones, SIMBOLOS["agua"], dtype=str)
        self.tablero_disparos = np.full(self.dimensiones, SIMBOLOS["agua"], dtype=str)
        self.vidas = sum([eslora * cantidad for eslora, cantidad in barcos.values()])

    def inicializar_tablero(self, aleatorio=True):
        if aleatorio:
            self.posicionar_barcos()
        else:
            pass # Implementar colocación manual
            
    def posicionar_barcos(self):
        for nombre, (eslora, cantidad) in self.barcos.items():  # Desempaqueta eslora y cantidad
            for i in range(cantidad):
                colocado = False
                while not colocado:  # Intenta hasta colocar el barco correctamente
                    x = randint(0, self.dimensiones[0] - 1)
                    y = randint(0, self.dimensiones[1] - 1)
                    orientacion = choice(["H", "V"])
                    if self.validar_posicion(x, y, eslora, orientacion):
                        self.colocar_barco(x, y, eslora, orientacion)
                        colocado = True

    def validar_posicion(self, fila, col, eslora, orientacion):
        if orientacion == "H":
            if col + eslora > self.dimensiones[1]:
                return False
            return all(self.tablero[fila, col + i] == SIMBOLOS["agua"] for i in range(eslora))
        elif orientacion == "V":
            if fila + eslora > self.dimensiones[0]:
                return False
            return all(self.tablero[fila + i, col] == SIMBOLOS["agua"] for i in range(eslora))

    def colocar_barco(self, fila, col, eslora, orientacion):
        for i in range(eslora):
            if orientacion == "H":
                self.tablero[fila, col + i] = SIMBOLOS["barco"]
            else:
                self.tablero[fila + i, col] = SIMBOLOS["barco"]

    def disparo(self, fila, col):
        if self.tablero[fila, col] == SIMBOLOS["barco"]:
            self.tablero[fila, col] = SIMBOLOS["impacto"]
            self.tablero_disparos[fila, col] = SIMBOLOS["impacto"]
            self.vidas -= 1
            return 1  # Impacto
        elif self.tablero[fila, col] == SIMBOLOS["impacto"] or self.tablero_disparos[fila, col] == SIMBOLOS["fallo"]:
            return 2 # Ya disparado
        else:
            self.tablero[fila, col] = SIMBOLOS["fallo"]
            self.tablero_disparos[fila, col] = SIMBOLOS["fallo"]
            return False  # Agua

    def imprimir_tablero(self, mostrar_barcos=False):
        print(self.tablero if mostrar_barcos else self.tablero_disparos)