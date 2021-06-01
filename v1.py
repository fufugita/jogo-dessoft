import pygame
import random
import math
from os import path

pygame.init()   
pygame.mixer.init()

#===== INICIA ASSETS =====
WIDTH = 1800
HEIGHT = 1000
FPS = 60
SPEED = 7

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))    
pygame.display.set_caption('ARENA GAME TESTE')

img_dir = path.join(path.dirname(__file__), 'assets', 'img')
snd_dir = path.join(path.dirname(__file__), 'assets', 'snd')

fireball_img = pygame.image.load(path.join(img_dir, 'fireball.png')).convert_alpha()
fireball_img = pygame.transform.scale(fireball_img, (25, 25))

player_img = pygame.image.load(path.join(img_dir, 'hyewonas.png')).convert_alpha()
player_img = pygame.transform.scale(player_img, (40, 40))

enemy_img = pygame.image.load(path.join(img_dir, 'gowon.png')).convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (40, 40))

pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.1)

font = pygame.font.SysFont(None, 48)

#===== ESTRUTURA DE DADOS =====
class Player(pygame.sprite.Sprite):

    #----- SPRITE DO PLAYER
    def __init__(self, player_img):

        #----- PLAYER
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.orig_image = player_img
        self.rect = self.image.get_rect()
        self.x = WIDTH / 2
        self.y = WIDTH / 2
        self.rect.center = (self.x, self.y)

        #----- SET PARA COOLDOWN DASH
        self.last_pos = pygame.time.get_ticks()
        self.pos_ticks = 2000

        #----- SET PARA COOLDOWN ATIRAR
        self.last_shot = pygame.time.get_ticks()
        self.shoot_ticks = 300

        #----- PLAYER PARADO POR DEFAULT
        self.speedx = 0
        self.speedy = 0

    #----- UPDATE DAS AÇÕES DO PLAYER
    def update(self):

        #----- OLHA NA DIREÇÃO DO MOUSE
        mouse = pygame.mouse.get_pos()
        mouse_x = mouse[0]
        mouse_y = mouse[1]
        cx = self.rect.centerx
        cy = self.rect.centery
        direcao_x = mouse_x - cx
        direcao_y = mouse_y - cy
        angulo_radianos = math.atan2(direcao_y, direcao_x)
        angulo_graus = math.degrees(angulo_radianos)
        angulo_rotacao = -(angulo_graus + 90)
        self.image = pygame.transform.rotate(self.orig_image, angulo_rotacao)
        self.rect = self.image.get_rect()
        self.rect.centerx = cx
        self.rect.centery = cy

        #----- VELOCIDADE
        self.speed = SPEED
        self.speedx = 0
        self.speedy = 0

        #----- MOVIMENTO
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -SPEED
        if keystate[pygame.K_d]:
            self.speedx = SPEED
        if keystate[pygame.K_w]:
            self.speedy = -SPEED
        if keystate[pygame.K_s]:
            self.speedy = SPEED

        #----- LIMITAR PLAYER NA TELA
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        #----- ATUALIZA VELOCIDADE
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def dash(self):
        #----- DASH
            mouse = pygame.mouse.get_pos()
            mouse_x = mouse[0]
            mouse_y = mouse[1]
            angulo_radianos = math.atan2(mouse_y - self.rect.bottom, mouse_x - self.rect.centerx)
            self.speedx = math.cos(angulo_radianos)
            self.speedy = math.sin(angulo_radianos)

            #----- COOLDOWN DASH
            now = pygame.time.get_ticks()             
            elapsed_ticks = now - self.last_pos
            if elapsed_ticks > self.pos_ticks:
                self.last_pos = now
                self.rect.centerx += self.speed * self.speedx 
                self.rect.bottom += self.speed * self.speedy 

    def shoot(self):
        #----- ATIRAR E COOLDOWN
        now = pygame.time.get_ticks()
        elapsed_ticks = now - self.last_shot
        if elapsed_ticks > self.shoot_ticks:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.centery, fireball_img)
            all_sprites.add(bullet)
            bullets.add(bullet)
      
    
class Mob(pygame.sprite.Sprite):

    #----- SPRITE MOB
    def __init__(self, enemy_img):

        #----- MOB INIMIGO
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.orig_image = enemy_img
        self.rect = self.image.get_rect()

        #----- SPAWN ALEATÓRIO
        self.x = random.randrange(WIDTH)
        self.y = random.randrange(HEIGHT)
        self.rect.center = (self.x, self.y)

        #----- VELOCIDADE
        self.speedx = SPEED
        self.speedy = SPEED
        
    #----- ATUALIZA POSIÇÃO DO MOB
    def update(self):
        
        #----- MOVE O MOB EM DIREÇÃO DO PLAYER
        if self.x < player.rect.centerx:
            self.x += self.speedx/3
            self.rect.center = (self.x, self.y)   
        elif self.x > player.rect.centerx:
            self.x -= self.speedx/3
            self.rect.center = (self.x, self.y)  
        if self.y < player.rect.centery:
            self.y += self.speedy/3
            self.rect.center = (self.x, self.y)  
        elif self.y > player.rect.centery:
            self.y -= self.speedy/3
            self.rect.center = (self.x, self.y) 

        #if len(pygame.sprite.spritecollide(self, mobs, False)) > 1:
            #print('colidiu')
        

class Bullet(pygame.sprite.Sprite):

    #----- SPRITE TIRO
    def __init__(self, centerx, centery, fireball_img):

        #----- TIRO
        pygame.sprite.Sprite.__init__(self)
        self.image = fireball_img
        self.orig_image = fireball_img
        self.rect = self.image.get_rect()
        self.rect.centery = centery
        self.rect.centerx = centerx

        #----- VELOCIDADE DEFAULT
        self.speed = 15
        
        #----- ATIRA NA DIREÇÃO DO MOUSE
        mouse = pygame.mouse.get_pos()
        mouse_x = mouse[0]
        mouse_y = mouse[1]
        angulo_radianos = math.atan2(mouse_y - self.rect.centery, mouse_x - self.rect.centerx)
        self.speedx = math.cos(angulo_radianos)
        self.speedy = math.sin(angulo_radianos) 
        
    def update(self):

        #----- VELOCIDADE DA BALA EM DIREÇÃO DO MOUSE
        self.rect.centerx += self.speed * self.speedx
        self.rect.centery += self.speed * self.speedy 

        #----- FAZER A BALA DESAPARECER
        if self.rect.bottom < 0:
            self.kill()
        if self.rect.top > HEIGHT:
            self.kill()
        if self.rect.right > WIDTH:
            self.kill()
        if self.rect.left < 0:
            self.kill ()

#===== CRIANDO MOBS =====
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()

#===== CRIANDO TIROS =====
bullet = Bullet(0, 0, fireball_img)
bullets = pygame.sprite.Group()

#===== CRIANDO O PLAYER =====
player = Player(player_img)
all_sprites.add(player)

#===== SPAWNA MOBS =====
for i in range(15):
    m = Mob(enemy_img)
    while ((m.rect.centerx - player.rect.centerx)**2 + (m.rect.centery - player.rect.centery)**2)**0.5 < 500:
        m = Mob(enemy_img)
    all_sprites.add(m)
    mobs.add(m)

#===== TELA DO JOGO =====
def game_screen(screen):

    #VARIÁVEL AJUSTE DE VELOCIDADE
    clock = pygame.time.Clock()

    #LOOP DO JOGO
    pygame.mixer.music.play(loops=-1)

    DONE = 0
    PLAYING = 1
    EXPLODING = 2
    state = PLAYING
    kills = 0

    #===== LOOP PRINCIPAL DO JOGO =====
    pygame.mixer.music.play(loops=-1)
    while state != DONE:
        clock.tick(FPS)

        #----- TRATA EVENTOS
        for event in pygame.event.get():

            #----- APERTOU QUIT NA ABA
            if event.type == pygame.QUIT:
             state = DONE

            if event.type == pygame.KEYDOWN:

                #----- APERTOU ESC -> FECHA O JOGO
                if event.key == pygame.K_ESCAPE:
                    state = DONE

                #APERTOU BARRA DE ESPAÇ0 -> DASH
                if event.key == pygame.K_SPACE:
                    player.dash()

            #APERTOU O BOTÃO DO MOUSE -> ATIRAR 
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.shoot()
                
        #----- ATUALIZA ESTADO DO JOGO
        #----- ATUALIZANDO POSIÇÃO DOS MOBS
        all_sprites.update()

        if state == PLAYING:
            #----- VERIFICA COLISÃO BALA COM MOB
            hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
            for hit in hits:
                m = Mob(enemy_img)
                while ((m.rect.centerx - player.rect.centerx)**2 + (m.rect.centery - player.rect.centery)**2)**0.5 < 500:
                    m = Mob(enemy_img)
                all_sprites.add(m)
                mobs.add(m)

                #----- CONTA KILLS
                kills += 1
    
        #----- VERIFICA COLISÃO PLAYER COM MOB
        hits = pygame.sprite.spritecollide(player, mobs, False)
        if hits:
            state = DONE


        #----- GERA SAÍDAS
        screen.fill(BLACK)

        #----- DESENHA SPRITES
        all_sprites.draw(screen)

        #----- CONTADOR DE KILLS
        text_surface = font.render("{:08d}".format(kills), True, BLUE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (WIDTH / 2,  10)
        screen.blit(text_surface, text_rect)

        #----- FLIPA E ATUALIZA O DISPLAY
        pygame.display.update()
        pygame.display.flip()

try:
    game_screen(screen)
finally:
    pygame.quit()