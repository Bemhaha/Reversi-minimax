import aisearch
from tkinter import *
from tkinter import messagebox


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
        
        #preparamos las imagenes para la interfaz gráfica
        self.principal.title("Reversi")
        self.botones=[]
        self.negro = PhotoImage(file="negro.png")
        self.blanco = PhotoImage(file="blanco.png")
        self.vacio = PhotoImage(file="vacio.png")
        self.sugerencia = PhotoImage(file="sugerencia.png")

        #Creamos los botones en una matriz 6x6 para el juego reversi 
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
        
        #Ponemos las fichas iniciales de Reversi, tanto en la interfáz gráfica como en la matriz interna de juegp en aisearch.py
        self.botones[2][2]["image"] = self.blanco
        self.juego.tablero[2][2] = "-1"
        self.botones[3][3]["image"] = self.blanco
        self.juego.tablero[3][3] = "-1"
        self.botones[3][2]["image"] = self.negro
        self.juego.tablero[3][2] = "1"
        self.botones[2][3]["image"] = self.negro
        self.juego.tablero[2][3] = "1"
        self.actualizacionTablero(self.juego.tablero) #actualizamos el tablero visible
    
    #Función encargada de darle pistas de jugadas válidad al usuario/humano
    def pistas(self, jugador):

        #guardamos el tablero en otra variable para que sea más simple de manejar
        tablero = self.juego.tablero

        #doble ciclo para recorrer la matriz
        for x in range(6):
            for y in range(6):
                
                #preguntamos si el jugador es el usuario/humano
                if jugador == "1":
                    #preguntamos si las coordanadas elegidas por el doble ciclo son válidas
                    if self.juego.jugadaValida(tablero, jugador, x, y):
                        #si la jugada es válida actualizamos el tablero de la interfaz gráfica con imagenes de cuadros con una x roja
                        self.botones[x][y]["image"] = self.sugerencia
        

    #Método encargado de revisar si la partida se encuentra en estado de elegir un ganador, si está en estado final, mostrará un messagebox diciendo quién ganó y luego reiniciará el juego
    def victoria(self, tablero):
        #preguntamos si estamos en estado final, es decir, si ya podemos designar un ganador
        if self.juego.estadoFinal(tablero):

            #vemos quién ganó, 1 si es el jugador humano, 0 si es empate, -1 si ganó la computadora
            if self.juego.ganador == "1":
                messagebox.showinfo("Reversi Game", "Has Ganado")
            elif self.juego.ganador == "0":
                messagebox.showinfo("Reversi Game", "Empate!")
            else:
                messagebox.showinfo("Reversi Game", "Has perdido!")
            
            #dado que estamos en estado final y ya nombramos al ganador, reiniciarmos el juego
            self.juego.reinciar()

            #restauramos la matriz de la interfaz gráfica, dejandola "solo con imágenes vacias"
            for i in range(6):
                for j in range(6):
                    self.botones[i][j]["image"] = self.vacio
            
            #ponemos las fichas inciales del juego
            self.botones[2][2]["image"] = self.blanco
            self.juego.tablero[2][2] = "-1"
            self.botones[3][3]["image"] = self.blanco
            self.juego.tablero[3][3] = "-1"
            self.botones[3][2]["image"] = self.negro
            self.juego.tablero[3][2] = "1"
            self.botones[2][3]["image"] = self.negro
            self.juego.tablero[2][3] = "1"
            self.actualizacionTablero(self.juego.tablero)
            self.pistas("1") #damos las pistas nuevas al jugador humano

            return True #retornamos verdadero dado que alguien ganó y se reinició el tablero
        else:
            #retornamos falso, dado que aún no podemos designar un ganador 
            return False

    #función encargada de actualizar el tablero de la interfaz gráfica según como se encuentra la matriz de reversi en aisearch.py
    def actualizacionTablero(self, tablero):

        #doble ciclo para recorrer la totalidad de la matriz
        for x in range(6):
            for y in range(6):
                #si es "1" lo que encontramos en la matriz, pondremos una imagen de ficha negra, si es -1 pondremos una imagen de ficha blanca, si es 0 podnremos una imagen de cuadro del tablero vacio
                if tablero[x][y] == "1":
                    self.botones[x][y]["image"] = self.negro
                elif tablero[x][y] == "-1":
                    self.botones[x][y]["image"] = self.blanco
                elif tablero[x][y] == "0":
                    self.botones[x][y]["image"] = self.vacio

        #mostramos las pistas al jugador
        self.pistas("1")

    #si el usuario hace "click" en un cuadro se llamará a este metodo
    def click(self, evento):
        #Se vé que el usuario haya clickeado en un cuadro válido, es decir, que esté "vacio", y sea una juagada valida
        if self.juego.tablero[evento.widget.x][evento.widget.y] == "0" and self.juego.jugadaValida(self.juego.tablero, "1", evento.widget.x, evento.widget.y):
            
            self.juego.jugar(evento.widget.x, evento.widget.y) #se hace la jugada en el tablero del usuario
            self.juego.tablero = self.juego.movimientoAReversear(self.juego.tablero, evento.widget.x, evento.widget.y, "1")#se hace reversi a las fichas que se deban según la jugada del usuario
            evento.widget["image"] = self.negro #se cambia la imagen clikeada a una de la ficha negro
            self.actualizacionTablero(self.juego.tablero) #actualizamos el tablero dada la jugada del usuario
            
            #preguntamos si estamos es estado de Victoria
            if not self.victoria(self.juego.tablero):
                #llamamos a Minimax de Reversi, para que haga su mejor jugada, en este caso, será la jugada de fichas blancas de la computadora
                resMinmax = self.juego.minimaxReversi(self.juego.tablero, self.juego.profundidadBusqueda, 1)
                #Minimax nos retornará un tablero con su jugada y fichas reverseadas, así que actualizamos el tablero main del juego
                self.juego.tablero = resMinmax[1]
                #actualizamos lo que mostramos al usuario por la interfaz gráfica según como jugó la computadora o minimax
                self.actualizacionTablero(self.juego.tablero)
                #imprimimos las nuevas pistas al usuario
                self.pistas("1")
                #revisamos si la computadora logró llegar a estado de victoria, si es así se reiniciará el juego luego de indicar quién ganó
                self.victoria(self.juego.tablero)

                
#Se instancia el juego Reversi y se deja en un loop
juego = Reversi()
mainloop()
