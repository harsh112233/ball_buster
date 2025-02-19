import pygame
from random import randint

#Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 700
FONT_PATH = "font/Pixeltype.ttf"
FONT_SIZE = 50
SKY_IMAGE = "Resources/image/sky2.png"
GROUND_IMAGE_1 = "graphics/ground.png"
PLAYER_IMAGE = "Resources/image/cannon.png"
OBSTACLE_IMAGE = "Resources/image/orca.png"
BULLET_IMAGE = "Resources/image/ball.png"

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Ball Buster')
clock = pygame.time.Clock()
font1 = pygame.font.Font(FONT_PATH, FONT_SIZE)


sky_surf = pygame.image.load(SKY_IMAGE).convert_alpha()
sky_rect = sky_surf.get_rect(topleft =(0,0) )
ground_surf = pygame.image.load('Resources/image/ground.png').convert_alpha()
ground_rect = ground_surf.get_rect(topleft =(0, 550))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.blit(sky_surf, sky_rect)
    screen.blit(ground_surf, ground_rect)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
