import pygame
from random import randint

#Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 700
FONT_PATH = "font/Pixeltype.ttf"
FONT_SIZE = 50
SKY_IMAGE = "Resources/image/sky2.png"
GROUND_IMAGE_1 = "Resources/image/ground.png"
PLAYER_IMAGE = "Resources/image/cannon.png"
OBSTACLE_IMAGE = "Resources/image/orca.png"
BULLET_IMAGE = "Resources/image/ball.png"

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
        self.image = pygame.image.load(GROUND_IMAGE_1).convert_alpha()
        self.rect = self.image.get_rect(topleft =(0, 600))


#Sky and Ground surfaces
sky_surf = pygame.image.load(SKY_IMAGE).convert_alpha()
sky_rect = sky_surf.get_rect(topleft =(0,0))
# ground_surf = pygame.image.load('Resources/image/ground.png').convert_alpha()
# ground_rect = pygame.image.get_rect(ground_surf, topleft =(0, 550))

# Player setup
player = pygame.sprite.GroupSingle()
player_ins = Player()
player.add(player_ins)

#BULLET GROUP
bullet_group = pygame.sprite.Group()

# OBSTACLE Group and setup
obstacle_spawn = pygame.USEREVENT + 1
spawn_delay = 1200
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

game_start_surf = font1.render("Press Space to start Playing", True, 'Purple')
game_start_rect = game_start_surf.get_rect(center = (600, 250))
game_over_surf_1 = font1.render("GAME OVER!!!", True, 'Red')
game_over_surf_2 = font1.render("Press space to start playing", True, 'Purple')
game_over_rect_1 = game_over_surf_1.get_rect(center=(600, 250))
game_over_rect_2 = game_over_surf_2.get_rect(center=(600,350))
high_score_surf = font1.render("High Score: 100", True, 'Purple')
high_score_rect = high_score_surf.get_rect(topleft=(900, 25))

# Game loop
running = True

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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    
                    miss_count = 0
                    score= 0
                    spawn_delay= 1100
                    bullet_group.empty()
                    obstacle_group.empty()
                    game_active = True
                    

    if game_active:
        # Increase spawn rate
        print(spawn_delay)
        
        game_time += clock.get_time()

        if game_time >= 5000:  # Adjust this interval as needed
            game_time = 0  # Reset game time
            spawn_delay = max(600, spawn_delay - 100)  # Decrease delay, but don't go below 200ms
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
        

        # Draw and update player, bullet
        player.draw(screen)
        obstacle_group.draw(screen)
        bullet_group.draw(screen)

        obstacle_group.update()
        bullet_group.update()
        player.update()


        #Game Over logic
        if miss_count == 5:
            game_active = False

    else:
        
        screen.blit(sky_surf, (0, 0))
        ground.draw(screen)
        #Score
        score_surf = font1.render(f"Your Score: {score}   High Score: 100", True, 'Purple')
        score_rect_1 = score_surf.get_rect(center=(600, 300))
        #Game start
        if miss_count == 0:
            screen.blit(game_start_surf, game_start_rect)
        #Restart Game
        if miss_count >= 5:
            screen.blit(game_over_surf_1,game_over_rect_1)
            screen.blit(game_over_surf_2, game_over_rect_2)
            screen.blit(score_surf, score_rect_1)

    pygame.display.update()
    clock.tick(60)

pygame.quit()