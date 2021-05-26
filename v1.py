import pygame
import random
import math
from os import path


#parametros
WIDTH = 1800
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
        #aself.image.fill(GREEN)
        self.rect = self.image.get_rect()

        self.x = WIDTH / 2
        self.y = WIDTH / 2
        self.rect.center = (self.x, self.y)

        self.last_pos = pygame.time.get_ticks()
        self.pos_ticks = 3000

        self.last_shot = pygame.time.get_ticks()
        self.shoot_ticks = 300

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

        self.speed = SPEED
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

    def dash(self):
        #dash
            mouse = pygame.mouse.get_pos()
            mouse_x = mouse[0]
            mouse_y = mouse[1]

            angulo_radianos = math.atan2(mouse_y - self.rect.bottom, mouse_x - self.rect.centerx)

            self.speedx = math.cos(angulo_radianos)
            self.speedy = math.sin(angulo_radianos)


            now = pygame.time.get_ticks()             
            elapsed_ticks = now - self.last_pos

            if elapsed_ticks > self.pos_ticks:
                self.last_pos = now
                self.rect.centerx += self.speed * self.speedx * 30
                self.rect.bottom += self.speed * self.speedy * 30

    def shoot(self):

        now = pygame.time.get_ticks()
        elapsed_ticks = now - self.last_shot

        if elapsed_ticks > self.shoot_ticks:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.centery, fireball_img)
            all_sprites.add(bullet)
            bullets.add(bullet)
      
    
class Mob(pygame.sprite.Sprite):
    def __init__(self, enemy_img):

        #sprite inimigo
        pygame.sprite.Sprite.__init__(self)

        self.image = enemy_img
        self.orig_image = enemy_img

        #self.image = pygame.Surface((30, 30))
        #self.image.fill(RED)

        self.rect = self.image.get_rect()

        self.x = random.randrange(WIDTH)
        self.y = random.randrange(HEIGHT)
        self.rect.center = (self.x, self.y)

        self.speedx = SPEED
        self.speedy = SPEED
        
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

        '''if self.x == player.x:
            self.kill()
        elif self.y == player.y:
            self.kill()'''

        if len(pygame.sprite.spritecollide(self, mobs, False)) > 1:
            print('colidiu')
        

class Bullet(pygame.sprite.Sprite):

    def __init__(self, centerx, centery, fireball_img):

        pygame.sprite.Sprite.__init__(self)
        self.image = fireball_img
        self.orig_image = fireball_img
        
        #self.image = pygame.Surface((20,20))
        #self.image.fill(BLUE)

        self.rect = self.image.get_rect()

        self.rect.centery = centery
        self.rect.centerx = centerx
        self.speed = 9
        
        mouse = pygame.mouse.get_pos()
        mouse_x = mouse[0]
        mouse_y = mouse[1]
        angulo_radianos = math.atan2(mouse_y - self.rect.centery, mouse_x - self.rect.centerx)
        
        self.speedx = math.cos(angulo_radianos)
        self.speedy = math.sin(angulo_radianos) 
        

         

    def update(self):

        #vel bala x y
        self.rect.centerx += self.speed * self.speedx
        self.rect.centery += self.speed * self.speedy 

        #sumir bala

        if self.rect.bottom < 0:
            self.kill()
        if self.rect.top > HEIGHT:
            self.kill()
        if self.rect.right > WIDTH:
            self.kill()
        if self.rect.left < 0:
            self.kill ()





#criar janela
pygame.init()   
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('ARENA GAME TESTE')
clock = pygame.time.Clock()


fireball_img = pygame.image.load(path.join(img_dir, 'fireball.png')).convert_alpha()
fireball_img = pygame.transform.scale(fireball_img, (25, 25))

player_img = pygame.image.load(path.join(img_dir, 'hyewonas.png')).convert_alpha()
player_img = pygame.transform.scale(player_img, (40, 40))

enemy_img = pygame.image.load(path.join(img_dir, 'gowon.png')).convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (40, 40))

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullet = Bullet(0, 0, fireball_img)
bullets = pygame.sprite.Group()
player = Player(player_img)
all_sprites.add(player)


for i in range(15):
    m = Mob(enemy_img)
    while ((m.rect.centerx - player.rect.centerx)**2 + (m.rect.centery - player.rect.centery)**2)**0.5 < 200:
        m = Mob(enemy_img)
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
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                player.dash()
        #tiros  
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.shoot()
                
    
    #update
    all_sprites.update()

    #checar bala com mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob(enemy_img)
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