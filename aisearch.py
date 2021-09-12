from tkinter.constants import E, FALSE, NO


class ReversiGame:

    def __init__(self, turno = "1"):

        self.tablero = self.generaTablero()
        self.completo = False
        self.ganador = None
        self.jugador = turno
        self.nodos = 0
        #self.profundidadBusqueda = 6
        print(self.tablero)
    


    def reinciar(self):

        self.tablero= self.generaTablero()
        self.completo = False
        self.ganador = None
        self.jugador = 1

    def generaTablero(self):
        
        tablero = []

        for i in range(6):
            tablero.append([])
            for j in range(6):
                tablero[i].append("0")

        return tablero      

#buscar posibles jugadas
    def jugadaValida(self, tablero , ficha, x, y):

        #print("fui llamada")
        
        if tablero[x][y] != "0":
            return False
        else:
            adyacencia = False
            adyacencias = []

            for i in range(max(0, x-1), min(x+2,6)):
                for j in range(max(0,y-1), min(y+2,6)):
                    if tablero[i][j] != "0":
                        adyacencia = True
                        adyacencias.append([i,j])
            
            if not adyacencia:
                return False
            else:

                booleano = False

                for adyacencia in adyacencias:

                    adyX = adyacencia[0]
                    adyY = adyacencia[1]

                    if tablero[adyX][adyY] == ficha:
                        continue
                    else:
                        #modulo
                        varX = adyX - x
                        varY = adyY - y
                        auxX = adyX
                        auxY = adyY

                        while 0 <= auxX <=5 and 0 <= auxY <= 5:
                            if tablero[auxX][auxY] == "0":
                                break

                            if tablero[auxX][auxY] == ficha:
                                booleano = True
                                break

                            auxX += varX
                            auxY += varY
                return booleano

#drama end

#new drama ia
    
    def minimax(self, tableroOriginal, profundidadBusqueda, minOrMax):
        print("idk what i do, but the real thing is, i do nothing xd") 
        self.nodos += 1
        auxTableros = []
        posibilidades = []

        for x in range(6):
            for y in range(6):
                if self.jugadaValida(tableroOriginal, "1", x, y):
                    intentar = self.movimientoAReversear(tableroOriginal, x, y, "1")
                    auxTableros.append(intentar)
                    posibilidades.append([x,y])
        
        #creación árbol 
        # condición de salida
        if profundidadBusqueda == 0 or len(posibilidades) == 0:
            return ([self.heuristicaMejorEsquina(tableroOriginal, "1", not minOrMax), tableroOriginal])
        #max o min del arbolito
        if minOrMax:
            #max
            mejorPuntaje = -10000
            mejorTableroJugar = []
            for tablero in auxTableros:
                puntajeAux = self.minimax(tablero, profundidadBusqueda-1, 0)[0]
                if puntajeAux > mejorPuntaje:
                    mejorPuntaje = puntajeAux
                    mejorTableroJugar = tablero
            return([mejorPuntaje, mejorTableroJugar])
        else:
            #min
            mejorPuntaje = 10000
            mejorTableroJugar = []
            for tablero in auxTableros:
                puntajeAux = self.minimax(tablero, profundidadBusqueda-1, 1)[0]
                if puntajeAux < mejorPuntaje:
                    mejorPuntaje = puntajeAux
                    mejorTableroJugar = tablero
            return ([mejorPuntaje, mejorTableroJugar])



    #heuristica extraida de un libro 
    def heuristicaMejorEsquina(self, tablero, ficha):
        print("holanda que talca")

        puntajeHeuristica = 0
        puntajeEsquina = 3
        puntajeAdyacente = 1
        puntajeLateral = 1

        if ficha == "1":
            fichaEnemiga = "-1"
        else:
            fichaEnemiga = "1"

        for x in range(6):
            for y in range(6):
                sumaAux = 1
                if (x == 0 and y == 1) or (x == 1 and 0 <= y <= 1):
                    if tablero[0][0] == ficha:
                        sumaAux = puntajeLateral
                    else:
                        sumaAux = -puntajeAdyacente
                    
                elif (x == 0 and y == 4) or (x == 1 and 4 <= y <= 5):
                    if tablero[6][0] == ficha:
                        sumaAux = puntajeLateral
                    else:
                        sumaAux = -puntajeAdyacente
                elif (x == 5 and y == 1) or (x == 4 and 0 <= y <=1):
                    if tablero[0][5] == ficha:
                        sumaAux = puntajeLateral
                    else:
                        sumaAux = -puntajeAdyacente
                elif (x == 5 and y == 4) or (x == 4 and 4 <= y <= 5):
                    if tablero[5][5] == ficha:
                        sumaAux = puntajeLateral
                    else:
                        sumaAux = -puntajeAdyacente
                elif (x == 0 and 1 < y < 4) or (x == 5 and 1 < y < 4) or (y == 0 and 1 < x < 4) or (y == 5 and 1<x<4):
                        sumaAux = puntajeLateral
                elif (x == 0 and y == 0) or (x == 0 and y == 5) or (x == 5 and y == 0) or (x == 5 and y == 5):
                    sumaAux = puntajeEsquina
                
                if tablero[x][y] == ficha:
                    puntajeHeuristica += sumaAux
                elif tablero[x][y] == fichaEnemiga:
                    puntajeHeuristica -= sumaAux
        
        print("puntaje ewe -->  ", puntajeHeuristica) 
        return puntajeHeuristica

    def movimientoAReversear(self, tab, x, y, ficha):

        newTab = self.copiaTablero(tab)

        newTab[x][y] = ficha

        adyacentes = []

        for i in range(max(0,x-1),min(x+2,6)):
            for j in range(max(0,y-1),min(y+2,8)):
                if newTab[i][j] != "0":
                    adyacentes.append([i, j])
        
        reversear = []

        for adyacente in adyacentes:
            adyX = adyacentes[0]
            adyY = adyacente[1]

            if newTab[adyX][adyY] != ficha:

                caminoAReversear = []

                varX = adyX - x
                varY = adyY - y
                auxX = adyX
                auxY = adyY

                while 0 <= auxX <= 5 and 0 <= auxY <= 5:
                    caminoAReversear.append([auxX, auxY])
                    evaluar = newTab[adyX][adyY]

                    if evaluar == "0":
                        break

                    if evaluar == ficha:
                        for nodo in caminoAReversear:
                            reversear.append(nodo)
                        break

                    auxX += varX
                    auxY += varY
        
        for nodo in reversear:
            newTab[nodo[0]][nodo[1]] == ficha
        
        return newTab

        

    
    def copiaTablero(self, tab):
        newTab = self.generaTablero()

        for x in range(6):
            for y in range(6):
                newTab[x][y] = tab[x][y]
        
        return newTab

#new drama ia end

    def estado_final(self):
        self.evaluar()
        if self.ganador is not None or self.completo:
            return True
        else:
            return False
    
    def evaluar(self):
        print("aun no hago nada jaja salu2")
    
    def calcular_utilidad(self):
        return self.ganador
    
    def jugar(self, jugadax, jugaday):
        self.tablero[jugadax][jugaday] = self.jugador
        self.jugador *= -1 #ni idea que hace esto jaja
        

    def minimax(juego, etapa, secuencia, secuencias):
        print("aun no sé jugar bai")