import pygame
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Resources/image/cannon.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(400, 520))

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x += 10
        if keys[pygame.K_LEFT]:
            self.rect.x -= 10

    def update(self):
        self.player_input()

class Obstacles(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(randint(50,750), 0))

    def update(self):
        self.rect.y += 5

class Bullets(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Resources/image/ball.png').convert_alpha()
        self.rect = self.image.get_rect(center=player_ins.rect.center)

    def update(self):
        self.rect.y -= 9

class Ground(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load('graphics/ground.png').convert_alpha()
            self.rect = self.image.get_rect(topleft= (0, 520))
# Pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 640))
pygame.display.set_caption('Ball oo Buster')
clock = pygame.time.Clock()
font1 = pygame.font.Font("font/Pixeltype.ttf", 50)

# Player setup
player = pygame.sprite.GroupSingle()
player_ins = Player()
player.add(player_ins)

ground = pygame.sprite.GroupSingle()
ground.add(Ground())

# Surfaces and rectangles
sky_surf = pygame.image.load('Resources/image/sky2.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()
count= 0
miss_count = 0
# score_surf = font1.render(f"Score: {count}", True, 'Purple')
# score_rect = score_surf.get_rect(topleft=(35, 25))

#BULLET GROUP
bullet_group = pygame.sprite.Group()

# OBSTACLE SETUP
obstacle_spawn = pygame.USEREVENT + 2
pygame.time.set_timer(obstacle_spawn,1100)
obstacle_group = pygame.sprite.Group()

# Game loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Post the custom event when spacebar is pressed
                bullet_group.add(Bullets())

        if event.type == obstacle_spawn:
            obstacle_group.add(Obstacles())

    # Check for collisions between bullets and obstacles
    collisions = pygame.sprite.groupcollide(bullet_group, obstacle_group, True, True)
    if collisions:
        count += 1
    misses = pygame.sprite.groupcollide(obstacle_group,ground, True, False)
    if misses:
        miss_count += 1
    # Draw everything
    screen.blit(sky_surf, (0, 0))
    score_surf = font1.render(f"Score: {count}", True, 'Purple')
    score_rect = score_surf.get_rect(topleft=(35, 25))
    pygame.draw.rect(screen, 'Pink', score_rect)
    pygame.draw.rect(screen, 'Pink', score_rect, 20)
    screen.blit(score_surf, score_rect)

    miss_surf = font1.render(f"Miss: {miss_count}", True, 'Purple')
    miss_rect = miss_surf.get_rect(topleft=(260, 25))
    pygame.draw.rect(screen, 'Pink', miss_rect)
    pygame.draw.rect(screen, 'Pink', miss_rect, 20)
    screen.blit(miss_surf, miss_rect)

    # Draw and update player
    obstacle_group.draw(screen)
    obstacle_group.update()
    bullet_group.draw(screen)
    bullet_group.update()
    player.draw(screen)
    player.update()
    ground.draw(screen)
    # print(count)
    # Update the display
    pygame.display.update()
    clock.tick(60)

pygame.quit()