import aisearch
from tkinter import *
from tkinter import messagebox

class Reversi:

    def __init__(self):
        self.principal = Tk()
        self.principal.title("Reversi")
        self.botones=[]
        self.negro = PhotoImage(file="negro.png")
        self.blanco = PhotoImage(file="blanco.png")
        self.vacio = PhotoImage(file="vacio.png")
        self.juego = aisearch.ReversiGame()

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
        self.juego.tablero[2][2] = "1"
        self.botones[3][3]["image"] = self.blanco
        self.juego.tablero[3][3] = "1"
        self.botones[3][2]["image"] = self.negro
        self.juego.tablero[3][2] = "-1"
        self.botones[2][3]["image"] = self.negro
        self.juego.tablero[2][3] = "-1"
        

    def victoria(self):
        if self.juego.estado_final():
            if self.juego.ganador == 1:
                messagebox.showinfo("Reversi", "has ganado")
            elif self.juego.ganador == 0:
                messagebox.showinfo("Reversi", "Empate")
            else:
                messagebox.showinfo("Reversi", "Has perdido")
            self.juego.reiniciar()

            for i in range(6):
                for j in range(6):
                    self.botones[i][j]["image"] = self.vacio

            return True
        else:
            return False 


    def click(self, evento):
        print("i do nothing")
        if self.juego.tablero[evento.widget.x][evento.widget.y] ==0:
            self.juego.jugar(evento.widget.x, evento.widget.y)
            evento.widget["image"] = self.negro
            print(self.juego.tablero)
            if not self.victoria():
                o = []
                m = aisearch.minimax(juego, 1, [], o)
                self.juego.jugar(m[1].x, m[1].y)
                self.botones[m[1].x][m[1].y]["image"] = self.blanco
                self.victoria()


juego = Reversi()
mainloop()
