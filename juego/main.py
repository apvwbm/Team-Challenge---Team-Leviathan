
from funciones import mensaje_lenta, menu_principal, seleccionar_dificultad, turno_usuario, turno_maquina

mensaje_lenta("¡Bienvenido a Hundir la Flota! ¿Estás preparado para esta batalla?")

menu_principal()

tablero_usuario = #Sustituir posiciones_barcos_maquina con los valores de la clase.
tablero_maquina = #Sustituir posiciones_barcos_maquina con los valores de la clase.

vidas_usuario = 20
vidas_maquina = 20
    
dificultad_partida = seleccionar_dificultad()
vidas_usuario = 20
vidas_maquina = 20

tablero_usuario = #Sustituir tablero_usuario con los valores de la clase.
tablero_maquina = #Sustituir tablero_maquina con los valores de la clase.

    
print("\nTablero del usuario:")
tablero_usuario.mostrar_tablero(tablero_usuario.tablero_usuario)
    
while vidas_usuario > 0 and vidas_maquina > 0:
    usuario_gana, vidas_maquina = turno_usuario(tablero_maquina, vidas_maquina)
    if usuario_gana:
        print("¡ENHORABUENA! Eres un maestro de la artillería. ¡Adelante!")
        break
        
    maquina_gana, vidas_usuario = turno_maquina(tablero_usuario, vidas_usuario, dificultad_partida)
    if maquina_gana:
        print("Capitán, nos estamos hundiendo. Esta vez no ha podido ser.")
        break