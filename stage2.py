import pygame
import random
from game_utils import WIDTH, HEIGHT, PLATFORM_HEIGHT, PLAYER_SIZE, PLAYER_SPEED, JUMP_VELOCITY, GRAVITY, FLAG_SIZE, create_player, handle_movement, handle_collisions, draw

def generate_platforms():
    FLOORS = 15
    GAP_WIDTH = 150
    MIN_GAP_OFFSET = GAP_WIDTH + 20
    vertical_gap = (HEIGHT - 60) // (FLOORS - 1)
    platforms = []
    previous_gap_x = None

    ground_y = HEIGHT - 40
    ground_platform = pygame.Rect(0, ground_y, WIDTH, PLATFORM_HEIGHT)
    platforms.append(ground_platform)

    highest_left_platform = None
    highest_right_platform = None
    for i in range(1, FLOORS):
        y = HEIGHT - 40 - i * vertical_gap
        min_x = WIDTH // 6
        max_x = WIDTH - WIDTH // 6 - GAP_WIDTH
        while True:
            gap_x = random.randint(min_x, max_x)
            if previous_gap_x is None or abs(gap_x - previous_gap_x) >= MIN_GAP_OFFSET:
                break
        previous_gap_x = gap_x
        left_platform = pygame.Rect(0, y, gap_x, PLATFORM_HEIGHT)
        platforms.append(left_platform)
        right_platform = pygame.Rect(
            gap_x + GAP_WIDTH, y, WIDTH - (gap_x + GAP_WIDTH), PLATFORM_HEIGHT)
        platforms.append(right_platform)
        if i == FLOORS - 1:
            highest_left_platform = left_platform
            highest_right_platform = right_platform

    flag_platform = highest_left_platform if highest_left_platform.width >= highest_right_platform.width else highest_right_platform
    flag_x = flag_platform.centerx - FLAG_SIZE // 2
    flag_y = flag_platform.top - FLAG_SIZE
    flag = pygame.Rect(flag_x, flag_y, FLAG_SIZE, FLAG_SIZE)

    return platforms, flag

def run_stage(screen, clock, player, platforms, flag):
    vel_y = 0
    on_ground = False
    running = True

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, player

        keys = pygame.key.get_pressed()
        prev_bottom = player.bottom
        vel_y, on_ground = handle_movement(player, keys, vel_y, on_ground)
        vel_y, on_ground = handle_collisions(
            player, platforms, vel_y, prev_bottom, on_ground)

    
        if player.colliderect(flag):
            return True, player

        draw(screen, player, platforms, flag)

    return False, player







