from funciones import mensaje_lento, menu_principal, seleccionar_dificultad, turno_usuario, turno_maquina
from variables import TABLERO_DIMENSIONES, BARCOS
from clases import Tablero

mensaje_lento("¡Bienvenido a Hundir la Flota! ¿Estás preparado para esta batalla?")

while True:
    if not menu_principal():
        break

    dificultad = seleccionar_dificultad()

    tablero_usuario = Tablero("Usuario", TABLERO_DIMENSIONES, BARCOS)
    tablero_maquina = Tablero("Máquina", TABLERO_DIMENSIONES, BARCOS)

    tablero_usuario.posicionar_barcos()
    tablero_maquina.posicionar_barcos()

    vidas_usuario = tablero_usuario.vidas
    vidas_maquina = tablero_maquina.vidas

    tablero_usuario.imprimir_tablero(mostrar_barcos=True)

    while vidas_usuario > 0 and vidas_maquina > 0:
        vidas_maquina = turno_usuario(tablero_maquina, vidas_maquina, tablero_usuario)
        print(f"Vidas restantes de la máquina: {vidas_maquina}")

        if vidas_maquina == 0:
            mensaje_lento("¡ENHORABUENA! Eres un maestro de la artillería. ¡Adelante!")
            break

        vidas_usuario = turno_maquina(tablero_usuario, vidas_usuario, dificultad)
        print(f"Vidas restantes del usuario: {vidas_usuario}")

        if vidas_usuario == 0:
            mensaje_lento("Capitán, nos estamos hundiendo. Esta vez no ha podido ser.")
            break