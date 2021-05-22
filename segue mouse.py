import math
import pygame

pygame.init()
window = pygame.display.set_mode((1500, 1000))
player = pygame.image.load("heejina.gif").convert_alpha()

#   0 - image is looking to the right
#  90 - image is looking up
# 180 - image is looking to the left
# 270 - image is looking down
correction_angle = 90

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    player_pos  = window.get_rect().center
    player_rect = player.get_rect(center = player_pos)

    mx, my = pygame.mouse.get_pos()
    dx, dy = mx - player_rect.centerx, my - player_rect.centery
    angle = math.degrees(math.atan2(-dy, dx)) - correction_angle

    rot_image      = pygame.transform.rotate(player, angle)
    rot_image_rect = rot_image.get_rect(center = player_rect.center)

    window.fill((255, 255, 255))
    window.blit(rot_image, rot_image_rect.topleft)
    pygame.display.flip()

pygame.quit()
exit()