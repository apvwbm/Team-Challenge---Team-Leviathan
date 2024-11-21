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
        self.dimensiones = dimensiones if isinstance(dimensiones, tuple) else (dimensiones, dimensiones)
        self.tablero = np.full(self.dimensiones, SIMBOLOS["agua"], dtype=str)
        self.tablero_disparos = np.full(self.dimensiones, SIMBOLOS["agua"], dtype=str)
        self.barcos = []
        
        # Crear los barcos según la estructura de BARCOS
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
                posiciones = self.generar_posiciones(x, y, barco.eslora, orientacion)
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
        if orientacion == "H":
            return [(fila, col + i) for i in range(eslora)]
        else:
            return [(fila + i, col) for i in range(eslora)]

    def validar_posiciones(self, posiciones):
        """
        Verifica si las posiciones generadas son válidas para colocar un barco.

        Args:
            posiciones (list): Lista de tuplas con las coordenadas (fila, columna).

        Returns:
            bool: True si las posiciones son válidas, False si no lo son.
        """
        for fila, col in posiciones:
            if not (0 <= fila < self.dimensiones[0] and 0 <= col < self.dimensiones[1]):
                return False
            if self.tablero[fila, col] != SIMBOLOS["agua"]:
                return False
        return True

    def colocar_barco(self, barco, posiciones):
        """
        Coloca un barco en las posiciones indicadas.

        Args:
            barco (Barco): Objeto de la clase Barco.
            posiciones (list): Lista de tuplas con las coordenadas (fila, columna).
        """
        barco.colocar(posiciones)
        for fila, col in posiciones:
            self.tablero[fila, col] = SIMBOLOS["barco"]

    def disparo(self, fila, col):
        """
        Verifica si un disparo impacta en cualquiera de los barcos del jugador (self).

        Args:
            fila (int): Coordenada de la fila para disparar.
            col (int): Coordenada de la columna para disparar.

        Returns:
            int: Código del resultado del disparo.
                - 0: Disparo en agua.
                - 1: Impacto en un barco.
                - 2: Disparo a una casilla ya atacada.
                - 3: Hundimiento de un barco.
        """
        if self.tablero_disparos[fila, col] != SIMBOLOS["agua"]:
            return 2  # Ya disparado

        for barco in self.barcos:
            if barco.recibir_disparo(fila, col):
                self.tablero[fila, col] = SIMBOLOS["impacto"]
                self.tablero_disparos[fila, col] = SIMBOLOS["impacto"]
                self.vidas -= 1
                return 1 if not barco.hundido else 3  # Impacto o Hundido

        self.tablero[fila, col] = SIMBOLOS["fallo"]
        self.tablero_disparos[fila, col] = SIMBOLOS["fallo"]
        return 0  # Agua


    def imprimir_tablero(self, mostrar_barcos=False, es_usuario=True):
        
        #Control booleano para mostrar los barcos del usuario y omitir 
        # las posiciones de los barcos de la máquina, mostrando solo los disparos.

        tablero_a_exibir = self.tablero if mostrar_barcos else self.tablero_disparos
    
        if es_usuario:
            print("Tablero del Usuario:")
        else:
            print("Tablero de la Máquina:")
    
        for fila in tablero_a_exibir:
            print(" ".join(fila))
        print()