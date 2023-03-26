import random

import arcade
import pymunk

import config
from sprites import Box


class Game(arcade.Window):
    def __init__(self):
        super().__init__(config.SCREEN_WIDTH, config.SCREEN_HEIGHT, title='Tetris in Ohio')
        arcade.set_background_color(arcade.color.STORMCLOUD)

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False
        self.funeral = False
        self.score = None

        self.score_text: arcade.Text = None
        self.health_text: arcade.Text = None

        # Separate variable that holds the player sprite
        # self.player_sprite: PlayerCharacter = None
        self.player_sprite_list: arcade.SpriteList = None

        self.platform_sprite_list: arcade.SpriteList = None

        self.boxes_sprite_list: arcade.SpriteList = None

        # Our 'physics' engine
        self.physics_engine: arcade.PymunkPhysicsEngine = None

        self.box_center_y_list = None
        self.box_center_x_list = None

        arcade.schedule(self.add_box, interval=5)

    def setup(self, _delta_time=config.DEAD_ZONE):
        self.physics_engine = arcade.PymunkPhysicsEngine(gravity=(0.0, -900.0), damping=1)

        self.boxes_sprite_list = arcade.SpriteList()
        self.box_center_y_list = []
        self.box_center_x_list = list(range(
            int(config.WALL_LEFT + config.BOX_SIZE / 2),
            int(config.WALL_RIGHT + config.BOX_SIZE / 2), config.BOX_SIZE)
        )
        
        self.platform_sprite_list = arcade.SpriteList(use_spatial_hash=True)
        for i in range(config.SCREEN_WIDTH // config.BOX_SIZE + 1):
            platform_grass = arcade.Sprite(":resources:images/tiles/brickBrown.png", scale=config.BOX_SIZE / 128)
            platform_grass.center_y = 80
            platform_grass.center_x = config.BOX_SIZE*i
            self.platform_sprite_list.append(platform_grass)

        for i in range(320 // config.BOX_SIZE + 1):
            center_y = 112 + config.BOX_SIZE * i
            platform_grass = arcade.Sprite(":resources:images/tiles/brickBrown.png", scale=config.BOX_SIZE / 128)
            platform_grass.center_y = center_y
            platform_grass.center_x = config.WALL_LEFT - config.BOX_SIZE / 2 - config.FREE_SPACE
            self.platform_sprite_list.append(platform_grass)

            platform_grass = arcade.Sprite(":resources:images/tiles/brickBrown.png", scale=config.BOX_SIZE / 128)
            platform_grass.center_y = center_y
            platform_grass.center_x = config.WALL_RIGHT + config.BOX_SIZE / 2 + config.FREE_SPACE
            self.platform_sprite_list.append(platform_grass)

            self.box_center_y_list.append(center_y)

        self.physics_engine.add_sprite_list(
            self.platform_sprite_list,
            mass=1.0,
            friction= config.GROUND_FRICTION / 3,
            elasticity=0.5,
            body_type=pymunk.Body.STATIC,
            collision_type="wall",
        )

    def on_draw(self):
        self.clear()

        # self.camera.use()
        # self.player_sprite_list.draw()
        # Activate the GUI camera before drawing GUI elements
        # self.gui_camera.use()
        self.boxes_sprite_list.draw()
        self.platform_sprite_list.draw()

    def add_box(self, _delta_time):
        if len(self.boxes_sprite_list) > 150:
            return
        sprite = Box(f"{config.BOX_PATH}/boxCrate_{random.randrange(0, 3)}.png")
        sprite.center_x = random.randrange(int(config.WALL_LEFT), int(config.WALL_RIGHT))
        sprite.center_y = 500
        self.physics_engine.add_sprite(
            sprite,
            mass=1.0,
            friction=config.GROUND_FRICTION,
            elasticity=0.5,
            moment_of_inertia=pymunk.moment_for_box(1.0, (config.BOX_SIZE, config.BOX_SIZE)),
            collision_type="box",
        )
        self.boxes_sprite_list.append(sprite)

    def on_update(self, delta_time: float):
        # self.process_keychange()
        self.physics_engine.step(1 / 60.0)


def main():
    game = Game()
    game.setup()
    game.run()


if __name__ == '__main__':
    main()
