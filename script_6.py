import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 640))
pygame.display.set_caption('Ball oo Buster')
clock = pygame.time.Clock()
font1 = pygame.font.Font("font/Pixeltype.ttf", 50)

running = True
dt = 0

# <==Creating surfaces and rectangles==>
sky_surf = pygame.image.load('Resources/image/sky2.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

score_surf = font1.render("Score", True, 'Purple')
score_rect = score_surf.get_rect(topleft=(35, 25))

cannon_surf = pygame.image.load('Resources/image/cannon2.png').convert_alpha()
cannon_rect = cannon_surf.get_rect(midbottom=(400, 520))

ball_surf = pygame.image.load('Resources/image/ball.png').convert_alpha()

snail_surf = pygame.image.load('graphics/snail/snail1.png')
snail_rect = snail_surf.get_rect(midbottom=(400, 100))

angle = 1
temp_angle = 2
visible = True

# List to store active cannonballs
bullets = []


def shoot():
    # Create a new cannonball at the cannon's position
    new_ball = {
        "rect": ball_surf.get_rect(midbottom=cannon_rect.midtop),
        "active": True,
    }
    bullets.append(new_ball)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # <=== Attaching surfaces on screen ===>
    screen.blit(sky_surf, (0, 0))
    pygame.draw.rect(screen, 'Pink', score_rect)
    pygame.draw.rect(screen, 'Pink', score_rect, 20)
    screen.blit(score_surf, score_rect)

    # Update and draw snail
    if visible:
        screen.blit(snail_surf, snail_rect)
        snail_rect.y += 3
        if snail_rect.y >= 500:
            snail_rect.y = 50

    # Rotate cannon
    if angle > 70:
        temp_angle = -4
    if angle < -70:
        temp_angle = 4
    angle += temp_angle
    rotated_cannon = pygame.transform.rotate(cannon_surf, angle)
    rotated_cannon_rect = rotated_cannon.get_rect(center=cannon_rect.midbottom)
    screen.blit(rotated_cannon, rotated_cannon_rect)

    # Handle cannon movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        cannon_rect.x += 10
    if keys[pygame.K_LEFT]:
        cannon_rect.x -= 10

    # Shoot cannonball when spacebar is pressed
    if keys[pygame.K_SPACE]:
        shoot()

    # Update and draw cannonballs
    for bullet in bullets:
        if bullet["active"]:
            # Move the cannonball upward
            bullet["rect"].y -= 15
            screen.blit(ball_surf, bullet["rect"])

            # Check for collision with snail
            if bullet["rect"].colliderect(snail_rect):
                visible = False
                bullet["active"] = False  # Deactivate the cannonball

            # Deactivate cannonball if it goes off-screen
            if bullet["rect"].bottom < 0:
                bullet["active"] = False

    # Remove inactive cannonballs
    bullets = [bullet for bullet in bullets if bullet["active"]]

    # Draw ground
    screen.blit(ground_surf, (0, 520))

    pygame.display.update()
    clock.tick(60)

pygame.quit()