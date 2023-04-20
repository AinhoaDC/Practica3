from multiprocessing.connection import Client
import traceback
import pygame
import sys, os


#a continuación tenemos una serie de constantes que nos servirán a lo largo del programa:
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)
GREEN = (0,255,0)
X = 0
Y = 1
SIZE = (787, 525) #el tamaño tiene que coincidir con el tamaño de la imagen que vamos a poner como fondo.

LEFT_PLAYER = 0
RIGHT_PLAYER = 1
PLAYER_COLOR = [GREEN, YELLOW]
PLAYER_HEIGHT = 100
PLAYER_WIDTH = 95

BALL_SIZE = 30
FPS = 60




SIDES = ["left", "right"]
SIDESSTR = ["left", "right"]




"""De nuevo tenemos la clase player, ball y game con sus métodos correspondientes"""
class Player():
    def __init__(self, side):
        self.side = side
        self.pos = [None, None]

    def get_pos(self):
        return self.pos

    def get_side(self):
        return self.side

    def set_pos(self, pos):
        self.pos = pos

    def __str__(self):
        return f"P<{SIDES[self.side], self.pos}>"

class Ball():
    def __init__(self):
        self.pos=[ None, None ]

    def get_pos(self):
        return self.pos

    def set_pos(self, pos):
        self.pos = pos

    def __str__(self):
        return f"B<{self.pos}>"


class Game():
    def __init__(self):
        self.players = [Player(i) for i in range(2)]
        self.ball = Ball()
        self.score = [0,0]
        self.running = True

    def get_player(self, side):
        return self.players[side]

    def set_pos_player(self, side, pos):
        self.players[side].set_pos(pos)


    def get_ball(self):
        return self.ball

    def set_ball_pos(self, pos):
        self.ball.set_pos(pos)

    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score


    def update(self, gameinfo):
        self.set_pos_player(LEFT_PLAYER, gameinfo['pos_left_player'])
        self.set_pos_player(RIGHT_PLAYER, gameinfo['pos_right_player'])
        self.set_ball_pos(gameinfo['pos_ball'])
        self.set_score(gameinfo['score'])
        self.running = gameinfo['is_running']

    def is_running(self):
        return self.running

    def stop(self):
        self.running = False

    def __str__(self):
        return f"G<{self.players[RIGHT_PLAYER]}:{self.players[LEFT_PLAYER]}:{self.ball}>"

""""Ahora crearemos varias clases para crear los Sprites tanto de los jugadores como de la bola, de modo
que podamos colocarlos en el tablero de manera visible y correcta"""

#para crear sprites con las imágenes que nosotras queremos hacemos lo siguiente:
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder,'img')
player_img = pygame.image.load(os.path.join(img_folder, 'nave.png'))

class Person(pygame.sprite.Sprite):
    def __init__(self, player):
      super().__init__()
      pygame.sprite.Sprite.__init__(self)
      self.player = player
      self.image = player_img
      self.image.set_colorkey(BLACK)
      self.rect = self.image.get_rect()
      self.rect.center = (PLAYER_WIDTH / 2, PLAYER_HEIGHT / 2)
      self.update()

    def update(self):
        pos = self.player.get_pos()
        self.rect.centerx, self.rect.centery = pos

    def __str__(self):
        return f"S<{self.player}>"

player_img2 = pygame.image.load(os.path.join(img_folder, 'estrella.png')) #imagen para el sprite de la bola.

class BallSprite(pygame.sprite.Sprite):
    def __init__(self, ball):
        super().__init__()
        self.ball = ball
        self.image = player_img2
        self.rect = self.image.get_rect()
        self.rect.center = (BALL_SIZE / 2, BALL_SIZE / 2)
        self.update()

    def update(self):
        pos = self.ball.get_pos()
        self.rect.centerx, self.rect.centery = pos


""""En esta clase desarrollaremos todo el juego, se analizarán los eventos que van teniendo lugar en el 
juego uno a uno para ejecutar los movimientos deseados en cada momento"""
class Display():
    def __init__(self, game):
        self.game = game
        self.people = [Person(self.game.get_player(i)) for i in range(2)]

        self.ball = BallSprite(self.game.get_ball()) #colocamos en el tablero la bola.
        self.all_sprites = pygame.sprite.Group()
        self.people_group = pygame.sprite.Group()
        for person  in self.people:
            self.all_sprites.add(person)
            self.people_group.add(person)
        self.all_sprites.add(self.ball)

        self.screen = pygame.display.set_mode(SIZE)
        self.clock =  pygame.time.Clock()  #FPS
        self.background = pygame.image.load('espacio2.png') #elegimos la imagen que queremos poner en el fondo.
        pygame.init()

    #según la tecla que se pulse, se ejecuta una acción u otra.
    def analyze_events(self, side):
        events = []
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    events.append("quit")
                elif event.key == pygame.K_UP:
                    events.append("up")
                elif event.key == pygame.K_DOWN:
                    events.append("down")
                elif event.key == pygame.K_RIGHT:
                    events.append("right")
                elif event.key == pygame.K_LEFT:
                    events.append("left")
            elif event.type == pygame.QUIT:
                events.append("quit")
        if pygame.sprite.collide_rect(self.ball, self.people[side]):
            events.append("collide")
        return events


    def refresh(self):
        self.all_sprites.update()
        self.screen.blit(self.background, (0, 0))
        score = self.game.get_score()
        font = pygame.font.Font(None, 74)
        text = font.render(f"{score[LEFT_PLAYER]}", 1, WHITE)
        self.screen.blit(text, (250, 10))
        text = font.render(f"{score[RIGHT_PLAYER]}", 1, WHITE)
        self.screen.blit(text, (SIZE[X]-250, 10))
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def tick(self):
        self.clock.tick(FPS)

    @staticmethod
    def quit():
        pygame.quit()


def main(ip_address):
    try:
        with Client((ip_address, 6000), authkey=b'secret password') as conn:
            game = Game()
            side,gameinfo = conn.recv()
            print(f"I am playing {SIDESSTR[side]}")
            game.update(gameinfo)
            display = Display(game)
            while game.is_running():
                events = display.analyze_events(side)
                for ev in events:
                    conn.send(ev)
                    if ev == 'quit':
                        game.stop()
                conn.send("next")
                gameinfo = conn.recv()
                game.update(gameinfo)
                display.refresh()
                display.tick()
    except:
        traceback.print_exc()
    finally:
        pygame.quit()


if __name__=="__main__":
    ip_address = "10.8.0.5"
    if len(sys.argv)>1:
        ip_address = sys.argv[1]
    main(ip_address)
