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

BALL1 = 0 #en este caso, al igual que para los jugadores, necesitaremos identificadores para cada una de las bolas de nuestro tablero
BALL2 = 1
BALL3 = 2
BALL4 = 3
BALL5 = 4
BALL6 = 5

SIZE = (800, 415) #el tamaño tiene que coincidir con el tamaño de la imagen que vamos a poner como fondo.
X=0
Y=1
DELTA = 30

"""Esta es la clase de los jugadores que, en este caso, serán laos astronautas que esquivarán cada uno 
de los meteoritos. Tendrá como atributo side, que indicará qué jugador es el que está
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


"""Aquí tenemos la clase Ball, que representa cada meteorito, que se irán moviendo por el tablero y rebotando
en los bordes a una velocidad específica, que aparece como 'velocity' y será un vector. Además también tendrá
como atributo 'ball', que hará referencia a la bola de entre las seis que hay que esté ejcutando alguno de los
métodos"""
class Ball():
    def __init__(self, velocity, ball):
        self.ball = ball
        self.pos=[ SIZE[X]//2, SIZE[Y]//2 ]
        self.velocity = velocity

    def get_pos(self):
        return self.pos

    def update(self):
        self.pos[X] += self.velocity[X]
        self.pos[Y] += self.velocity[Y]
        
    #esta es una función de actualización a la que se llamará cuando alguno de los jugadores 
    #sea alcanzado por alguna de las bolas, de modo que esta cambiará de posición a una aleatoria en ese instante.
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
        self.balls = manager.list( [Ball([-2,2], BALL1), Ball([2,2.1], BALL2), Ball([-2.2,-2], BALL3), Ball([2,-2.1], BALL4), Ball([-2.3,3], BALL5), Ball([2.2,-3.1], BALL6) ] )
        self.score = manager.list( [0,0] )
        self.running = Value('i', 1) # 1 running
        self.lock = Lock()

    def get_player(self, side):
        return self.players[side]

    def get_ball(self, ball):
        return self.balls[ball]

    def get_score(self):
        return list(self.score)

    def is_running(self):
        return self.running.value == 1

    def stop(self):
        self.running.value = 0

    #los siguientes cuatro métodos especifican los movimientos que pueden realizar cada uno de los 
    #jugadores, que se mueven controlados por el teclado por todo el tablero esquivando las bolas.
    
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
        
    #cuando las bolas chocan con algún jugador, lo que ocurrirá será que se sume un punto al jugador contrario Además, si alguno
    #de los jugadores llega a 10 puntos o un múltiplo suyo, la velocidad de la bola aumentará, dificultando cada vez más el juego.

    def ball_collide(self, player, ball):
        self.lock.acquire()
        bola = self.balls[ball]
        self.score[abs(player - 1)] += 1 #le sumamos uno al marcador del jugador contrario
        if self.score[player] % 10 == 0: #queremos que la velocidad aumente
            if bola.velocity[0] > 0:
                bola.velocity[0]+=0.25
            else:
                bola.velocity[0]-=0.25
            if bola.velocity[1] > 0:
                bola.velocity[1]+=0.25
            else:
                bola.velocity[1]-=0.25
        bola.update2()
        self.balls[ball] = bola
        self.lock.release()

    def get_info(self):
        info = {
            'pos_left_player': self.players[LEFT_PLAYER].get_pos(),
            'pos_right_player': self.players[RIGHT_PLAYER].get_pos(),
            'pos_ball1': self.balls[BALL1].get_pos(),
            'pos_ball2': self.balls[BALL2].get_pos(),
            'pos_ball3': self.balls[BALL3].get_pos(),
            'pos_ball4': self.balls[BALL4].get_pos(),
            'pos_ball5': self.balls[BALL5].get_pos(),
            'pos_ball6': self.balls[BALL6].get_pos(),
            'score': list(self.score),
            'is_running': self.running.value == 1
        }
        return info

    def move_ball(self, ball):
        self.lock.acquire()
        bola = self.balls[ball]
        bola.update()
        pos = bola.get_pos()
        if pos[Y]<0 or pos[Y]>SIZE[Y]:
            bola.bounce(Y)
        if pos[X]>SIZE[X] or pos[X] < 0:
            bola.bounce(X)
        self.balls[ball]=bola
        self.lock.release()


    def __str__(self):
        return f"G<{self.players[RIGHT_PLAYER]}:{self.players[LEFT_PLAYER]}:{self.balls[BALL1]}:{self.balls[BALL2]}:{self.balls[BALL3]}:{self.balls[BALL4]}:{self.balls[BALL5]}:{self.balls[BALL6]}:{self.running.value}>"

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
                elif command == "collide1": #un collide para cada bola
                    game.ball_collide(side,0)
                elif command == "collide2":
                    game.ball_collide(side,1)
                elif command == "collide3":
                    game.ball_collide(side,2)
                elif command == "collide4":
                    game.ball_collide(side,3)
                elif command == "collide5":
                     game.ball_collide(side,4)
                elif command == "collide6":
                     game.ball_collide(side,5)
                elif command == "quit":
                    game.stop()
            if side == 1:
                for i in range(6):
                    game.move_ball(i)
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
