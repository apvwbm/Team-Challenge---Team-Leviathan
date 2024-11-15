# variables.py

# Dimensiones del tablero
TABLERO_DIMENSIONES = (10, 10)

# Num de barcos y su eslora
BARCOS = {
    "portaaviones": (4, 1),   # Eslora, cantidad
    "acorazados": (3, 2),     # Eslora, cantidad
    "destructores": (2, 3),   # Eslora, cantidad
    "submarinos": (1, 4)      # Eslora, cantidad
}

# Símbolos en el tablero
SIMBOLOS = {
    "agua": "-",
    "barco": "B",
    "impacto": "X",
    "fallo": "O"
}
