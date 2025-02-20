import pygame
from random import randint

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
FONT_PATH = "font/Pixeltype.ttf"
FONT_SIZE = 50
SKY_IMAGE = "Resources/image/sky2.png"
GROUND_IMAGE = "graphics/ground.png"
PLAYER_IMAGE = "Resources/image/cannon.png"
OBSTACLE_IMAGE = "Resources/image/orca.png"
BULLET_IMAGE = "Resources/image/ball.png"

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Ball Buster')
clock = pygame.time.Clock()
font1 = pygame.font.Font(FONT_PATH, FONT_SIZE)

# Load images once (outside the game loop)
sky_surf = pygame.image.load(SKY_IMAGE).convert_alpha()
ground_surf = pygame.image.load(GROUND_IMAGE).convert_alpha()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(PLAYER_IMAGE).convert_alpha()
        self.rect = self.image.get_rect(midbottom=(400, 650))

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
        self.image = pygame.image.load(OBSTACLE_IMAGE).convert_alpha()
        self.rect = self.image.get_rect(midbottom=(randint(50, 750), 0))

    def update(self):
        self.rect.y += 5

class Bullets(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(BULLET_IMAGE).convert_alpha()
        self.rect = self.image.get_rect(center=player_ins.rect.center)

    def update(self):
        self.rect.y -= 9

class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ground_surf
        self.rect = self.image.get_rect(topleft=(0, 650))

# Player setup
player = pygame.sprite.GroupSingle()
player_ins = Player()
player.add(player_ins)

# BULLET GROUP
bullet_group = pygame.sprite.Group()

# OBSTACLE Group
obstacle_spawn = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_spawn, 1100)
obstacle_group = pygame.sprite.Group()

# Ground Groupsingle to detect collision
ground = pygame.sprite.GroupSingle()
ground.add(Ground())

# Other game objects
game_active = False
score = 0
miss_count = 0

# Game loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet_group.add(Bullets())

            if event.type == obstacle_spawn:
                obstacle_group.add(Obstacles())

    if game_active:
        # Check for collisions between bullets and obstacles
        collisions = pygame.sprite.groupcollide(bullet_group, obstacle_group, True, True)
        if collisions:
            score += 1
        misses = pygame.sprite.groupcollide(obstacle_group, ground, True, False)
        if misses:
            miss_count += 1

        # Draw ground and sky
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 650))

        # Draw score and miss count
        score_surf = font1.render(f"Score: {score}", True, 'Purple')
        score_rect = score_surf.get_rect(topleft=(35, 25))
        pygame.draw.rect(screen, 'Pink', score_rect)
        pygame.draw.rect(screen, 'Pink', score_rect, 20)
        screen.blit(score_surf, score_rect)

        miss_surf = font1.render(f"Miss: {miss_count}/5", True, 'Purple')
        miss_rect = miss_surf.get_rect(topleft=(260, 25))
        pygame.draw.rect(screen, 'Pink', miss_rect)
        pygame.draw.rect(screen, 'Pink', miss_rect, 20)
        screen.blit(miss_surf, miss_rect)

        # Draw and update player, bullet, and obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()
        bullet_group.draw(screen)
        bullet_group.update()
        player.draw(screen)
        player.update()
        ground.draw(screen)
        
        # Game Over logic
        if miss_count == 5:
            game_active = False

    else:
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 650))

        # Game start or restart
        if miss_count == 0:
            game_start_surf = font1.render("Press Space to start Playing", True, 'Purple')
            game_start_rect = game_start_surf.get_rect(topleft=(35, 25))
            screen.blit(game_start_surf, game_start_rect)
        else:
            game_over_surf_1 = font1.render("GAME OVER!!!", True, 'Red')
            game_over_surf_2 = font1.render("Press space to start playing", True, 'Purple')
            game_over_rect_1 = game_over_surf_1.get_rect(topleft=(250, 150))
            game_over_rect_2 = game_over_surf_2.get_rect(topleft=(200, 200))
            score_surf = font1.render(f"Score: {score}", True, 'Purple')
            score_rect = score_surf.get_rect(topleft=(250, 100))
            screen.blit(game_over_surf_1, game_over_rect_1)
            screen.blit(game_over_surf_2, game_over_rect_2)
            screen.blit(score_surf, score_rect)

    pygame.display.update()
    clock.tick(60)  # Limit frame rate to 60 FPS

pygame.quit()