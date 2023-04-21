
"""
Práctica realizada por Ainhoa Díaz Cabrera y Claudia Gómez Alonso.
"""

from multiprocessing.connection import Listener
from multiprocessing import Process, Manager, Value, Lock
import traceback
import sys
import random

#a continuación tenemos una serie de constantes que nos servirán a lo largo del programa:
LEFT_PLAYER = 0
RIGHT_PLAYER = 1
SIDESSTR = ["left", "right"]
SIZE = (787, 525)#el tamaño tiene que coincidir con el tamaño de la imagen que vamos a poner como fondo.
X=0
Y=1
DELTA = 30


"""Esta es la clase de los jugadores que, en este caso, serán las naves espaciales que irán a por la 
estrella para obtener puntos. Tendrá como atributo side, que indicará qué jugador es el que está
ejecutando los movimientos"""
class Player():
    def __init__(self, side):
        self.side = side
        if side == LEFT_PLAYER:
            self.pos = [5, SIZE[Y]//2]
        else:
            self.pos = [SIZE[X] - 5, SIZE[Y]//2]

    def get_pos(self):
        return self.pos

    def get_side(self):
        return self.side

    def moveDown(self):
        self.pos[Y] += DELTA
        if self.pos[Y] > SIZE[Y]:
            self.pos[Y] = SIZE[Y]

    def moveUp(self):
        self.pos[Y] -= DELTA
        if self.pos[Y] < 0:
            self.pos[Y] = 0
            
    def moveRight(self):
        self.pos[X] += DELTA
        if self.pos[X] > SIZE[X]:
            self.pos[X] = SIZE[X]
            
    def moveLeft(self):
        self.pos[X] -= DELTA
        if self.pos[X] < 0:
            self.pos[X] = 0
        

    def __str__(self):
        return f"P<{SIDESSTR[self.side]}, {self.pos}>"


"""Aquí tenemos la clase Ball, que representa a la estrella y se irá moviendo por el tablero y rebotando
en los bordes a una velocidad específica, que aparece como atributo 'velocity' y será un vector."""
class Ball():
    def __init__(self, velocity):
        self.pos=[ SIZE[X]//2, SIZE[Y]//2 ]
        self.velocity = velocity

    def get_pos(self):
        return self.pos

    def update(self):
        self.pos[X] += self.velocity[X]
        self.pos[Y] += self.velocity[Y]
    
    #esta es una función de actualización a la que se llamará cuando alguno de los jugadores (naves) 
    #alcance la bola, de modo que esta cambiará de posición a una aleatoria en ese instante.
    def update2(self): 
        self.pos[X] = random.randint(0,SIZE[X]) 
        self.pos[Y] = random.randint(0,SIZE[Y]) 
       

    def bounce(self, AXIS):
        self.velocity[AXIS] = -self.velocity[AXIS]

 

    def __str__(self):
        return f"B<{self.pos, self.velocity}>"


""""Esta clase es la que nos va a decir el estado del juego en cada momento, crea los jugadores
y la bola, así como otras variables que se necesitan, como la puntuación.  """
class Game():
    def __init__(self, manager):
        self.players = manager.list( [Player(LEFT_PLAYER), Player(RIGHT_PLAYER)] )
        self.ball = manager.list( [ Ball([-2,2]) ] )
        self.score = manager.list( [0,0] )
        self.running = Value('i', 1) # 1 running
        self.lock = Lock()

    def get_player(self, side):
        return self.players[side]

    def get_ball(self):
        return self.ball[0]

    def get_score(self):
        return list(self.score)

    def is_running(self):
        return self.running.value == 1

    def stop(self):
        self.running.value = 0
    
    #los siguientes cuatro métodos especifican los movimientos que pueden realizar cada uno de los 
    #jugadores, que se mueven controlados por el teclado por todo el tablero en busca de la bola (estrella).
    
    def moveUp(self, player):
        self.lock.acquire()
        p = self.players[player]
        p.moveUp()
        self.players[player] = p
        self.lock.release()

    def moveDown(self, player):
        self.lock.acquire()
        p = self.players[player]
        p.moveDown()
        self.players[player] = p
        self.lock.release()
        
    def moveRight(self, player):
        self.lock.acquire()
        p = self.players[player]
        p.moveRight()
        self.players[player] = p
        self.lock.release()

    def moveLeft(self, player):
        self.lock.acquire()
        p = self.players[player]
        p.moveLeft()
        self.players[player] = p
        self.lock.release()

    #cuando las bolas chocan con algún jugador, es decir alguna nave alcanza la estrella, lo que 
    #ocurrirá será que se sume un punto al jugador que haya conseguido atraparla. Además, si alguno
    #de los jugadores llega a 5 puntos o un múltiplo suyo, la velocidad de la bola aumentará, 
    #dificultando un poco el juego.
    def ball_collide(self, player):
        self.lock.acquire()
        ball = self.ball[0]
        self.score[player] += 1
        ball.update2()
        if self.score[player] % 5 == 0: #queremos que la velocidad aumente
            if ball.velocity[0] > 0:
                ball.velocity[0]+=0.25
            else:
                ball.velocity[0]-=0.25
            if ball.velocity[1] > 0:
                ball.velocity[1]+=0.25
            else:
                ball.velocity[1]-=0.25
        self.ball[0] = ball
        self.lock.release()

    def get_info(self):
        info = {
            'pos_left_player': self.players[LEFT_PLAYER].get_pos(),
            'pos_right_player': self.players[RIGHT_PLAYER].get_pos(),
            'pos_ball': self.ball[0].get_pos(),
            'score': list(self.score),
            'is_running': self.running.value == 1
        }
        return info

    def move_ball(self):
        self.lock.acquire()
        ball = self.ball[0]
        ball.update()
        pos = ball.get_pos()
        if pos[Y]<0 or pos[Y]>SIZE[Y]: #cuando la bola alcanza alguno de los bordes, rebota.
            ball.bounce(Y)
        if pos[X]>SIZE[X] or pos[X] < 0:
            ball.bounce(X)
        self.ball[0]=ball
        self.lock.release()


    def __str__(self):
        return f"G<{self.players[RIGHT_PLAYER]}:{self.players[LEFT_PLAYER]}:{self.ball[0]}:{self.running.value}>"


""""Esta función va a ir analizando cada uno de los comandos que hay para llamar a la función
correspondiente, según lo que se pide en cada momento que se haga."""
def player(side, conn, game):
    try:
        print(f"starting player {SIDESSTR[side]}:{game.get_info()}")
        conn.send( (side, game.get_info()) )
        while game.is_running():
            command = ""
            while command != "next":
                command = conn.recv()
                if command == "up":
                    game.moveUp(side)
                elif command == "down":
                    game.moveDown(side)
                elif command == "right":
                    game.moveRight(side)
                elif command == "left":
                    game.moveLeft(side)
                elif command == "collide":
                    game.ball_collide(side)
                elif command == "quit":
                    game.stop()
            if side == 1:
                game.move_ball()
            conn.send(game.get_info())
    except:
        traceback.print_exc()
        conn.close()
    finally:
        print(f"Game ended {game}")


def main(ip_address):
    manager = Manager()
    try:
        with Listener((ip_address, 6000),
                      authkey=b'secret password') as listener:
            n_player = 0
            players = [None, None]
            game = Game(manager)
            while True:
                print(f"accepting connection {n_player}")
                conn = listener.accept()
                players[n_player] = Process(target=player,
                                            args=(n_player, conn, game))
                n_player += 1
                if n_player == 2:
                    players[0].start()
                    players[1].start()
                    n_player = 0
                    players = [None, None]
                    game = Game(manager)

    except Exception as e:
        traceback.print_exc()

if __name__=='__main__':
    ip_address = "10.8.0.5"
    if len(sys.argv)>1:
        ip_address = sys.argv[1]

    main(ip_address)
