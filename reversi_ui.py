from tkinter import *
from tkinter import messagebox

class reversi:

    def __init__(self):
        self.principal = Tk()
        self.principal.title("Reversi")
        self.botones=[]
        self.negro = PhotoImage(file="negro.png")
        self.blanco = PhotoImage(file="blanco.png")
        self.vacio = PhotoImage(file="vacio.png")
        #self.juego = aisearch.ReversiMiniMax()

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
    
    def victoria(self):
        print("hi, i do nothing")

    def click(self, evento):
        print("i do nothing")

juego = reversi()
mainloop()
