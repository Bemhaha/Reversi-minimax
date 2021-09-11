from tkinter.constants import E, FALSE, NO


class ReversiGame:

    def __init__(self, turno = "-1"):

        self.tablero = self.generaTablero()
        self.completo = False
        self.ganador = None
        self.jugador = turno
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
    def jugadaValida(self, tablero , jugador, x, y):

        #print("fui llamada")

        if jugador == "1":
            ficha = "1"
        else:
            ficha = "-1"
        
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
                        estX = adyX
                        estY = adyY

                        while 0 <= estX <=5 and 0 <= estY <= 5:
                            if tablero[estX][estY] == "0":
                                break

                            if tablero[estX][estY] == ficha:
                                booleano = True
                                break

                            estX += varX
                            estY += varY
                return booleano



#drama end

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
        self.jugador*=-1 #ni idea que hace esto jaja
        

    def minimax(juego, etapa, secuencia, secuencias):
        print("aun no sé jugar bai")