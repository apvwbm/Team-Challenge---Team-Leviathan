from funciones import mensaje_lento, menu_principal, seleccionar_dificultad, turno_usuario, turno_maquina
from variables import TABLERO_DIMENSIONES, BARCOS
from clases import Tablero

mensaje_lento("¡Bienvenido a Hundir la Flota! ¿Estás preparado para esta batalla?")

menu_principal()

dificultad_partida = seleccionar_dificultad()

tablero_usuario = Tablero("Usuario", TABLERO_DIMENSIONES, BARCOS)
tablero_maquina = Tablero("Maquina", TABLERO_DIMENSIONES, BARCOS)

tablero_usuario.posicionar_barcos()
tablero_maquina.posicionar_barcos()

vidas_usuario = 20
vidas_maquina = 20
    
print("\nTablero del usuario:")
tablero_usuario.imprimir_tablero(mostrar_barcos=True)
    
while vidas_usuario > 0 and vidas_maquina > 0:
    vidas_maquina = turno_usuario(tablero_maquina, vidas_maquina)
    print(f"Vidas restantes de la máquina: {vidas_maquina}")  # Mostrar las vidas después del turno de la máquina

    if vidas_maquina == 0:
        print("¡ENHORABUENA! Eres un maestro de la artillería. ¡Adelante!")
        break
    
    vidas_usuario = turno_maquina(tablero_usuario, vidas_usuario, dificultad_partida)
    print(f"Vidas restantes del usuario: {vidas_usuario}")  # Mostrar las vidas después del turno de la máquina

    if vidas_usuario == 0:
        print("Capitán, nos estamos hundiendo. Esta vez no ha podido ser.")
        break
1
menu_principal()