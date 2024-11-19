from funciones import mensaje_lenta, menu_principal, seleccionar_dificultad, turno_usuario, turno_maquina
from variables import TABLERO_DIMENSIONES, BARCOS
from clases import Tablero

mensaje_lenta("¡Bienvenido a Hundir la Flota! ¿Estás preparado para esta batalla?")

menu_principal()

dificultad_partida = seleccionar_dificultad()

tablero_usuario = Tablero("Usuario", TABLERO_DIMENSIONES, BARCOS)
tablero_maquina = Tablero("Maquina", TABLERO_DIMENSIONES, BARCOS)

vidas_usuario = 20
vidas_maquina = 20
    
print("\nTablero del usuario:")
tablero_usuario.imprimir_tablero(mostrar_barcos=True)
    
while vidas_usuario > 0 and vidas_maquina > 0:
    usuario_gana, vidas_maquina = turno_usuario(tablero_maquina, vidas_maquina)
    if usuario_gana:
        print("¡ENHORABUENA! Eres un maestro de la artillería. ¡Adelante!")
        break
        
    maquina_gana, vidas_usuario = turno_maquina(tablero_usuario, vidas_usuario, dificultad_partida)
    if maquina_gana:
        print("Capitán, nos estamos hundiendo. Esta vez no ha podido ser.")
        break

menu_principal()