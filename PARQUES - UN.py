import random
import pygame
import tkinter
from tkinter import messagebox
from tkinter import simpledialog

# --------------------- variables globales

# tablero
tablero = []

# variable para saber si hay un ganador
ganador = False

# variables para guardar el valor de los dados
valor_d1 = -1
valor_d2 = -1

# mapa de las casillas especiales, ya sean salidas, seguros, etc.
casillas_especiales = {}

# variable para controlar el jugador actual en la partida
jugador_actual = -1

# variables que controlan la cantidad de fichas en la carcel que tiene cada jugador
carcel_1 = 4
carcel_2 = 4
carcel_3 = 4
carcel_4 = 4

# variables que controlan la cantidad de fichas que han ganado por cada jugador
ganadores_1 = 0
ganadores_2 = 0
ganadores_3 = 0
ganadores_4 = 0

# mapa que guarda el color de cada jugador
color_jugador = {}

# mapa que guarda el color de la salida de cada jugador
color_salidas = {}

# variable que guarda el color de los seguros
color_seguro = (255, 194, 102)

# variable que guarda el color del fondo
color_fondo = (242, 242, 242)

# variable que guarda el color de los bordes de las casillas
color_borde = (0, 0, 0)

# variable que guarda el color de un dado seleccionado
color_seleccionado = (255, 0, 0)

# variable que guarda el color que indica si un dado se movió automaticamente
color_mov_auto = (0, 0, 255)

# variable que controla el tamaño de la celda en pixeles
tam_celda = 40

# variable que indica si el jugador actual puede lanzar los dados
puede_lanzar = True

# variable que indica si el jugador actual tiene seleccionado el dado 1 o 2
select_d1 = False
select_d2 = False

# variable que indica si el jugador actual puede usar el dado 1 o 2
puede_mover_d1 = False
puede_mover_d2 = False

# variable que indica el dado 1 o 2 fue usado automaticamente
auto_d1 = False
auto_d2 = False

# variable para controlar que se haya salido correctamente del popup para ingresar el valor de los dados como desarrollador
popup_salida_exitosa = False

# mapa que guarda el nombre de los jugadores
nombres_jugadores = {}

# --------------------- funciones

def iniciar_juego():
    """Inicializa todas las variables necesarias para reiniciar el juego"""
    global tablero, carcel_1, carcel_2, carcel_3, carcel_4, jugador_actual, valor_d1, valor_d2, puede_lanzar, puede_mover_d1, puede_mover_d2, select_d1, select_d2, popup_salida_exitosa, auto_d1, auto_d2, nombres_jugadores, ganador, ganadores_1, ganadores_2, ganadores_3, ganadores_4
    jugador_actual = 1
    ganador = False
    carcel_1 = 4
    carcel_2 = 4
    carcel_3 = 4
    carcel_4 = 4
    ganadores_1 = 0
    ganadores_2 = 0
    ganadores_3 = 0
    ganadores_4 = 0
    valor_d1 = -1
    valor_d2 = -1
    puede_lanzar = True
    select_d1 = False
    select_d2 = False
    puede_mover_d1 = False
    puede_mover_d2 = False
    auto_d1 = False
    auto_d2 = False
    popup_salida_exitosa = False
    nombres_jugadores = {}
    # cada "*" es una casilla que en la que una ficha puede moverse
    tablero = [[['*'] for i in range(19)] for i in range(19)]
    crear_esquinas()
    crear_centro()
    llenar_casillas_especiales()
    llenar_colores()

def crear_esquinas():
    """Crea las esquinas vacias en la matriz para que la ficha vaya por el camino correcto"""
    for i in range(0, 64):
        # esquina superior izquierda
        tablero[i//8][i%8] = ['']
        # esquina superior derecha
        tablero[i//8][len(tablero)-1-i%8] = ['']
        # esquina inferior izquierda
        tablero[len(tablero)-1-i//8][i%8] = ['']
        # esquina inferior derecha
        tablero[len(tablero)-1-i//8][len(tablero)-1-i%8] = ['']

def crear_centro():
    """Crea el centro vacio en la matriz para que la ficha vaya por el camino correcto"""
    for i in range(-1, 2):
        for j in range(-1, 2):
            tablero[9+i][9+j] = ['']

def lanzar_dados(dev = False, d1 = 0, d2 = 0):
    """Asigna el valor a los dados ya sea por un lanzamiento o por asignacion en el modo desarrollador
    Args:
        dev (bool): Para determinar si es lanzamiento en modo desarrollador o no
        d1 (int): Valor del dado 1
        d2 (int): Valor del dado 2
    """
    global valor_d1, valor_d2, puede_lanzar, puede_mover_d1, puede_mover_d2, auto_d1, auto_d2
    puede_lanzar = False
    puede_mover_d1 = False
    puede_mover_d2 = False
    auto_d1 = False
    auto_d2 = False
    if dev == False:
        valor_d1 = random.randint(1,6)
        valor_d2 = random.randint(1,6)
    else:
        valor_d1 = d1
        valor_d2 = d2

def llenar_casillas_especiales():
    """Asigna las casillas especiales, ya sean seguros, salidas, etc."""
    global casillas_especiales
    casillas_especiales['Seg'] = [(9,0),(9,18),(0,9),(18,9),(14,8),(10,14),(4,10),(8,4),(10,4),(14,10),(8,14),(4,8)]
    # salidas
    casillas_especiales['S1'] = [(10,4)]
    casillas_especiales['S2'] = [(14,10)]
    casillas_especiales['S3'] = [(8,14)]
    casillas_especiales['S4'] = [(4,8)]
    # carcel
    casillas_especiales['C1'] = [(14,3),(14,4),(15,3),(15,4)]
    casillas_especiales['C2'] = [(14,14),(14,15),(15,14),(15,15)]
    casillas_especiales['C3'] = [(3,14),(3,15),(4,14),(4,15)]
    casillas_especiales['C4'] = [(3,3),(3,4),(4,3),(4,4)]
    # nombre jugador
    casillas_especiales['N1'] = [(16,3)]
    casillas_especiales['N2'] = [(16,14)]
    casillas_especiales['N3'] = [(5,14)]
    casillas_especiales['N4'] = [(5,3)]
    # casilla donde las fichas giran para la "recta final"
    casillas_especiales['F1'] = [(9,0)]
    casillas_especiales['F2'] = [(18,9)]
    casillas_especiales['F3'] = [(9,18)]
    casillas_especiales['F4'] = [(0,9)]
    # casillas donde la ficha ya gana
    casillas_especiales['Fin'] = [(9,8),(8,9),(9,10),(10,9)]

def llenar_colores():
    """Asigna el color a jugadores y salidas de jugadores"""
    color_jugador[1] = (255, 255, 0)
    color_jugador[2] = (255, 0, 0)
    color_jugador[3] = (0, 255, 0)
    color_jugador[4] = (0, 0, 255)
    color_salidas['S1'] = (255, 255, 204)
    color_salidas['S2'] = (255, 204, 204)
    color_salidas['S3'] = (204, 255, 204)
    color_salidas['S4'] = (204, 204, 255)

def salir():
    """Saca una ficha de la carcel dependiendo del jugador actual"""
    global tablero, carcel_1, carcel_2, carcel_3, carcel_4, select_d1, select_d2
    select_d1 = False
    select_d2 = False
    if jugador_actual == 1:
        carcel_1 -= 1
    if jugador_actual == 2:
        carcel_2 -= 1
    if jugador_actual == 3:
        carcel_3 -= 1
    if jugador_actual == 4:
        carcel_4 -= 1
    # obtiene la casilla donde debe salir la ficha
    casilla_salida = casillas_especiales['S'+str(jugador_actual)][0]
    # pregunta si en la casilla hay un jugador, ya sea del mismo equipo o de otro
    if len(tablero[casilla_salida[0]][casilla_salida[1]]) > 1:
        por_eliminar = 0
        jugador_eliminar = 0
        for objeto in tablero[casilla_salida[0]][casilla_salida[1]]:
            if objeto != '*' and objeto != jugador_actual:
                jugador_eliminar = objeto
                por_eliminar = tablero[casilla_salida[0]][casilla_salida[1]].count(objeto)
                break
        if jugador_eliminar == 1:
            carcel_1 += por_eliminar
        if jugador_eliminar == 2:
            carcel_2 += por_eliminar
        if jugador_eliminar == 3:
            carcel_3 += por_eliminar
        if jugador_eliminar == 4:
            carcel_4 += por_eliminar
        if jugador_eliminar != 0:
            for i in range(tablero[casilla_salida[0]][casilla_salida[1]].count(jugador_eliminar)):
                tablero[casilla_salida[0]][casilla_salida[1]].remove(jugador_eliminar)
    # pone el jugador en el lugar de salida
    tablero[casilla_salida[0]][casilla_salida[1]].append(jugador_actual)

def mover(cantidad, x, y):
    """Mueve una ficha, dada la cantidad de casillas que debe mover y la posicion de la ficha
    Args:
        cantidad (int): Cantidad de fichas a mover, 0<=cantidad<=6
        x (int): Posicion x de la matriz de la ficha a mover
        y (int): Posicion y de la matriz de la ficha a mover
    """
    global tablero, carcel_1, carcel_2, carcel_3, carcel_4, ganadores_1, ganadores_2, ganadores_3, ganadores_4, select_d1, select_d2, puede_lanzar, auto_d1, auto_d2, ganador
    puede_lanzar = False
    select_d1 = False
    select_d2 = False
    esquina1 = False
    esquina2 = False
    esquina3 = False
    esquina4 = False
    # variable para guardar la posicion inicial x de la ficha
    ini_x = x
    # variable para guardar la posicion inicial y de la ficha
    ini_y = y
    # variable para guardar la ultima posicion x en donde estuvo la ficha
    ant_x = [0]
    # variable para guardar la ultima posicion y en donde estuvo la ficha
    ant_y = [0]
    # preguntar si esta en una "recta final" horizontal y no puede moverse porque es un numero muy grande
    if x == 9:
        if y < 9:
            if not ('*' in tablero[x][y+cantidad] or (x, y+cantidad) in casillas_especiales['Fin']) or y+cantidad > 9:
                auto_d1 = False
                auto_d2 = False
                return
        if y > 9:
            if not ('*' in tablero[x][y-cantidad] or (x, y-cantidad) in casillas_especiales['Fin']) or y-cantidad < 9:
                auto_d1 = False
                auto_d2 = False
                return
    # preguntar si esta en una "recta final" vertical y no puede moverse porque es un numero muy grande
    if y == 9:
        if x < 9:
            if not ('*' in tablero[x+cantidad][y] or (x+cantidad, y) in casillas_especiales['Fin']) or x+cantidad > 9:
                auto_d1 = False
                auto_d2 = False
                return
        if x > 9:
            if not ('*' in tablero[x-cantidad][y] or (x-cantidad, y) in casillas_especiales['Fin']) or x-cantidad < 9:
                auto_d1 = False
                auto_d2 = False
                return
    while cantidad > 0:
        cantidad-=1
        ant_x.append(x)
        ant_y.append(y)
        # movimiento si esta en una casilla donde debe moverse hacia la derecha
        if x == 10:
            if y+1 < len(tablero) and '*' in tablero[x][y+1]:
                y += 1
            elif y+1 == len(tablero):
                x -= 1
            else:
                esquina1 = True
        # movimiento si esta en una casilla donde debe moverse hacia la izquierda
        elif x == 8:
            if y-1 >= 0 and '*' in tablero[x][y-1]:
                y -= 1
            elif y-1 < 0:
                x += 1
            else:
                esquina3 = True
        # movimiento si esta en una casilla donde debe moverse hacia abajo
        elif y == 8:
            if x+1 < len(tablero) and '*' in tablero[x+1][y]:
                x += 1
            elif x+1 == len(tablero):
                y += 1
            else:
                esquina4 = True
        # movimiento si esta en una casilla donde debe moverse hacia arriba
        elif y == 10:
            if x-1 >= 0 and '*' in tablero[x-1][y]:
                x -= 1
            elif x-1 < 0:
                y -= 1
            else:
                esquina2 = True
        # movimiento si esta en una casilla final y pregunta si es la casilla final del jugador
        elif x == 0:
            casilla_final = casillas_especiales['F'+str(jugador_actual)][0]
            if casilla_final[0] == x and casilla_final[1] == y:
                x += 1
                continue
            y -= 1
        # movimiento si esta en una casilla final y pregunta si es la casilla final del jugador
        elif y == 0:
            casilla_final = casillas_especiales['F'+str(jugador_actual)][0]
            if casilla_final[0] == x and casilla_final[1] == y:
                y += 1
                continue
            x += 1
        # movimiento si esta en una casilla final y pregunta si es la casilla final del jugador
        elif x == len(tablero)-1:
            casilla_final = casillas_especiales['F'+str(jugador_actual)][0]
            if casilla_final[0] == x and casilla_final[1] == y:
                x -= 1
                continue
            y += 1
        # movimiento si esta en una casilla final y pregunta si es la casilla final del jugador
        elif y == len(tablero)-1:
            casilla_final = casillas_especiales['F'+str(jugador_actual)][0]
            if casilla_final[0] == x and casilla_final[1] == y:
                y -= 1
                continue
            x -= 1
        # movimiento si esta en una "recta final" horizontal
        elif x == 9:
            if y < 9:
                y += 1
            if y > 9:
                y -= 1
        # movimiento si esta en una "recta final" vertical
        elif y == 9:
            if x < 9:
                x += 1
            if x > 9:
                x -= 1

        # movimiento si esta en una esquina del trayecto
        if esquina1:
            esquina1 = False
            y += 1
            x += 1
        elif esquina2:
            esquina2 = False
            y += 1
            x -= 1
        elif esquina3:
            esquina3 = False
            y -= 1
            x -= 1
        elif esquina4:
            esquina4 = False
            y -= 1
            x += 1
        
        # rompe el bucle si encuentra un bloqueo y lo deja en la posicion anterior
        if len(tablero[x][y]) == 3:
            for i in range(len(ant_x)-1,-1,-1):
                if len(tablero[ant_x[i]][ant_y[i]]) < 3:
                    x = ant_x[i]
                    y = ant_y[i]
                    break
            break

    # preguntar si la ficha no se movió
    if x == 0 and y == 0:
        return

    casilla_final = (x, y)

    # quitar el jugador de la casilla inicial
    tablero[ini_x][ini_y].remove(jugador_actual)

    # preguntar si quedo en una casilla de fin para marcar la ficha como ganadora
    if casilla_final in casillas_especiales['Fin']:
        if jugador_actual == 1:
            ganadores_1 += 1
        if jugador_actual == 2:
            ganadores_2 += 1
        if jugador_actual == 3:
            ganadores_3 += 1
        if jugador_actual == 4:
            ganadores_4 += 1
        # mostrar un mensaje si el jugador gano
        if ganadores_1 == 4 or ganadores_2 == 4 or ganadores_3 == 4 or ganadores_4 == 4:
            texto = f"El jugador {jugador_actual} ha ganado, presione 'R' para volver a jugar."
            if jugador_actual in nombres_jugadores:
                texto = f"El jugador {nombres_jugadores[jugador_actual]} ({jugador_actual}) ha ganado, presione 'R' para volver a jugar."
            messagebox.showinfo("Ganador", texto)
            ganador = True
        return

    # preguntar si hay fichas en la casilla de llegada y si no es un seguro
    if len(tablero[x][y]) > 1 and casilla_final not in casillas_especiales['Seg']:
        por_eliminar = 0
        jugador_eliminar = 0
        for objeto in tablero[x][y]:
            if objeto != '*' and objeto != jugador_actual:
                jugador_eliminar = objeto
                por_eliminar = tablero[x][y].count(objeto)
                break
        if jugador_eliminar == 1:
            carcel_1 += por_eliminar
        if jugador_eliminar == 2:
            carcel_2 += por_eliminar
        if jugador_eliminar == 3:
            carcel_3 += por_eliminar
        if jugador_eliminar == 4:
            carcel_4 += por_eliminar
        if jugador_eliminar != 0:
            for i in range(tablero[x][y].count(jugador_eliminar)):
                tablero[x][y].remove(jugador_eliminar)

    tablero[x][y].append(jugador_actual)

def verificar_salir():
    """Verifica si un jugador puede salir, ya sea por bloqueo, o porque no tiene un 5 o indicar que se salio automaticamente con un 5 que tenga el jugador
    Returns:
        bool
    """
    global puede_mover_d1, puede_mover_d2, puede_lanzar, jugador_actual, auto_d1, auto_d2
    casilla_salida = casillas_especiales['S'+str(jugador_actual)][0]
    if tablero[casilla_salida[0]][casilla_salida[1]].count(jugador_actual) == 2:
        return
    if valor_d1 == 5:
        salir()
        puede_mover_d2 = True
        auto_d1 = True
    elif valor_d2 == 5:
        salir()
        puede_mover_d1 = True
        auto_d2 = True
    elif valor_d1 + valor_d2 == 5:
        salir()
        auto_d1 = True
        auto_d2 = True
    else:
        puede_lanzar = True
        jugador_actual += 1
        if jugador_actual == 5:
            jugador_actual = 1
        return False
    return True

def encontrar_jugador(jugador):
    """Dado un jugador retorna su posicion
    Args:
        jugador (int): Numero del jugador
    Returns:
        tuple"""
    for x in range(len(tablero)):
        for y in range(len(tablero)):
            if jugador in tablero[x][y]:
                return (x, y)
    return (0, 0)

def contar_fichas_jugador(jugador):
    """Dado un jugador cuenta cuantas fichas tiene en el tablero
    Args:
        jugador (int): Numero del jugador
    Returns:
        int"""
    total = 0
    for x in range(len(tablero)):
        for y in range(len(tablero)):
            if jugador in tablero[x][y]:
                total += tablero[x][y].count(jugador)
    return total

def verificar_auto():
    """Verifica si la ficha puede moverse automaticamente, de ser asi la mueve"""
    global auto_d1, auto_d2, puede_mover_d1, puede_mover_d2
    if auto_d1:
        puede_mover_d1 = False
    if auto_d2:
        puede_mover_d2 = False
    if contar_fichas_jugador(jugador_actual) == 1:
        if not(ganadores_1 == 3 and carcel_1 == 0) and ((valor_d1 == 5 and not auto_d1) or (valor_d2 == 5 and not auto_d2)):
            return
        casilla_jugador = encontrar_jugador(jugador_actual)
        if casilla_jugador != (0,0):
            if puede_mover_d1:
                auto_d1 = True
                puede_mover_d1 = False
                mover(valor_d1, casilla_jugador[0], casilla_jugador[1])
            casilla_jugador = encontrar_jugador(jugador_actual)
            if puede_mover_d2:
                auto_d2 = True
                puede_mover_d2 = False
                mover(valor_d2, casilla_jugador[0], casilla_jugador[1])

def asignar_nombre(jugador):
    """Abre una ventana para asignarle nombre al jugador actual"""
    root = tkinter.Tk()
    root.withdraw()
    nombre = simpledialog.askstring("Nombre", f"Elegir nombre para el jugador {jugador}:")
    if nombre is not None:
        nombres_jugadores[jugador_actual] = nombre

def abrir_dialogo_dados():
    """Abre una ventana para el lanzamiento de dados como desarrollador"""
    root = tkinter.Tk()
    root.withdraw()

    dialogo = tkinter.Toplevel()
    dialogo.geometry("300x150")
    dialogo.resizable(False, False)
    dialogo.title("Ingresar Valores Dados")
    dialogo.protocol("WM_DELETE_WINDOW", root.destroy)

    dialogo.grid_rowconfigure(0, weight=1)
    dialogo.grid_rowconfigure(1, weight=1)
    dialogo.grid_rowconfigure(2, weight=1)
    dialogo.grid_columnconfigure(0, weight=1)
    dialogo.grid_columnconfigure(1, weight=1)

    tkinter.Label(dialogo, text="Dado 1:").grid(row=0, column=0)
    entrada1 = tkinter.Entry(dialogo)
    entrada1.grid(row=0, column=1)

    tkinter.Label(dialogo, text="Dado 2:").grid(row=1, column=0)
    entrada2 = tkinter.Entry(dialogo)
    entrada2.grid(row=1, column=1)

    def guardar_datos():
        global valor_d1, valor_d2, popup_salida_exitosa
        if not entrada1.get().isnumeric() or not entrada2.get().isnumeric():
            messagebox.showerror("Error", "Valores no validos")
            return
        d1 = int(entrada1.get())
        d2 = int(entrada2.get())
        if d1<1 or d1>6 or d2<1 or d2>6:
            messagebox.showerror("Error", "Valores no validos")
            return
        valor_d1 = d1
        valor_d2 = d2
        popup_salida_exitosa = True
        dialogo.destroy()
        root.destroy()

    boton = tkinter.Button(dialogo, text="Guardar", command=guardar_datos)
    boton.grid(row=2, columnspan=2)

    dialogo.grab_set()
    root.mainloop()

iniciar_juego()

pygame.init()

fuente_dados = pygame.font.Font(None, 30)

pantalla = pygame.display.set_mode(((len(tablero)+3) * tam_celda, len(tablero) * tam_celda))
pygame.display.set_caption("Parqués UN")

ejecutando = True
# bucle infinito hasta que cierre el programa, para refrescar pantalla y ejecutar el juego
while ejecutando:
    pantalla.fill(color_fondo)

    # control de eventos para detectar si se cierra o si oprime una tecla
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        
        # detectar si se oprime el clic izquierdo del mouse
        if evento.type == pygame.MOUSEBUTTONDOWN:
            # desactiva los eventos si ya el juego terminó
            if ganador:
                continue
            x, y = evento.pos

            columna = x // tam_celda
            fila = y // tam_celda

            # pregunta si se le hizo clic a un jugador o a un dado
            if 0 <= fila < len(tablero) and 0 <= columna < len(tablero) and len(tablero[fila][columna])>1:
                if jugador_actual in tablero[fila][columna]:
                    if select_d1 == True:
                        puede_mover_d1 = False
                        mover(valor_d1,fila,columna)
                    if select_d2 == True:
                        puede_mover_d2 = False
                        mover(valor_d2,fila,columna)
                    if not (puede_mover_d1 or puede_mover_d2):
                        puede_lanzar = True
                        jugador_actual += 1
                        if jugador_actual == 5:
                            jugador_actual = 1

            if fila == 1 and columna == 20 and puede_mover_d1:
                select_d1 = True
                select_d2 = False

            if fila == 3 and columna == 20 and puede_mover_d2:
                select_d2 = True
                select_d1 = False
        
        # eventos para teclado
        if evento.type == pygame.KEYDOWN:
            tecla_presionada = pygame.key.name(evento.key)
            # si oprime r reinicia el juego
            if tecla_presionada == "r":
                iniciar_juego()
            # desactiva los eventos si ya el juego terminó
            if ganador:
                continue
            # si oprime l lanza los dados
            if tecla_presionada == "l" and puede_lanzar:
                lanzar_dados()
                sale = True
                if contar_fichas_jugador(jugador_actual) == 0:
                    sale = verificar_salir()
                if sale:
                    puede_mover_d1 = True
                    puede_mover_d2 = True
                    verificar_auto()
                    if not (puede_mover_d1 or puede_mover_d2):
                        puede_lanzar = True
                        jugador_actual += 1
                        if jugador_actual == 5:
                            jugador_actual = 1
            # si oprime d lanza los dados como desarrollador
            if tecla_presionada == "d" and puede_lanzar:
                popup_salida_exitosa = False
                abrir_dialogo_dados()
                if not popup_salida_exitosa:
                    puede_lanzar = True
                    continue
                auto_d1 = False
                auto_d2 = False
                sale = True
                if contar_fichas_jugador(jugador_actual) == 0:
                    sale = verificar_salir()
                if sale:
                    puede_mover_d1 = True
                    puede_mover_d2 = True
                    verificar_auto()
                    if not (puede_mover_d1 or puede_mover_d2):
                        puede_lanzar = True
                        jugador_actual += 1
                        if jugador_actual == 5:
                            jugador_actual = 1
            # si oprime s saca una ficha de la carcel
            if tecla_presionada == "s":
                casilla_salida = casillas_especiales['S'+str(jugador_actual)][0]
                if tablero[casilla_salida[0]][casilla_salida[1]].count(jugador_actual) == 2 or (not select_d1 and not select_d2):
                    continue
                if select_d1 == True and valor_d1 == 5:
                    salir()
                    puede_mover_d1 = False
                if select_d2 == True and valor_d2 == 5:
                    salir()
                    puede_mover_d2 = False
                verificar_auto()
                if not (puede_mover_d1 or puede_mover_d2):
                    puede_lanzar = True
                    jugador_actual += 1
                    if jugador_actual == 5:
                        jugador_actual = 1
            # si oprime n le asigna nombre al jugador actual
            if tecla_presionada == "n":
                asignar_nombre(jugador_actual)
            # si oprime p salta un turno, solo para pruebas
            if tecla_presionada == "p":
                puede_lanzar = True
                jugador_actual += 1
                if jugador_actual == 5:
                    jugador_actual = 1
            # si oprime h muestra la ayuda
            if tecla_presionada == "h":
                messagebox.showinfo("Ayuda", "Bienvenido a Parqués UN.\nAl lado derecho de la pantalla en la esquina superior derecha verá cuales son los valores de los dados despues de lanzarlos, si aparece un -1 es porque es el primer turno y nadie ha lanzado antes, si un numero aparece en azul es porque se uso automaticamente ya que no habian mas opciones, si un numero aparece en rojo es porque ya se usó ese dado por el jugador o porque no es posible usarlo.\n\nPara lanzar los dados presione la tecla 'L'.\nPara elegir los valores de los dados presione la tecla 'D' (solo se puede hacer si no ha movido).\nSi desea saltar un turno presione la tecla 'P'.\nSi desea usar un dado para salir en vez de moverse presione la tecla 'S'.\nSi desea reiniciar el juego presione la tecla 'R'.")

    cont_carcel_1 = 0
    cont_carcel_2 = 0
    cont_carcel_3 = 0
    cont_carcel_4 = 0

    # dibujar la matriz
    for fila in range(len(tablero)):
        for col in range(len(tablero)):
            x = col * tam_celda
            y = fila * tam_celda
            
            centro_x = x + tam_celda // 2
            centro_y = y + tam_celda // 2
            
            centro1_x = x + tam_celda // 2
            centro1_y = y + tam_celda // 4
            
            centro2_x = x + tam_celda // 2
            centro2_y = y + (tam_celda // 4) * 3

            # dibuja los bordes de la casilla donde el jugador puede moverse
            if '*' in tablero[fila][col]:
                pygame.draw.rect(pantalla, color_borde, (x, y, tam_celda, tam_celda), 1)

            # dibuja los jugadores en la carcel
            if (fila, col) in casillas_especiales['C1'] and cont_carcel_1 < carcel_1:
                cont_carcel_1 += 1
                pygame.draw.circle(pantalla, color_jugador[1], (centro_x, centro_y), tam_celda // 4)

            if (fila, col) in casillas_especiales['C2'] and cont_carcel_2 < carcel_2:
                cont_carcel_2 += 1
                pygame.draw.circle(pantalla, color_jugador[2], (centro_x, centro_y), tam_celda // 4)

            if (fila, col) in casillas_especiales['C3'] and cont_carcel_3 < carcel_3:
                cont_carcel_3 += 1
                pygame.draw.circle(pantalla, color_jugador[3], (centro_x, centro_y), tam_celda // 4)

            if (fila, col) in casillas_especiales['C4'] and cont_carcel_4 < carcel_4:
                cont_carcel_4 += 1
                pygame.draw.circle(pantalla, color_jugador[4], (centro_x, centro_y), tam_celda // 4)

            # dibuja los nombres de los jugadores debajo de la carcel
            if (fila, col) in casillas_especiales['N1']:
                rect = pygame.Rect(x+tam_celda//2, y, tam_celda, tam_celda)
                texto = fuente_dados.render("Jugador: " + (str(1) if 1 not in nombres_jugadores else nombres_jugadores[1]), True, color_borde)
                text_rect = texto.get_rect(center=rect.center)
                pantalla.blit(texto, text_rect)

            if (fila, col) in casillas_especiales['N2']:
                rect = pygame.Rect(x+tam_celda//2, y, tam_celda, tam_celda)
                texto = fuente_dados.render("Jugador: " + (str(2) if 2 not in nombres_jugadores else nombres_jugadores[2]), True, color_borde)
                text_rect = texto.get_rect(center=rect.center)
                pantalla.blit(texto, text_rect)

            if (fila, col) in casillas_especiales['N3']:
                rect = pygame.Rect(x+tam_celda//2, y, tam_celda, tam_celda)
                texto = fuente_dados.render("Jugador: " + (str(3) if 3 not in nombres_jugadores else nombres_jugadores[3]), True, color_borde)
                text_rect = texto.get_rect(center=rect.center)
                pantalla.blit(texto, text_rect)

            if (fila, col) in casillas_especiales['N4']:
                rect = pygame.Rect(x+tam_celda//2, y, tam_celda, tam_celda)
                texto = fuente_dados.render("Jugador: " + (str(4) if 4 not in nombres_jugadores else nombres_jugadores[4]), True, color_borde)
                text_rect = texto.get_rect(center=rect.center)
                pantalla.blit(texto, text_rect)
                
            # dibuja los seguros
            if (fila, col) in casillas_especiales['Seg']:
                pygame.draw.rect(pantalla, color_seguro, (x, y, tam_celda, tam_celda))
            
            # dibuja las salidas
            if (fila, col) in casillas_especiales['S1']:
                pygame.draw.rect(pantalla, color_salidas['S1'], (x, y, tam_celda, tam_celda))
                
            if (fila, col) in casillas_especiales['S2']:
                pygame.draw.rect(pantalla, color_salidas['S2'], (x, y, tam_celda, tam_celda))
                
            if (fila, col) in casillas_especiales['S3']:
                pygame.draw.rect(pantalla, color_salidas['S3'], (x, y, tam_celda, tam_celda))
                
            if (fila, col) in casillas_especiales['S4']:
                pygame.draw.rect(pantalla, color_salidas['S4'], (x, y, tam_celda, tam_celda))

            # dibuja las fichas
            if len(tablero[fila][col]) > 2:
                pygame.draw.circle(pantalla, color_jugador[tablero[fila][col][1]], (centro1_x, centro1_y), tam_celda // 4)
                pygame.draw.circle(pantalla, color_jugador[tablero[fila][col][2]], (centro2_x, centro2_y), tam_celda // 4)
            elif len(tablero[fila][col]) > 1:
                pygame.draw.circle(pantalla, color_jugador[tablero[fila][col][1]], (centro_x, centro_y), tam_celda // 4)

    # dibuja el dado 1
    x = 20 * tam_celda
    y = 1 * tam_celda
    rect = pygame.Rect(x, y, tam_celda, tam_celda)
    pygame.draw.rect(pantalla, color_seleccionado if select_d1 else color_borde, (x, y, tam_celda, tam_celda), 1)
    texto = fuente_dados.render(str(valor_d1), True, color_borde if puede_mover_d1 else color_seleccionado if not auto_d1 else color_mov_auto)
    text_rect = texto.get_rect(center=rect.center)
    pantalla.blit(texto, text_rect)
    
    # dibuja el dado 2
    x = 20 * tam_celda
    y = 3 * tam_celda
    rect = pygame.Rect(x, y, tam_celda, tam_celda)
    pygame.draw.rect(pantalla, color_seleccionado if select_d2 else color_borde, (x, y, tam_celda, tam_celda), 1)
    texto = fuente_dados.render(str(valor_d2), True, color_borde if puede_mover_d2 else color_seleccionado if not auto_d1 else color_mov_auto)
    text_rect = texto.get_rect(center=rect.center)
    pantalla.blit(texto, text_rect)

    # dibuja la palabra jugador
    x = 20 * tam_celda
    y = 5 * tam_celda
    rect = pygame.Rect(x, y, tam_celda, tam_celda)
    texto = fuente_dados.render("Jugador", True, color_borde)
    text_rect = texto.get_rect(center=rect.center)
    pantalla.blit(texto, text_rect)

    # dibuja el nombre del jugador
    x = 20 * tam_celda
    y = 6 * tam_celda
    rect = pygame.Rect(x, y, tam_celda, tam_celda)
    texto = fuente_dados.render(str(jugador_actual) if jugador_actual not in nombres_jugadores else nombres_jugadores[jugador_actual], True, color_borde)
    text_rect = texto.get_rect(center=rect.center)
    pantalla.blit(texto, text_rect)

    # dibuja el mensaje que indica que oprimir h abre la ayuda
    x = 20 * tam_celda
    y = 17 * tam_celda
    rect = pygame.Rect(x, y, tam_celda, tam_celda)
    texto = fuente_dados.render("H = Ayuda", True, color_borde)
    text_rect = texto.get_rect(center=rect.center)
    pantalla.blit(texto, text_rect)

    pygame.display.flip()

# si se rompe el bucle cierra el programa
pygame.quit()