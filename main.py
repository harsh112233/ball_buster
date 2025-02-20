import pygame
from random import randint
import time
import asyncio

#Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 700
FONT_PATH = "assets/Pixeltype.ttf"
FONT_SIZE = 50
SKY_IMAGE = "assets/sky.png"
GROUND_IMAGE = "assets/ground.png"
PLAYER_IMAGE = "assets/cannon.png"
OBSTACLE_IMAGE = "assets/orca.png"
BULLET_IMAGE = "assets/ball.png"
DIRECTION_IMAGE = "assets/direction.png"

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Ball Buster')
clock = pygame.time.Clock()
font1 = pygame.font.Font(FONT_PATH, FONT_SIZE)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(PLAYER_IMAGE).convert_alpha()
        self.rect = self.image.get_rect(midbottom=(600, 600))

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x += 12
        if keys[pygame.K_LEFT]:
            self.rect.x -= 12

    def update(self):
        self.player_input()

class Obstacles(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(OBSTACLE_IMAGE).convert_alpha()
        self.rect = self.image.get_rect(midbottom=(randint(200,1000), 0))

    def update(self):
        self.rect.y += 8

class Bullets(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(BULLET_IMAGE).convert_alpha()
        self.rect = self.image.get_rect(center=player_ins.rect.center)

    def update(self):
        self.rect.y -= 12
        if self.rect.bottom < 0:
            self.kill()

class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(GROUND_IMAGE).convert_alpha()
        self.rect = self.image.get_rect(topleft =(0, 600))

#Sky surface
sky_surf = pygame.image.load(SKY_IMAGE).convert_alpha()
sky_rect = sky_surf.get_rect(topleft =(0,0))

# Player setup
player = pygame.sprite.GroupSingle()
player_ins = Player()
player.add(player_ins)

#BULLET GROUP
bullet_group = pygame.sprite.Group()

# OBSTACLE Group and setup
obstacle_spawn = pygame.USEREVENT + 1
spawn_delay = 1100
pygame.time.set_timer(obstacle_spawn, spawn_delay)
obstacle_group = pygame.sprite.Group()
game_time = 0

#Ground Groupsingle to detect collision
ground = pygame.sprite.GroupSingle()
ground.add(Ground())

#Other game objects and surfaces
game_active = False
score= 0
miss_count = 0

game_direction_surf = pygame.image.load(DIRECTION_IMAGE).convert_alpha()
game_direction_rect = game_direction_surf.get_rect(midtop = (600, 70))
game_over_surf_1 = font1.render("GAME OVER!!!", True, 'Red')
game_over_rect_1 = game_over_surf_1.get_rect(center=(600, 220))
high_score_surf = font1.render("High Score: 100", True, 'Purple')
high_score_rect = high_score_surf.get_rect(topleft=(900, 25))

# Game loop
running = True

async def main():

    global miss_count
    global score
    global spawn_delay
    global running
    global game_active
    global game_time
    global sky_surf
    global sky_rect
    global obstacle_spawn
    global bullet_group
    global obstacle_group
    global ground
    global screen
    global high_score_surf
    global high_score_rect
    global game_over_surf_1
    global game_over_rect_1
    global game_direction_surf
    global game_direction_rect

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
            if game_active:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    bullet_group.add(Bullets())

                if event.type == obstacle_spawn:
                    obstacle_group.add(Obstacles())
            else: 
                # Start or Restart Game
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        
                        miss_count = 0
                        score= 0
                        spawn_delay= 1100
                        bullet_group.empty()
                        obstacle_group.empty()
                        game_time = 0
                        pygame.time.set_timer(obstacle_spawn, spawn_delay)
                        game_active = True
                        
        if game_active:
            # Increasing spawn rate
            game_time += clock.get_time()
            if game_time >= 4400:
                game_time = 0 
                spawn_delay = max(500, spawn_delay - 100)
                pygame.time.set_timer(obstacle_spawn, spawn_delay)

            # Check for collisions between bullets and obstacles
            collisions = pygame.sprite.groupcollide(bullet_group, obstacle_group, True, True)
            if collisions:
                score += 1
            misses = pygame.sprite.groupcollide(obstacle_group,ground, True, False)
            if misses:
                miss_count += 1

            # Draw ground and sky
            screen.blit(sky_surf, sky_rect)
            ground.draw(screen)
            pygame.draw.rect(screen, 'Pink', high_score_rect)
            screen.blit(high_score_surf,high_score_rect)
            
            #Draw score and miss count
            score_surf = font1.render(f"Score: {score}", True, 'Purple')
            score_rect_2 = score_surf.get_rect(topleft=(35, 25))
            miss_surf = font1.render(f"Miss: {miss_count}/5", True, 'Purple')
            miss_rect = miss_surf.get_rect(topleft=(260, 25))
            pygame.draw.rect(screen, 'Pink', score_rect_2)
            pygame.draw.rect(screen, 'Pink', miss_rect)
            screen.blit(score_surf, score_rect_2)
            screen.blit(miss_surf, miss_rect)
            
            # Draw and update player, bullet, obstacles          
            obstacle_group.draw(screen)
            bullet_group.draw(screen)
            player.draw(screen)
            obstacle_group.update()
            bullet_group.update()
            player.update()

            #Game Over logic
            if miss_count == 5:
                game_active = False

        else:
            screen.blit(sky_surf, (0, 0))
            ground.draw(screen)

            #Show score
            score_surf = font1.render(f"Your Score: {score}   High Score: 100", True, 'Purple')
            score_rect_1 = score_surf.get_rect(center=(600, 270))

            #Game Start Screen
            if miss_count == 0:
                screen.blit( game_direction_surf,game_direction_rect)

            #Restart Game Screen
            if miss_count >= 5:
                screen.blit(game_over_surf_1,game_over_rect_1)
                screen.blit(score_surf, score_rect_1)
                screen.blit( game_direction_surf,game_direction_rect)
                
        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())