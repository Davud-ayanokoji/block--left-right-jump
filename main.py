import pygame
import sys
from stage1 import generate_platforms as generate_stage1_platforms, run_stage as run_stage1
from stage2 import generate_platforms as generate_stage2_platforms, run_stage as run_stage2
from game_utils import create_player, show_transition, wait_for_quit

pygame.init()
screen = pygame.display.set_mode((640, 720))
pygame.display.set_caption("Block Jump Up")
clock = pygame.time.Clock()

# Pre-generate platforms for both stages
stage1_platforms, stage1_flag = generate_stage1_platforms()
stage2_platforms, stage2_flag = generate_stage2_platforms()

# Create player
player = create_player()

# Run Stage 1
success, player = run_stage1(
    screen, clock, player, stage1_platforms, stage1_flag)
if not success:
    pygame.quit()
    sys.exit()

# Show transition and reset player position
show_transition(screen, "Stage 1 Complete")
player = create_player()  # Reset player to ground level for Stage 2

# Run Stage 2
success, player = run_stage2(
    screen, clock, player, stage2_platforms, stage2_flag)
if not success:
    pygame.quit()
    sys.exit()

# Show win screen
show_transition(screen, "Stage 2 Complete")
wait_for_quit(screen, clock)
pygame.quit()
sys.exit()
