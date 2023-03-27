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
    right_facing: int = 0
    left_facing: int = 1

    # How many pixels to move before we change the texture in the walking animation
    distance_to_change_texture: int = 10

    scaling: int = 1

    health: int = 100

    light_radius: int = 100


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

WALL_BULB_RADIUS = (WALL_RIGHT - WALL_LEFT) / 2

# Space in the box row for ease.
FREE_SPACE = 3

GAME_END_TIME = 150

DEBUG = False
PERFORMANCE = False

# time after which the lights go out.
LIGHTS_OUT = 50

BOX_PATH = Path(__file__).parent.parent.resolve() / "assets/Box/"
ASSET_PATH = Path(__file__).parent.parent.resolve() / "assets/"

# Must be greater than 1.
LIGHT_FLICKING_TIME_PERIOD = 2

STORY = \
    f"""
Your school bully Baba, mod-d 5 tetris for you to play. But there was something suspicious about it. Looking at your gestures he said don't be scared Mallo(your name) this is mod-d 5. So you and your friend Pols Agi decided to play the game, little did you know it was a trap and your friend Pols got sucked into the computer screen and now is stuck inside the game.

You currently control him with(A for left, D for right and W for jump). The game's main goal is to survive {GAME_END_TIME} seconds. You will get some extra bonus if you arrange the boxes in a straight line like tetris.
    """

POPCULTURE_REFERENCE = \
    f"""
Popculture references:
+ The "in Ohio" suffix in the game's name is in context with the meme Only in Ohio.
+ Baba, mod-d 5, Mallo and Pols Agi is in context with the Indian meme Pols Agi.
    """

if len(sys.argv) > 1:
    if sys.argv[1].lower() == "true":
        DEBUG = True

if len(sys.argv) > 2:
    if sys.argv[2].lower() == "true":
        PERFORMANCE = True
