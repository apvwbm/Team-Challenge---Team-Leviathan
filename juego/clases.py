# clases.py
import numpy as np
from random import randint, choice
from variables import SIMBOLOS


class Barco:
    def __init__(self, nombre, eslora):
        self.nombre = nombre
        self.eslora = eslora
        self.posiciones = []  # Guarda las coordenadas ocupadas por el barco
        self.hundido = False

    def colocar(self, posiciones):
        self.posiciones = posiciones

    def recibir_disparo(self, fila, col):
        if (fila, col) in self.posiciones:
            self.posiciones.remove((fila, col))

            if not self.posiciones:
                self.hundido = True
            return True
        else:
            return False


class Tablero:
    def __init__(self, jugador_id, dimensiones, barcos):
        self.jugador_id = jugador_id
        self.dimensiones = dimensiones if isinstance(
            dimensiones, tuple) else (dimensiones, dimensiones)
        self.tablero = np.full(self.dimensiones, SIMBOLOS["agua"], dtype=str)
        self.tablero_disparos = np.full(
            self.dimensiones, SIMBOLOS["agua"], dtype=str)
        self.barcos = []

        # Crear los barcos según la estructura de BARCOS (en variables.py)
        for nombre, (eslora, cantidad) in barcos.items():
            for _ in range(cantidad):
                self.barcos.append(Barco(nombre, eslora))

        # Sumar todas las vidas
        self.vidas = sum(barco.eslora for barco in self.barcos)

    def posicionar_barcos(self):
        """
        Posiciona los barcos en el tablero de forma aleatoria.

        Comentario:
            La función recorre la lista de barcos y, para cada uno, genera posiciones aleatorias
            hasta encontrar una que sea válida. Luego, coloca el barco en esas posiciones.
        """
        for barco in self.barcos:
            colocado = False
            while not colocado:
                x = randint(0, self.dimensiones[0] - 1)
                y = randint(0, self.dimensiones[1] - 1)
                orientacion = choice(["H", "V"])
                posiciones = self.generar_posiciones(
                    x, y, barco.eslora, orientacion)
                if self.validar_posiciones(posiciones):
                    self.colocar_barco(barco, posiciones)
                    colocado = True

    def generar_posiciones(self, fila, col, eslora, orientacion):
        """
        Genera las posiciones que ocupará un barco en el tablero.

        Args:
            fila (int): Fila inicial del barco.
            col (int): Columna inicial del barco.
            eslora (int): Longitud del barco.
            orientacion (str): Orientación del barco ("H" = horizontal, "V" = vertical).

        Returns:
            list: *Lista de tuplas* con las coordenadas (fila, columna) que ocupará el barco. Por ejemplo, [(X, Y), (X, Y), (X, Y)].
        """
        pass  # Implementar

    def validar_posiciones(self, posiciones):
        """
        Verifica si las posiciones generadas son válidas para colocar un barco.

        Args:
            posiciones (list): Lista de tuplas con las coordenadas (fila, columna).

        Returns:
            bool: True si las posiciones son válidas, False si no lo son.
        """
        pass  # Implementar

    def colocar_barco(self, barco, posiciones):
        """
        Coloca un barco en las posiciones indicadas.

        Args:
            barco (Barco): Objeto de la clase Barco.
            posiciones (list): Lista de tuplas con las coordenadas (fila, columna).
        """
        pass  # Implementar

    def disparo(self, fila, col):
        """
        Verifica si un disparo impacta en cualquiera de los barcos del jugador (self).

        Args:
            fila (int): _description_
            col (int): _description_

        Returns:
            int: 0 si cae en agua, 1 si hay impacto en un barco, 2 si dispara a una casilla ya disparada.
        """
        pass  # Implementar

    def imprimir_tablero(self, mostrar_barcos=False):
        print(self.tablero if mostrar_barcos else self.tablero_disparos)
