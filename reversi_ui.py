import aisearch
from tkinter import *
from tkinter import messagebox
import time

class Reversi:

    def __init__(self):
        #se crea un atributo para más adelante instanciar un TK()
        self.principal = NONE
        #Se instancia un TK() para elegir la dificultad del juego
        self.menu = Tk()
        #se instancia la "ia" del juego
        self.juego = aisearch.ReversiGame()

        #Se preparan los datos para el TK menú y así poder elegir la dificultad
        self.pregunta = Label(self.menu, text="Seleccione dificultad")
        self.facil = Button(self.menu, text="Fácil", command= self.iniciarReversiF)
        self.normal = Button(self.menu, text="Normal", command= self.iniciarReversiN)
        self.dificil = Button(self.menu, text="Dificíl", command= self.iniciarReversiD)

        #se hace pack al TK menú para poder mostrar en la interfaz la elección de dificultad
        self.pregunta.pack()
        self.facil.pack()
        self.normal.pack()
        self.dificil.pack()
    
    #si el usuario toca el recuerdo de "facil", se iniciará el juego con una profundidad de busqueda 2
    def iniciarReversiF(self):
        #se destruye el tk para poder iniciar el tk del maingame
        self.menu.destroy()
        #se inicia el juego con dificultado 2
        self.iniciarReversi(2)

    #si el usuario toca el recuerdo de "normal", se iniciará el juego con una profundidad de busqueda 3
    def iniciarReversiN(self):
        #se destruye el tk para poder iniciar el tk del maingam
        self.menu.destroy()
        #se inicia el juego con dificultado 3
        self.iniciarReversi(3)
    
    #si el usuario toca el recuerdo de "dificil", se iniciará el juego con una profundidad de busqueda 4
    def iniciarReversiD(self):
        #se destruye el tk para poder iniciar el tk del maingam
        self.menu.destroy()
        #se inicia el juego con dificultado 4
        self.iniciarReversi(4)

    #metodo que inicia REVERSI, recibe como parametro la dificultad o profundidad de busqueda para minimax
    def iniciarReversi(self, dificultad):

        #instanciamos en principal el TK()
        self.principal = Tk()
        #Se establece la dificultad de busqueda según lo elegido por el usuario
        self.juego.profundidadBusqueda = dificultad
        
        
        self.principal.title("Reversi")
        self.botones=[]
        self.negro = PhotoImage(file="negro.png")
        self.blanco = PhotoImage(file="blanco.png")
        self.vacio = PhotoImage(file="vacio.png")
        self.sugerencia = PhotoImage(file="sugerencia.png")

        for i in range(6):
            fila=[]
            for j in range(6):
                b1=Button(self.principal, image=self.vacio, width="80",height="80")
                b1.bind("<Button-1>", self.click)
                b1.x=i
                b1.y=j
                b1.grid(row=i, column=j)
                fila.append(b1)
            self.botones.append(fila)
        
        
        self.botones[2][2]["image"] = self.blanco
        self.juego.tablero[2][2] = "-1"
        self.botones[3][3]["image"] = self.blanco
        self.juego.tablero[3][3] = "-1"
        self.botones[3][2]["image"] = self.negro
        self.juego.tablero[3][2] = "1"
        self.botones[2][3]["image"] = self.negro
        self.juego.tablero[2][3] = "1"
        self.actualizacionTablero(self.juego.tablero)
    
    def pistas(self, jugador):

        #print("buscando pistas")
        tablero = self.juego.tablero
        for x in range(6):
            for y in range(6):
                #print("buscando pistas2")
                if jugador == "1":
                    #print("buscando pistas3")
                    if self.juego.jugadaValida(tablero, jugador, x, y):
                        self.botones[x][y]["image"] = self.sugerencia
                        #print("cambio sugerencia")

    def hayQuePasarLaJugada(self, jugador):
        
        tablero = self.juego.tablero

        for x in range(6):
            for y in range(6):
                if self.juego.jugadaValida(tablero, jugador, x, y):
                    return True
        
        return False
        

    def victoria(self, tablero):
        if self.juego.estadoFinal(tablero):
            #print("Estamos en estado final = ", self.juego.estadoFinal(tablero))
            #print("el ganador es = ", self.juego.ganador)
            if self.juego.ganador == "1":
                messagebox.showinfo("Reversi Game", "Has Ganado")
            elif self.juego.ganador == "0":
                messagebox.showinfo("Reversi Game", "Empate!")
            else:
                messagebox.showinfo("Reversi Game", "Has perdido!")
            
            self.juego.reinciar()

            for i in range(6):
                for j in range(6):
                    self.botones[i][j]["image"] = self.vacio
            
            self.botones[2][2]["image"] = self.blanco
            self.juego.tablero[2][2] = "-1"
            self.botones[3][3]["image"] = self.blanco
            self.juego.tablero[3][3] = "-1"
            self.botones[3][2]["image"] = self.negro
            self.juego.tablero[3][2] = "1"
            self.botones[2][3]["image"] = self.negro
            self.juego.tablero[2][3] = "1"
            self.actualizacionTablero(self.juego.tablero)
            self.pistas("1")
            return True
        else: 
            return False

    def actualizacionTablero(self, tablero):

        for x in range(6):
            for y in range(6):
                if tablero[x][y] == "1":
                    self.botones[x][y]["image"] = self.negro
                elif tablero[x][y] == "-1":
                    self.botones[x][y]["image"] = self.blanco
                elif tablero[x][y] == "0":
                    self.botones[x][y]["image"] = self.vacio

        self.pistas("1")


    def click(self, evento):
        #print("i do nothing")
        if self.juego.tablero[evento.widget.x][evento.widget.y] == "0" and self.juego.jugadaValida(self.juego.tablero, "1", evento.widget.x, evento.widget.y):
            self.juego.jugar(evento.widget.x, evento.widget.y)
            #print("x = ", evento.widget.x, " y= ", evento.widget.y)
            self.juego.tablero = self.juego.movimientoAReversear(self.juego.tablero, evento.widget.x, evento.widget.y, "1")
            evento.widget["image"] = self.negro
            self.actualizacionTablero(self.juego.tablero)
            time.sleep(1)
            
            #print(self.juego.tablero)
            if not self.victoria(self.juego.tablero):
                resMinmax = self.juego.minimaxReversi(self.juego.tablero, self.juego.profundidadBusqueda, 1)
                self.juego.tablero = resMinmax[1]
                self.actualizacionTablero(self.juego.tablero)
                self.pistas("1")
                self.victoria(self.juego.tablero)

                #print("tablero = ", self.juego.tablero)
                

juego = Reversi()
mainloop()
