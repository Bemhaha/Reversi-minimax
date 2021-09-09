from tkinter.constants import E, NO


class ReversiGame:

    def __init__(self, estado=[0]*6[0]*6, turno = 1):
        self.tablero = estado
        self.completo = False
        self.ganador = None
        self,jugador = turno
    
    def reinciar(self):
        self.tablero=[0]*6[0]*6
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