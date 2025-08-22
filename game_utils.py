import pygame

# Configura
WIDTH, HEIGHT = 640, 720
PLATFORM_HEIGHT = 10
PLAYER_SIZE = 30
PLAYER_SPEED = 5
JUMP_VELOCITY = -18
GRAVITY = 1
FLAG_SIZE = 20


def create_player():
    ground_y = HEIGHT - 40
    player_start_x = WIDTH // 2 - PLAYER_SIZE // 2
    player_start_y = ground_y - PLAYER_SIZE
    return pygame.Rect(player_start_x, player_start_y, PLAYER_SIZE, PLAYER_SIZE)


def handle_movement(player, keys, vel_y, on_ground):
    # Horizontal movement
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.x += PLAYER_SPEED

    # Gravity
    vel_y += GRAVITY
    player.y += vel_y

    # Jump
    if keys[pygame.K_SPACE] and on_ground:
        vel_y = JUMP_VELOCITY

    # Horizontal boundaries
    if player.left < 0:
        player.left = 0
    if player.right > WIDTH:
        player.right = WIDTH

    return vel_y, False


def handle_collisions(player, platforms, vel_y, prev_bottom, on_ground):
    for plat in platforms:
        if player.colliderect(plat):
            # Landing on platform from above
            if vel_y >= 0 and prev_bottom <= plat.top < player.bottom:
                player.bottom = plat.top
                vel_y = 0
                on_ground = True
            # Hitting platform from below
            elif vel_y < 0 and prev_bottom >= plat.bottom > player.top:
                player.top = plat.bottom
                vel_y = 0
    return vel_y, on_ground


def draw(screen, player, platforms, flag):
    screen.fill((50, 50, 100))
    camera_y = player.centery - HEIGHT // 2
    for plat in platforms:
        pygame.draw.rect(screen, (150, 200, 255), plat.move(0, -camera_y))
    pygame.draw.rect(screen, (255, 100, 100), player.move(0, -camera_y))
    pygame.draw.rect(screen, (255, 255, 0), flag.move(0, -camera_y))
    pygame.display.flip()


def show_transition(screen, message):
    font = pygame.font.SysFont(None, 48)
    text = font.render(message, True, (255, 255, 255))
    screen.fill((0, 0, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() //
                2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.event.clear()
    pygame.time.delay(1000)


def wait_for_quit(screen, clock):
    font = pygame.font.SysFont(None, 48)
    text = font.render("YOU WIN!", True, (255, 255, 255))
    screen.fill((0, 0, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() //
                2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
        clock.tick(30)

