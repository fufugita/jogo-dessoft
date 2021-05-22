import pygame
import random
import math

#parametros
WIDTH = 1500
HEIGHT = 1000
FPS = 60
SPEED = 7

#cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Player(pygame.sprite.Sprite):
    #sprite player
    def __init__(self):

        #player
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25, 25))
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

        self.speedx = 0
        self.speedy = 0

    def update(self):

        self.speedx = 0
        self.speedy = 0


        #movimento
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_a]:
            self.speedx = -SPEED
        if keystate[pygame.K_d]:
            self.speedx = SPEED
        if keystate[pygame.K_w]:
            self.speedy = -SPEED
        if keystate[pygame.K_s]:
            self.speedy = SPEED

        #limitar na tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT


        self.rect.x += self.speedx
        self.rect.y += self.speedy
      
    
class Mob(pygame.sprite.Sprite):
    def __init__(self):

        #sprite inimigo
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25, 25))
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(HEIGHT - self.rect.height)

        self.speedx2 = random.randrange(1, SPEED - 1)
        self.speedy2 = random.randrange(1, SPEED - 1)


    def update(self):

        self.rect.x += self.speedx2
        self.rect.y += self.speedy2   

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT   

    

#criar janela
pygame.init()   
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('ARENA GAME TESTE')
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
player = Player()
all_sprites.add(player)


for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

#loop do jogo
running = True
while running:

    #cap fps
    clock.tick(FPS)

    #eventos
    for event in pygame.event.get():

        #se fechou a janela
        if event.type == pygame.QUIT:
            running = False

    #update
    all_sprites.update()

    #draw/render
    screen.fill(BLACK)
    all_sprites.draw(screen)

    #flip display
    pygame.display.flip()



pygame.quit()