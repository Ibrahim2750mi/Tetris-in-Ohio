import sys
from pathlib import Path


PLAYER_MOVE_FORCE_ON_GROUND = 1200
# Force applied when moving left/right in the air
PLAYER_MOVE_FORCE_IN_AIR = 600

# Strength of a jump
PLAYER_JUMP_IMPULSE = 600

# Close enough to not-moving to have the animation go to idle.
DEAD_ZONE = 0.1
PERPENDICULAR_ZONE = 0.9

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

# How many pixels to move before we change the texture in the walking animation
DISTANCE_TO_CHANGE_TEXTURE = 10

CHARACTER_SCALING = 1

# Friction for ground.
GROUND_FRICTION = 0.5

BOX_SIZE = 32
# Number of boxes required in a row to score.
BOX_ROW_COUNT = 7

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Tetris wall boundaries
WALL_LEFT = SCREEN_WIDTH / 2 - (BOX_ROW_COUNT * BOX_SIZE) / 2
WALL_RIGHT = SCREEN_WIDTH / 2 + (BOX_ROW_COUNT * BOX_SIZE) / 2

# Space in the box row for ease.
FREE_SPACE = 3

DEBUG = False

BOX_PATH = Path.cwd() / "../assets/Box/"

if len(sys.argv) > 1:
    if sys.argv[1].lower() == "true":
        DEBUG = True
