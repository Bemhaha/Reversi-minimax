from tkinter.constants import E, FALSE, NO


class ReversiGame:

    #Constructor de la clase que contiene la lógica de Reversi en conjunto a su algoritmo MiniMax
    def __init__(self, turno = "1"):

        #se instancian los atributos bases para poder desarrollar el juego de manera óptima
        self.tablero = self.generaTablero() #Contiene una matriz de 6x6 que contendrá los datos de las jugadas, "0" si es tablero vacio, "1" si es ficha negro "-1" si es ficha blanco
        self.completo = False #Booleano que nos indica si el tablero se completó o aún quedan espacios pendientes
        self.ganador = None #este atributo indicará con 1 si ganó el usuario, -1 si ganó la computadora y 0 si es empate
        self.jugador = turno #esta variable alterna entre 1 y -1 según sea el turno de cada jugador
        self.nodos = 0 #contador de nodos generados para mostrar por consola los nodos creados en el árbol de búsqueda según requerimientos del profesor
        self.profundidadBusqueda = 1 #profundidad de busqueda por defecto de MiniMax
    

    #Función que se encarga de reiniciar la clase para poder volver a jugar Reversi una vez completado el juego en curso
    def reinciar(self):

        self.tablero= self.generaTablero() #volvemos a crear la matriz con "0"
        self.completo = False #indicamos que la matriz aún tiene posibles jugadas
        self.ganador = None #indicamos que aún no hay un ganador
        self.jugador = "1" #indicamos quién parte jugando 

    #función encargada de generar un tablero nuevo para Reversi, es una matriz de 6x6 la cual contendrá "0"
    def generaTablero(self):
        
        tablero = [] #instanciamos la lista

        #ciclo que permite crear la lista de listas o matriz
        for i in range(6):
            tablero.append([])
            for j in range(6):
                tablero[i].append("0") #insertamos los "0" o fichas vacias del tablero

        return tablero #se retorna el tablero limpio
    
    #Esta función se encarga de evaluar si ya nos encontramos en el momento de designar un ganador dado que el tablero ya no tiene "0" en el, y así retornar un booleano indicandonos la situación
    def estadoFinal(self, tablero):
        self.evaluar() #se llama a la función evaluar, la cual verá si aún hay "0" en la matriz, en caso de no encontrar, verá quién ganó

        if self.completo: #si estamos en situación de evaluar el ganador, se retornará VERDADERO
            return True
        else:           #en caso contrario retornará FALSO
            return False


    #Función que se encarga de evaluar si hay un ganador o no 
    def evaluar(self):
        
        suma = 0

        estado = False

        #en este ciclo vemos si el tablero se completó o no, si hay por lo menos un "0" la condición interna, sabremos que aún es posible seguir jugando
        for x in range(6):
            for y in range(6):
                if self.tablero[x][y] == "0":
                    estado = True

        #si el estado se mantiene FALSO, podemos evaluar quién ganó haciendo una suma del tablero completo, dado que el tablero está lleno de "1" o "-1" si la suma es negativa podemos asumir que ganó Blanco, si es positiva ganó negro, si es 0 es empate
        if not estado:
            self.completo = True
            for i in range (6):
                for j in range(6):
                    suma += int(self.tablero[i][j])
        
            if suma > 0: #caso en que gana Negro
                self.ganador = "1"
            elif suma < 0: #caso en que gana blanco
                self.ganador = "-1"
            else: #caso de empate
                self.ganador = "0"
        else:#se mantiene FALSO en caso de aún poder seguir jugando
            self.completo = False

        
    #En esta función vemos si la jugada que vamos a intentar es valida o no
    def jugadaValida(self, tablero , ficha, x, y):
        
        #primero revisamos si está disponible la celda para poner una ficha encima
        if tablero[x][y] != "0":
            return False
        else:
            #creamos una lista vacía de adyacentes y un booleano de adyacentes para poder ver si la jugada es válida más abajo
            adyacencia = False
            adyacencias = []

            #en este For doble recorremos la matriz en busqueda de los nodos adyacentes distintos de 0 del punto (x,y), en caso de no haber adyacencia quedará en FALSO
            for i in range(max(0, x-1), min(x+2,6)):
                for j in range(max(0,y-1), min(y+2,6)):
                    if tablero[i][j] != "0":
                        adyacencia = True
                        adyacencias.append([i,j])
            
            if not adyacencia: #retornamos jugada invalida ya que no hay fichas adyacentes al punto (x,y), por lo tanto, automaticamente es una jugada no valida
                return False
            else:

                booleano = False #bandera que usaremos para evaluar si es una jugada valida

                for adyacencia in adyacencias: #revisamos las adyacencias para ver si podemos jugar en el punto (x,y) según las reglas de REVERSi
                    
                    #se extrae el punto x e y de la lista de adyacencias
                    adyX = adyacencia[0]
                    adyY = adyacencia[1]
                    
                    #si la ficha es igual a la ficha del jugador, seguimos revisando las otras que queden en la lista de adyacencias, en caso contrario, revisamos si la jugada es posible
                    if tablero[adyX][adyY] == ficha:
                        continue
                    else:

                        #acotamos el area de busqueda
                        varX = adyX - x
                        varY = adyY - y
                        auxX = adyX
                        auxY = adyY
                        #ciclo que revisará si la jugada es valida en el area acotado
                        while 0 <= auxX <=5 and 0 <= auxY <= 5:
                            if tablero[auxX][auxY] == "0": #en caso de que encontremos un "0", la jugada será invalida, haremos un break y revisaremos la posible siguiente jugada
                                break

                            if tablero[auxX][auxY] == ficha: #si encontramos en el area acotada otra ficha del jugador, siginifca que podemos hacer reversi, y por lo tanto estamos en una diagonal o vertical o horizontal y es jugada valida
                                booleano = True
                                break
                            
                            #se incrementan los contadores para volver a acotar el area de busqueda
                            auxX += varX
                            auxY += varY
                #se retorna el booleano, si es valida la jugada será TRUE, en caso contrario FALSE
                return booleano

    #Heuristica que evalua con un puntaje un posible tablero futuro elegido por MiniMax
    def heuristicaMejorEsquina(self, tablero, ficha):

        #Iniciamos el puntaje total en 0, además de dar puntaje a las posibles jugadas, esta heuristica se basa en que las mejores jugadas son las esquinas
        puntajeHeuristica = 0
        puntajeEsquina = 25 #si la jugada es una esquina, sumaremos 25 pts
        puntajeAdyacente = 5 # si es una diagonal sumamos 5 puntos
        puntajeLateral = 5  #si es vertical u hotizontal la jugada sumamos 5 puntos

        #evaluamos que ficha es aliada y cual es enemiga
        if ficha == 1:
            ficha = "1"
            fichaEnemiga = "-1"
        else:
            ficha = "-1"
            fichaEnemiga = "1"

        #comenzamos con un for doble el analisis de la jugada en todo el tablero
        for x in range(6):
            for y in range(6):
                sumaAux = 1 #inciamos la suma en 1 que es el puntaje "base"
                if (x == 0 and y == 1) or (x == 1 and 0 <= y <= 1): #vemos si es una jugada del lateral izquierdo
                    if tablero[0][0] == ficha: #si la ficha encontrada es aliada, sumamos puntos
                        sumaAux = puntajeLateral
                    else: #en caso que sea ficha enemiga, los restamos 
                        sumaAux = -puntajeAdyacente
                    
                elif (x == 0 and y == 4) or (x == 1 and 4 <= y <= 5): #vemos si la jugada posible es del lateral izquierdo casi esquina
                    if tablero[5][0] == ficha:#si la ficha encontrada es aliada, sumamos puntos
                        sumaAux = puntajeLateral
                    else:#en caso que sea ficha enemiga, los restamos
                        sumaAux = -puntajeAdyacente
                elif (x == 5 and y == 1) or (x == 4 and 0 <= y <=1): #vemos si la jugada posible es del lateral derecho o casi esquina
                    if tablero[0][5] == ficha: #si la ficha es aliada, sumamos puntos
                        sumaAux = puntajeLateral
                    else:
                        sumaAux = -puntajeAdyacente #en caso contrario, restamos
                elif (x == 5 and y == 4) or (x == 4 and 4 <= y <= 5): #vemos si la jugada posible es lateral inferior o izquierda
                    if tablero[5][5] == ficha: #en caso de tener ficha en la esquina, sumamos puntaje lateral, dado que la esquina ya está tomada por nosotros
                        sumaAux = puntajeLateral
                    else:
                        sumaAux = -puntajeAdyacente #en caso contrario restamos
                elif (x == 0 and 1 < y < 4) or (x == 5 and 1 < y < 4) or (y == 0 and 1 < x < 4) or (y == 5 and 1<x<4): #revisamos el centro de la matriz de 6x6, para ver las jugadas posibles
                        sumaAux = puntajeLateral #si encontramos espacios, sumamos puntaje lateral
                elif (x == 0 and y == 0) or (x == 0 and y == 5) or (x == 5 and y == 0) or (x == 5 and y == 5): #y el ultimo caso, es que tengamos libre las esquinas y sea nuestra posible siguiente jugada
                    sumaAux = puntajeEsquina #así que sumamos puntaje esquina, el que es el mas grande 
                
                #si la posición indicada es de nuestra ficha aliada, lo sumamos a nuestro puntaje total de heuristica, en caso contrario, lo restamos
                if tablero[x][y] == ficha:
                    puntajeHeuristica += sumaAux
                elif tablero[x][y] == fichaEnemiga:
                    puntajeHeuristica -= sumaAux

        #retornamos el puntaje de la juagada posible con el tablero dado 
        return puntajeHeuristica

    #Función que se encarga de hacer reversi a las fichas que se deban según la ficha puesta por un jugador
    def movimientoAReversear(self, tab, x, y, ficha):

        newTab = self.copiaTablero(tab) #copiamos el tablero para trabajar sobre el sin modificar el original 

        newTab[x][y] = ficha #posicionamos la ficha previamente validada en la posición (x, y) del tablero

        adyacentes = [] #lista con tuplas de las fichas adyacentes a la ficha colocada

        #Buscamos en el espacio acotado los adyacentes
        for i in range(max(0,x-1),min(x+2,5)): 
            for j in range(max(0,y-1),min(y+2,5)):
                if newTab[i][j] != "0": #Si hay fichas podremos darlas vueltas y hacerles "reversi", así que buscamos los adyacentes que sean distintos de 0 o vacio
                    adyacentes.append([i, j]) #Añadimos a la lista adyacente las coordenadas encontradas ya sea con "1" o "-1"
        
        reversear = [] #fichas que deberemos dar vuelta, se instancia la lista

        #ciclo para revisar los adyacentes
        for adyacente in adyacentes:
            #Extraemos de la lista la tupla (x, y)
            adyX = int(adyacente[0])
            adyY = int(adyacente[1])

            #revisamos si en la tupla elegida hay una ficha enemiga, si es así, entramos a la condición
            if newTab[adyX][adyY] != ficha:

                #lista que guardara las posiciones de las fichas que debemos reversear o hacer "reversi"
                caminoAReversear = []

                #preparamos las precondiciones para acotar el cuadro de busqueda y preparar los sectores de busqueda
                varX = adyX - x
                varY = adyY - y
                auxX = adyX
                auxY = adyY

                #comenzamos a revisar las fichas que debemos reversear o no (reversear o hacer reversi)
                while 0 <= auxX <= 5 and 0 <= auxY <= 5:
                    #insertamos la tupla a la lista
                    caminoAReversear.append([auxX, auxY])
                    evaluar = newTab[auxX][auxY]

                    #revisamos si es una fucha vacia, en caso de ser no tenemos en que hacer reversi, hacemos un break y pasamos a la siguiente
                    if evaluar == "0":
                        break
                    
                    #si hay una ficha y podemos hacer reversi, agregamos a la lista reveresear
                    if evaluar == ficha:
                        for nodo in caminoAReversear:
                            reversear.append(nodo)
                        break
                    #sumamos los contadores del ciclo
                    auxX += varX
                    auxY += varY

        #hacemos reversi 
        for nodo in reversear:
            newTab[nodo[0]][nodo[1]] = ficha

        #se retorna el nuevo tablero con las fichas reverseadas 
        return newTab

    
    #Metodo encargado de crear un tablero copia de otro dado por parametros
    def copiaTablero(self, tab):
        #se crea un tablero nuevo 
        newTab = self.generaTablero()

        #con un ciclo doble copiamos los datos contenidos en el tablero dado por parametro
        for x in range(6):
            for y in range(6):
                newTab[x][y] = tab[x][y]
        
        #retornamos el nuevo tablero con las celdas copiadas
        return newTab

    #metodo de busqueda de jugada MINIMAX 
    def minimaxReversi(self, tableroOriginal, profundidadBusqueda, minOrMax):
        
        #contador de nodos creados
        self.nodos += 1
        #tableros creados
        auxTableros = []
        #jugadas posibles
        posibilidades = []

        #primero creamos 2 listas, una con matrices de tableros posibles, otra con posibles jugadas, destacar que los indices corresponden a las jugadas y su tablero
        for x in range(6):
            for y in range(6):
                if self.jugadaValida(self.tablero, "-1", x, y):
                    intentar = self.movimientoAReversear(tableroOriginal, x, y, "-1")
                    auxTableros.append(intentar)
                    posibilidades.append([x,y])
        
        
        #Comenzamos la creación del árbol

        # condición de salida, lo que indicia que llegamos a un nodo terminal en el arbol de tableros de busqueda
        if profundidadBusqueda == 0 or len(posibilidades) == 0:
            return ([self.heuristicaMejorEsquina(tableroOriginal, 1-minOrMax), tableroOriginal]) #se retorna el puntaje del tablero, en conjunto a sus tablero
        
        
        #max o min del arbolito
        if minOrMax:
            #max
            #si el booleano minOrMax es 1, siginifica que maximizaremos la jugada elegida, ya que será MAX quien está en juego
            mejorPuntaje = -10000 #inciamos el mejor puntaje como -infinito
            mejorTableroJugar = [] #lista con los tableros mejores para jugar

            #ciclo que crea los siguientes nodos del minimax, aleternando minOrMax
            for i in range(len(auxTableros)):
                #llamamos recursivamente a minimax y extraemos su puntaje para evaluar si es la jugada con la maxima cantidad de puntos posibles
                puntajeAux = self.minimaxReversi(auxTableros[i], profundidadBusqueda-1, 0)[0]
                
                #evaluamos si el tablero jugado da la maxima utilidad/puntaje, si es así, lo guardamos en el mejorTablero
                if puntajeAux > mejorPuntaje:
                    mejorPuntaje = puntajeAux
                    mejorTableroJugar = auxTableros[i]
            
            #se retorna el tablero dela mejor jugada en conjunto a su puntaje o utilidad
            return([mejorPuntaje, mejorTableroJugar])
        else:
            #min
            #si el booleano minOrMax es 0, significa que minimizaremos la jugada elegida, ya que será MIN quien está en juego
            mejorPuntaje = 10000 #iniciamos el mejor puntaje como + infiinito
            mejorTableroJugar = [] #lista con los tableros de menor utilidad o puntaje

            #ciclo que crea los siguientes nodos del minimax, alternado minOrMax
            for i in range(len(auxTableros)):
                #llamamos recursivamente a minimax y extraemos su puntaje para evaluar si la jugada minimiza la cantidad de puntos o utilidad
                puntajeAux = self.minimaxReversi(auxTableros[i], profundidadBusqueda-1, 1)[0]

                #evaluamos si el tablero jugado minimiza la utilidad/puntaje, si es así, lo guardamos en el mejorTablero
                if puntajeAux < mejorPuntaje:
                    mejorPuntaje = puntajeAux
                    mejorTableroJugar = auxTableros[i]

            #se retorna el tablero de la mejor jugada en conjunto de su utilidad
            return ([mejorPuntaje, mejorTableroJugar])

    #funciona que se encarga de que el "humano" pueda realizar su jugada
    def jugar(self, jugadax, jugaday):
        #se realiza en tablero la jugada del "humano"
        self.tablero[jugadax][jugaday] = self.jugador
        #se alterna el jugador
        self.jugador *= -1 
        
