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
        self.x = WIDTH / 2
        self.y = WIDTH / 2
        self.rect.center = (self.x, self.y)

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
    
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.bottom)
        all_sprites.add(bullet)
        bullets.add(bullet)
      
    
class Mob(pygame.sprite.Sprite):
    def __init__(self):

        #sprite inimigo
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25, 25))
        self.image.fill(RED)
        self.rect = self.image.get_rect()

        #self.rect.x = random.randrange(WIDTH - self.rect.width)
        # #self.rect.y = random.randrange(HEIGHT - self.rect.height)
        self.x = random.randrange(WIDTH - player.rect.width)
        self.y = random.randrange(HEIGHT - player.rect.height)
        self.rect.center = (self.x, self.y)

        self.speedx = random.randrange(3, SPEED - 1)
        self.speedy = random.randrange(3, SPEED - 1)
        
    def update(self):
        global player
        if self.x < player.rect.centerx:
            self.x += 1
            self.rect.center = (self.x, self.y)
            
        elif self.x > player.rect.centerx:
            self.x -= 1
            self.rect.center = (self.x, self.y)
            
        if self.y < player.rect.centery:
            self.y += 1
            self.rect.center = (self.x, self.y)
            
        elif self.y > player.rect.centery:
            self.y -= 1
            self.rect.center = (self.x, self.y)  
        

        #limitar na tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

class Bullet(pygame.sprite.Sprite):
    def __init__(self, centerx, bottom):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,10))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()

        self.rect.bottom = bottom
        self.rect.centerx = centerx
        self.speedy = -10 

    def update(self):

        self.rect.y += self.speedy

        #sumir bala

        if self.rect.bottom < 0:
            self.kill()




#criar janela
pygame.init()   
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('ARENA GAME TESTE')
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)


for i in range(10):
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

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    
    #update
    all_sprites.update()

    #checar bala com mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    #checar mob colidir com player
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        running = False

    #draw/render
    screen.fill(BLACK)
    all_sprites.draw(screen)

    #flip display
    pygame.display.flip()



pygame.quit()