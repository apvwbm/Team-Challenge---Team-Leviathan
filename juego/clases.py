import numpy as np


class Barco:
    def __init__(self, nombre, tamaño):
        self.nombre = nombre
        self.tamaño = tamaño
        self.barcos = {
            "Portaaviones": 4,
            "Crucero": 3,
            "Submarino": 3,
            "Fragata": 2,
            "Canoa": 1,
        }


class Tablero:
    def __init__(self, jugador_id, tamaño=10):
        self.jugador_id = jugador_id
        self.tamaño = tamaño
        self.tablero_invisible = np.zeros((tamaño, tamaño), dtype=int)
        self.tablero_juego = np.zeros((tamaño, tamaño)), dtype = int)
