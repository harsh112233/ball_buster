# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 640))
pygame.display.set_caption('Ball oo Buster')
clock = pygame.time.Clock()
font1 = pygame.font.Font("font/Pixeltype.ttf", 50)

running = True

# <==Creating surfaces and rectangles==>
sky_surf = pygame.image.load('Resources/image/sky2.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

score_surf = font1.render("Score", True, 'Purple')
score_rect = score_surf.get_rect(topleft= (35,25))

cannon_surf = pygame.image.load('Resources/image/cannon2.png').convert_alpha()
cannon_rect = cannon_surf.get_rect(midbottom= (400,520))

ball_surf = pygame.image.load('Resources/image/ball.png').convert_alpha()
ball_rect = ball_surf.get_rect(midbottom= (400,425))

snail_surf = pygame.image.load('graphics/snail/snail1.png')
snail_rect = snail_surf.get_rect(midbottom = (400,100))

angle = 1
temp_angle = 2
state = "inactive"
visible = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # <=== Attaching surfaces on screen ===>
    screen.blit(sky_surf,(0,0))
    # screen.blit(ground_surf,(0,520))
    pygame.draw.rect(screen,'Pink', score_rect)
    pygame.draw.rect(screen,'Pink', score_rect, 20)
    screen.blit(score_surf, score_rect)


    if visible == True:
        screen.blit(snail_surf,snail_rect)
        snail_rect.y += 3
        if snail_rect.y >= 500: snail_rect.y = 50
    if visible == False:
        visible = True
        snail_rect.y = 50

    if angle > 70: temp_angle = -4
    if angle < -70: temp_angle = 4
    angle = (angle + temp_angle)
    rotated_cannon = pygame.transform.rotate(cannon_surf, angle)
    rotated_cannon_rect = rotated_cannon.get_rect(center=cannon_rect.midbottom)
    screen.blit(rotated_cannon,rotated_cannon_rect)

    if ball_rect.colliderect(snail_rect):
        visible = False
        # state = "inactive"

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        state = "active"
    if state == "active":
        screen.blit(ball_surf,ball_rect)
        ball_rect.y -= 15
        if ball_rect.y <= -30:
            state = "inactive"
            ball_rect.y = 430

    if keys[pygame.K_RIGHT]:
        cannon_rect.x += 10
    if keys[pygame.K_LEFT]:
        cannon_rect.x -= 10
    ball_rect.x = cannon_rect.x


    screen.blit(ground_surf, (0, 520))
    pygame.display.update()
    clock.tick(60)


pygame.quit()