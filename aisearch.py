from tkinter.constants import E, NO


class ReversiGame:

    def __init__(self, turno = 1):
        
        estado = []

        for i in range(6):
            estado.append([])
            for j in range(6):
                estado[i].append(0)

        self.tablero = estado
        self.completo = False
        self.ganador = None
        self.jugador = turno
        print(self.tablero)
    


    def reinciar(self):

        tablero = []

        for i in range(6):
            tablero.append([])
            for j in range(6):
                tablero[i].append(0)

        self.tablero=tablero
        self.completo = False
        self.ganador = None
        self.jugador = 1
    
    def generar_jugadas_popsibles(self):
        posibles=[]
        print("Aún no sé hacer nada")

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