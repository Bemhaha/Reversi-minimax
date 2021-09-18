import aisearch
from tkinter import *
from tkinter import messagebox
import time

class Reversi:

    def __init__(self):
        self.principal = NONE
        self.menu = Tk()
        self.juego = aisearch.ReversiGame()
        #self.iniciarReversi(3)

        #print("vamos a crear los botones")
        self.pregunta = Label(self.menu, text="Seleccione dificultad")
        self.facil = Button(self.menu, text="Fácil", command= self.iniciarReversiF)
        self.normal = Button(self.menu, text="Normal", command= self.iniciarReversiN)
        self.dificil = Button(self.menu, text="Dificíl", command= self.iniciarReversiD)
        self.pregunta.pack()
        self.facil.pack()
        self.normal.pack()
        self.dificil.pack()
        #print("terminé los botones")
        
    def iniciarReversiF(self):
        self.menu.destroy()
        self.iniciarReversi(2)

    def iniciarReversiN(self):
        self.menu.destroy()
        self.iniciarReversi(3)
    
    def iniciarReversiD(self):
        self.menu.destroy()
        self.iniciarReversi(4)

    def iniciarReversi(self, dificultad):

        self.principal = Tk()
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
