import random

def comprueba_choque(serpiente: list[tuple[int, int]], paredes: list[list[tuple[int, int]]], otra_serpiente: list[tuple[int, int]]) -> bool:
    '''
    Comprueba si la serpiente se ha chocado consigo misma, con las paredes o con la otra serpiente. Tenga en cuenta
    que la serpiente avanza siempre por su cabeza, que está situada en la 
    primera posición de la lista.

    Parámetros:
    serpiente: Lista de tuplas representando las posiciones (columna, fila) de cada segmento de la serpiente.
    paredes: Lista de listas de tuplas representando las posiciones (columna, fila) de los segmentos de las paredes.
    otra_serpiente: Lista de tuplas representando las posiciones (columna, fila) de la otra serpiente.

    Devuelve:
    True si la serpiente se ha chocado consigo misma, con las paredes o con la otra serpiente, False en caso contrario.
    '''    
    if serpiente[0] in serpiente[1:] or serpiente[0] in otra_serpiente:
        return True
    
    for pared in paredes:
        if serpiente[0] in pared:
            return True
        
    return False

def ha_comido_serpiente(serpiente: list[tuple[int, int]], posicion_comida: tuple[int, int]) -> bool:
    '''
    Comprueba si la cabeza de la serpiente está en la misma posición que la comida.

    Parámetros:
    serpiente: Lista de tuplas representando las posiciones (columna, fila) de la serpiente.
    posicion_comida: Tupla representando la posición de la comida (columna, fila).

    Devuelve:
    True si la cabeza de la serpiente está en la misma posición que la comida, False en caso contrario.
    '''
    if serpiente[0]==posicion_comida:
        return True
    else:
        return False

def crece_serpiente(serpiente: list[tuple[int, int]]) -> None:
    '''
    Hace crecer la serpiente añadiendo duplicando la posición de la cola

    Parámetros:
    serpiente: Lista de tuplas representando las posiciones (columna, fila) de la serpiente.
    '''
    serpiente.insert(-1,serpiente[-1])

def genera_comida_aleatoria(serpiente_jugador: list[tuple[int, int]], serpiente_ia: list[tuple[int, int]], paredes: list[list[tuple[int, int]]], filas: int, columnas: int) -> tuple[int, int]:
    '''
    Genera una posición aleatoria para la comida que no esté en la misma posición que las serpientes o las paredes.

    Parámetros:
    serpiente_jugador: Lista de tuplas representando las posiciones (columna, fila) de la serpiente.
    serpiente_ia: Lista de tuplas representando las posiciones (columna, fila) de la otra serpiente.
    paredes: Lista de listas de tuplas representando las posiciones (columna, fila) de los segmentos de las paredes.
    filas: Número de filas en el tablero de juego.
    columnas: Número de columnas en el tablero de juego.

    Devuelve:
    Posición aleatoria para la comida (columna, fila).
    '''
    comida=tuple()
    valido=False

    while valido==False:
        valido=True
        x=random.randint(0,columnas-1)
        y=random.randint(0,filas-1)
        comida=(x,y)
        for pared in paredes:
            if comida in pared:
                valido=False
        if comida in serpiente_jugador or comida in serpiente_ia:
            valido=False
        
    return comida

def mueve_serpiente(serpiente: list[tuple[int, int]], direccion: str, filas: int, columnas: int) -> None:
    '''
    Mueve la serpiente en el tablero según la dirección dada. El tablero es circular, lo que significa
    que si la serpiente se sale por la derecha, debe aparecer por la izquierda, y viceversa (y lo 
    mismo si se sale por arriba o por abajo).

    Parámetros:
    serpiente: Lista de tuplas representando las posiciones (columna, fila) de la serpiente.
    direccion: Dirección en la que se debe mover la serpiente ('Left', 'Right', 'Down', 'Up').
    filas: Número de filas en el tablero de juego.
    columnas: Número de columnas en el tablero de juego.
    '''
    if direccion=="Left":
        y=serpiente[0][1]  
        if serpiente[0][0]==0: 
            x=columnas-1
        else:
            x=serpiente[0][0]-1 
        
        serpiente.insert(0,(x,y))
        serpiente.pop()

    if direccion=="Right":
        y=serpiente[0][1]  
        if serpiente[0][0]==columnas-1: 
            x=0
        else:
            x=serpiente[0][0]+1 
        
        serpiente.insert(0,(x,y))
        serpiente.pop()

    if direccion=="Up":
        x=serpiente[0][0]  
        if serpiente[0][1]==0: 
            y=filas-1
        else:
            y=serpiente[0][1]-1 
        
        serpiente.insert(0,(x,y))
        serpiente.pop()

    if direccion=="Down":
        x=serpiente[0][0]  
        if serpiente[0][1]==filas-1: 
            y=0
        else:
            y=serpiente[0][1]+1 
        
        serpiente.insert(0,(x,y))
        serpiente.pop()

def decide_movimiento_ia(serpiente_rival: list[tuple[int, int]], serpiente_jugador: list[tuple[int, int]],
    paredes: list[list[tuple[int, int]]], posicion_comida: tuple[int, int],
    filas: int, columnas: int) -> str:
    '''
    Decide la dirección de movimiento de la serpiente rival, intentando elegir la que más 
    le acerque a la comida sin chocar.

    Parámetros:
    serpiente_rival: lista de posiciones (columna, fila) de la serpiente rival.
    serpiente_jugador: lista de posiciones de la serpiente del jugador.
    paredes: lista de listas de posiciones de las paredes.
    posicion_comida: posición actual de la comida.
    filas, columnas: tamaño del tablero.

    Devuelve:
    Dirección elegida: 'Left', 'Right', 'Up' o 'Down'.    
    '''
    # Construiremos una lista de (distancia_a_la_comida, direccion)
    opciones = []
    for d in ("Up", "Down", "Left", "Right"):
        
        serpiente_copia=serpiente_rival.copy()
        mueve_serpiente(serpiente_copia,d,filas,columnas)

        
        if comprueba_choque(serpiente_copia,paredes,serpiente_jugador)==False:    
            
            x1=serpiente_copia[0][0]
            x2=posicion_comida[0]
            y1=serpiente_copia[0][1]
            y2=posicion_comida[1]
            
            distancia_a_la_comida= abs(x1-x2) + abs(y1-y2)
            
            opciones.append((distancia_a_la_comida,d))
    
    k=-1
    if opciones!=[]:
        for i in opciones:
            if i[0]<k or k==-1:
                k=i[0]
                direccion=i[1]
        return direccion
    
    return "Up" 

