import pygame
import random
import math
from os import path


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


img_dir = path.join(path.dirname(__file__), '')


class Player(pygame.sprite.Sprite):
    #sprite player
    def __init__(self, player_img):

        #player
        pygame.sprite.Sprite.__init__(self)

        self.image = player_img
        self.orig_image = player_img
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()

        self.x = WIDTH / 2
        self.y = WIDTH / 2
        self.rect.center = (self.x, self.y)

        self.speedx = 0
        self.speedy = 0

    def update(self):

        #olha para o mouse
        mouse = pygame.mouse.get_pos()
        mouse_x = mouse[0]
        mouse_y = mouse[1]

        # Guarda a posição do jogador em variáveis para facilitar
        cx = self.rect.centerx
        cy = self.rect.centery

        # Calcula o vetor do centro do personagem até o mouse
        direcao_x = mouse_x - cx
        direcao_y = mouse_y - cy

        # Calcula o ângulo entre o eixo horizontal e o vetor da direção
        angulo_radianos = math.atan2(direcao_y, direcao_x)
        angulo_graus = math.degrees(angulo_radianos)

        # Rotaciona a imagem
        # Como a imagem da nave está inicialmente apontando para cima, devemos
        # somar 90 graus, pois angulo_graus é contado a partir do eixo x positivo.
        # Nesse caso, o eixo x positivo seria a nave apontando para a direita.
        # Além disso, o eixo y aponta para baixo, mas a função math.atan2 assume
        # que o y aponta para cima, por isso devemos inverter a direção do ângulo

        angulo_rotacao = -(angulo_graus + 90)
        self.image = pygame.transform.rotate(self.orig_image, angulo_rotacao)
        self.rect = self.image.get_rect()
        self.rect.centerx = cx
        self.rect.centery = cy

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

        self.x = random.randrange(WIDTH - player.rect.width)
        self.y = random.randrange(HEIGHT - player.rect.height)
        self.rect.center = (self.x, self.y)

        self.speedx = random.randrange(3, SPEED)
        self.speedy = random.randrange(3, SPEED)
        
    def update(self):
        
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

        if len(pygame.sprite.spritecollide(self, mobs, False)) > 1:
            print('colidiu')
            self.x -= 1

            
        

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
        self.image = pygame.Surface((30,10))
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

player_img = pygame.image.load(path.join(img_dir, 'hyewonas.jpg')).convert_alpha()
player_img = pygame.transform.scale(player_img, (25, 25))

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player(player_img)
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