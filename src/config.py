import dataclasses
import sys
from pathlib import Path


@dataclasses.dataclass
class Player:
    # Force applied when moving left/right in the air/ground
    move_force_on_ground: int = 1200
    move_force_in_air: int = 600

    # Strength of a jump
    jump_impulse: int = 800

    # Mass of player
    mass: float = 2.0

    asset_path = Path(__file__).parent.parent.resolve() / "assets/Player/"

    # Constants used to track if the player is facing left or right
    right_facing = 0
    left_facing = 1

    # How many pixels to move before we change the texture in the walking animation
    distance_to_change_texture = 10

    scaling = 1


# Close enough to not-moving to have the animation go to idle.
DEAD_ZONE = 0.1
PERPENDICULAR_ZONE = 0.9

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

BOX_PATH = Path(__file__).parent.parent.resolve() / "assets/Box/"

if len(sys.argv) > 1:
    if sys.argv[1].lower() == "true":
        DEBUG = True
