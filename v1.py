import pygame
import random
import math
from os import path
import time

from pygame.constants import KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN, QUIT

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

background = pygame.image.load(path.join(img_dir, 'background.jpg')).convert_alpha()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))


fire_img = pygame.image.load(path.join(img_dir, 'fire.png')).convert_alpha()
fire_img = pygame.transform.scale(fire_img, (25, 25))

fire2_img = pygame.image.load(path.join(img_dir, 'fire2.png')).convert_alpha()
fire2_img = pygame.transform.scale(fire2_img, (25, 25))

player_img = pygame.image.load(path.join(img_dir, 'player.png')).convert_alpha()
player_img = pygame.transform.scale(player_img, (40, 40))

enemy_img = pygame.image.load(path.join(img_dir, 'mob.png')).convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (40, 40))

pygame.mixer.music.load(path.join(snd_dir, 'musica.mp3'))
pygame.mixer.music.set_volume(0.1)

boom_sound = pygame.mixer.Sound(path.join(snd_dir, 'xpld.wav'))
pew_sound = pygame.mixer.Sound(path.join(snd_dir, 'FX294.mp3'))

font = pygame.font.SysFont(None, 48)

#===== ESTRUTURA DE DADOS =====

#------ TEXTO
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


#----- MAIN MENU
click = False
def main_menu():
   
    while True:
        
        screen.fill((0,0,0))
    
 
        mx, my = pygame.mouse.get_pos()
 
        button_1 = pygame.Rect(50, 100, 200, 50)
        button_2 = pygame.Rect(50, 200, 200, 50)

        if button_1.collidepoint((mx, my)):
            if click:
                game_screen(screen)

        if button_2.collidepoint((mx, my)):
            if click:
                pygame.quit()

       
        click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        screen.fill(BLACK)
        screen.blit(background, (0, 0))
        draw_text('main menu', font, (255, 255, 255), screen, 20, 20)
        pygame.draw.rect(screen, (255, 0, 0), button_1)
        pygame.draw.rect(screen, (255, 0, 0), button_2)
        pygame.display.update()

#----- TELA DE MORTE
def morte(kills):
    
    while True:
        
        screen.fill((0,0,0))
    
        screen.blit(background, (0, 0))
        draw_text('Que pena tente novamente! Aperte ESC para sair.', font, (255, 255, 255), screen, 20, 20)
        draw_text('Pontuação: ', font, (255, 255, 255), screen, 50, 50)
        draw_text('{0}'.format(kills), font, (255, 255, 255), screen, 300, 50)
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    
        pygame.display.update()

#----- Player
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

        #----- SET PARA COOLDOWN ATIRAR
        self.last_shot = pygame.time.get_ticks()
        self.shoot_ticks = 500

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

    def shoot(self):
        #----- ATIRAR E COOLDOWN
        now = pygame.time.get_ticks()
        elapsed_ticks = now - self.last_shot
        if elapsed_ticks > self.shoot_ticks:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.centery, fire_img)
            all_sprites.add(bullet)
            bullets.add(bullet)
            pew_sound.play()
            
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

        #----- SET PARA COOLDOWN ATIRAR
        self.last_shot = pygame.time.get_ticks()
        self.shoot_ticks = 300

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

        #----- OLHA NA DIREÇÃO DO PLAYER
        p_x = player.rect.centerx
        p_y = player.rect.centery
        cx = self.rect.centerx
        cy = self.rect.centery
        direcao_x = p_x - cx
        direcao_y = p_y - cy
        angulo_radianos = math.atan2(direcao_y, direcao_x)
        angulo_graus = math.degrees(angulo_radianos)
        angulo_rotacao = -(angulo_graus + 90)
        self.image = pygame.transform.rotate(self.orig_image, angulo_rotacao)
        self.rect = self.image.get_rect()
        self.rect.centerx = cx
        self.rect.centery = cy

        atirar = random.randrange(0, 1000)
        if atirar == 730:
            self.shoot(angulo_radianos)
            self.shoot(angulo_radianos + 1)
            self.shoot(angulo_radianos - 1)
            pew_sound.play()

    def shoot(self, angulo_radianos):
        #----- ATIRAR E COOLDOWN
        bullet = MobBullet(self.rect.centerx, self.rect.centery, angulo_radianos, fire2_img)
        all_sprites.add(bullet)
        mbullets.add(bullet)
        

class Bullet(pygame.sprite.Sprite):

    #----- SPRITE TIRO
    def __init__(self, centerx, centery, fire_img):

        #----- TIRO
        pygame.sprite.Sprite.__init__(self)
        self.image = fire_img
        self.orig_image = fire_img
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

class MobBullet(pygame.sprite.Sprite):
    #----- SPRITE TIRO
    def __init__(self, centerx, centery, angulo, fire_img):

        #----- TIRO
        pygame.sprite.Sprite.__init__(self)
        self.image = fire_img
        self.orig_image = fire_img
        self.rect = self.image.get_rect()
        self.rect.centery = centery
        self.rect.centerx = centerx

        #----- VELOCIDADE DEFAULT
        self.speed = 15
        
        #----- ATIRA 
        self.speedx = math.cos(angulo)
        self.speedy = math.sin(angulo) 
        
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
bullets = pygame.sprite.Group()
mbullets = pygame.sprite.Group()

#===== CRIANDO O PLAYER =====
player = Player(player_img)
all_sprites.add(player)

#===== SPAWNA MOBS =====
for i in range(10):
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
                pygame.quit()

            if event.type == pygame.KEYDOWN:

                #----- APERTOU ESC -> FECHA O JOGO
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

            #APERTOU O BOTÃO DO MOUSE -> ATIRAR 
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.shoot()
                
        #----- ATUALIZA ESTADO DO JOGO
        #----- ATUALIZANDO POSIÇÃO DOS MOBS
        all_sprites.update()

        if state == PLAYING:
            #----- VERIFICA COLISÃO BALA DO PLAYER COM MOB
            hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
            if hits:
                boom_sound.play()
                time.sleep(0.01)
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
                boom_sound.play()
                time.sleep(1)
                state = DONE
                skills = str(kills)
                with open('highscore.txt', 'a') as arquivo:
                    arquivo.write('{0}\n'.format(skills))
                morte(kills)

            #----- VERIFICA COLISÃO BALA DO MOB COM PLAYER
            hits = pygame.sprite.spritecollide(player, mbullets, False)
            if hits:
                boom_sound.play()
                time.sleep(1)
                state = DONE
                skills = str(kills)
                with open('highscore.txt', 'a') as arquivo:
                    arquivo.write('{0}\n'.format(skills))
                morte(kills)

        #----- GERA SAÍDAS
        screen.fill(BLACK)
        screen.blit(background, (0, 0))

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
    main_menu()
finally:
    pygame.quit()
