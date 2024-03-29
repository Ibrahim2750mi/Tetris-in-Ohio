import random

import arcade
import pymunk
from arcade.experimental.lights import Light, LightLayer

import config
from sprites import Box, PlayerCharacter
from views import Aftermath


class Game(arcade.View):
    def __init__(self, start_bg_player):
        super().__init__()
        arcade.set_background_color(arcade.color.STORMCLOUD)

        self.start_bg_player = start_bg_player

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
        self.timer_text: arcade.Text = None

        self.total_game_time: int = 0
        self.reset_cooldown: int = 0

        # Separate variable that holds the player sprite
        self.player_sprite: PlayerCharacter = None
        self.player_sprite_list: arcade.SpriteList = None
        self.player_light: Light = None

        self.wall_bulb_left: Light = None
        self.wall_bulb_right: Light = None

        self.platform_sprite_list: arcade.SpriteList = None

        self.boxes_sprite_list: arcade.SpriteList = None

        # Our 'physics' engine
        self.physics_engine: arcade.PymunkPhysicsEngine = None

        self.box_center_y_list = None
        self.box_center_x_list = None

        self.light_layer: LightLayer = None

        self.switch_on_sound = arcade.load_sound(config.ASSET_PATH / "switch_on.wav")
        self.switch_off_sound = arcade.load_sound(config.ASSET_PATH / "switch_off.wav")

        self.dies_irae_sound = arcade.load_sound(config.ASSET_PATH / "dies_irae_f2.wav")
        self.dies_irae_player = None

        self.bg_music = arcade.load_sound(config.ASSET_PATH / r"01.A-Creepy-Intro.ogg", streaming=True)
        self.bg_player = None

        arcade.schedule(self.add_box, interval=5)

        # debug section
        self.fps_text: arcade.Text = None
        self.debug_list = None

    def add_box(self, _delta_time):
        if len(self.boxes_sprite_list) > 150:
            return
        sprite = Box(f"{config.BOX_PATH}/boxCrate_{random.randrange(0, 3)}.png")
        sprite.center_x = random.randrange(int(config.WALL_LEFT), int(config.WALL_RIGHT))
        sprite.center_y = config.BOX_DROP_HEIGHT
        self.physics_engine.add_sprite(
            sprite,
            mass=1.0,
            friction=config.GROUND_FRICTION,
            elasticity=0.5,
            moment_of_inertia=pymunk.moment_for_box(1.0, (config.BOX_SIZE, config.BOX_SIZE)),
            collision_type="box",
        )
        self.boxes_sprite_list.append(sprite)
        if not self.player_sprite.dead:
            self.score += 10
            self.score_text.text = f"Score: {self.score}"

    def start_timer(self, delta_time):
        self.total_game_time += delta_time
        self.timer_text.text = f"Time left to survive: {int(config.GAME_END_TIME - self.total_game_time)}"

        self.reset_cooldown -= delta_time

        if int(config.GAME_END_TIME - self.total_game_time) < 0:
            self.window.show_view(Aftermath(self.score, True))
        elif self.total_game_time > config.LIGHTS_OUT:
            if self.player_light not in self.light_layer:
                self.light_layer.add(self.player_light)

                arcade.stop_sound(self.start_bg_player)
                self.bg_player = arcade.play_sound(self.bg_music, looping=True, volume=0.025)

            if int(self.total_game_time) % config.LIGHT_FLICKING_TIME_PERIOD != 0:
                return
            if self.wall_bulb_left in self.light_layer:
                arcade.play_sound(self.switch_off_sound, volume=0.2 )
                self.light_layer.remove(self.wall_bulb_left)
                self.light_layer.remove(self.wall_bulb_right)
            else:
                arcade.play_sound(self.switch_on_sound, volume=0.2)
                self.light_layer.add(self.wall_bulb_left)
                self.light_layer.add(self.wall_bulb_right)

    def game_over(self, _delta_time):
        arcade.stop_sound(self.bg_player)
        self.window.show_view(Aftermath(self.score, False, self.dies_irae_player))

    def setup(self, _delta_time=config.DEAD_ZONE):
        self.funeral = False
        self.total_game_time = 0
        self.reset_cooldown: int = 0
        arcade.schedule(self.start_timer, interval=1)

        self.physics_engine = arcade.PymunkPhysicsEngine(gravity=(0.0, -900.0), damping=1)
        self.player_sprite = PlayerCharacter()
        self.physics_engine.add_sprite(
            self.player_sprite,
            mass=config.Player.mass,
            moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF,
            collision_type="player",
            friction=1,
            damping=0.4,
        )

        self.player_sprite_list = arcade.SpriteList()
        self.player_sprite_list.append(self.player_sprite)

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
            platform_grass.center_x = config.BOX_SIZE * i
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
            friction=config.GROUND_FRICTION / 3,
            elasticity=0.5,
            body_type=pymunk.Body.STATIC,
            collision_type="wall",
        )

        def enable_pushing(player_sprite, _box_sprite, arbiter, _space, _data):
            original_pushing = player_sprite.pushing
            if abs(arbiter.normal.x) > config.DEAD_ZONE:
                player_sprite.pushing = True

            if arbiter.normal.y < -config.PERPENDICULAR_ZONE / 2:
                # above the box
                if not (original_pushing == player_sprite.pushing):
                    player_sprite.pushing = False
                if player_sprite.jumping:
                    self.score += 10
            elif arbiter.normal.y > config.PERPENDICULAR_ZONE:
                # below the box
                player_sprite.crushed = True
                if not (original_pushing == player_sprite.pushing):
                    player_sprite.pushing = False
            return True

        def disable_pushing(player_sprite, _box_sprite, _arbiter, _space, _data):
            if player_sprite.crushed:
                player_sprite.health -= 10
                self.health_text.text = f"Player health: {self.player_sprite.health}"
                if config.DEBUG:
                    print(f"Player took heavy damage. Current health: {player_sprite.health}")
            player_sprite.crushed = False
            player_sprite.pushing = False

        self.physics_engine.add_collision_handler(
            "player",
            "box",
            pre_handler=enable_pushing,
            separate_handler=disable_pushing,
        )

        self.score = 0

        self.score_text = arcade.Text(
            text=f"Score: {self.score}", start_x=10, start_y=config.SCREEN_HEIGHT - 30
        )
        self.health_text = arcade.Text(
            text=f"Player health: {self.player_sprite.health}", start_x=10, start_y=config.SCREEN_HEIGHT - 50
        )

        self.timer_text = arcade.Text(
            text=f"Time left to survive: {config.GAME_END_TIME}",
            start_x=config.SCREEN_WIDTH - 200,
            start_y=config.SCREEN_HEIGHT - 30,
        )

        self.light_layer = LightLayer(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        # We can also set the background color that will be lit by lights,
        # but in this instance we just want a black background
        self.light_layer.set_background_color(arcade.color.BLACK)

        self.player_light = Light(0, 0, config.Player.light_radius, arcade.csscolor.WHITE, "soft")
        y = self.box_center_y_list[-1]
        self.wall_bulb_left = Light(config.WALL_LEFT, y, config.WALL_BULB_RADIUS, arcade.csscolor.WHITE, "soft")
        self.wall_bulb_right = Light(config.WALL_RIGHT, y, config.WALL_BULB_RADIUS, arcade.csscolor.WHITE, "soft")

        if not config.DEBUG:
            return

        self.debug_list = []
        for x in self.box_center_x_list:
            for y in self.box_center_y_list:
                self.debug_list.append(arcade.shape_list.create_rectangle(
                    x, y - config.BOX_SIZE / 2 + config.FREE_SPACE, 2, 2, color=arcade.color.RED)
                )

        self.fps_text = arcade.Text(
            text="FPS: 60", start_x=10, start_y=config.SCREEN_HEIGHT - 70
        )
        self.debug_list.append(self.fps_text)

        self.total_game_time: int = 0

    def on_draw(self):
        self.clear()

        if self.total_game_time > config.LIGHTS_OUT:
            with self.light_layer:
                self.player_sprite_list.draw()
                self.boxes_sprite_list.draw()
                self.platform_sprite_list.draw()
            # Draw the light layer to the screen.
            # This fills the entire screen with the lit version
            # of what we drew into the light layer above.
            self.light_layer.draw(ambient_color=(3, 3, 3))
        else:
            self.player_sprite_list.draw()
            self.boxes_sprite_list.draw()
            self.platform_sprite_list.draw()

        self.score_text.draw()
        self.health_text.draw()
        self.timer_text.draw()

        if not config.DEBUG:
            return
        for rect in self.debug_list:
            rect.draw()

        arcade.draw_lines(self.player_sprite.get_adjusted_hit_box(), color=arcade.color.RED)

    def on_show_view(self):
        self.setup()

    def process_keychange(self):
        """
        Called when we change a key up/down or we move on/off a ladder.
        """
        if self.funeral:
            return

        # Process up/down
        if self.up_pressed and not self.down_pressed:
            if (
                    self.physics_engine.is_on_ground(self.player_sprite)
                    and not self.player_sprite.jumping
            ):
                force = (0, config.Player.jump_impulse)
                self.physics_engine.apply_impulse(self.player_sprite, force)
                # Set friction to zero for the player while moving
                self.physics_engine.set_friction(self.player_sprite, 0)
                self.player_sprite.jumping = True
        else:
            # Player's feet are not moving. Therefore up the friction so we stop.
            self.physics_engine.set_friction(self.player_sprite, 1.0)

        # Process left/right
        if self.left_pressed and not self.right_pressed:
            # Create a force to the left. Apply it.
            force = (-config.Player.move_force_on_ground, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            # Set friction to zero for the player while moving
            self.physics_engine.set_friction(self.player_sprite, 0)
        elif self.right_pressed and not self.left_pressed:
            # Create a force to the right. Apply it.
            force = (config.Player.move_force_on_ground, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            # Set friction to zero for the player while moving
            self.physics_engine.set_friction(self.player_sprite, 0)
        else:
            # Player's feet are not moving. Therefore up the friction so we stop.
            self.physics_engine.set_friction(self.player_sprite, 1.0)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.P:
            self.player_sprite.pulling = not self.player_sprite.pulling
        elif key == arcade.key.R:
            if self.reset_cooldown <= 0:
                self.reset_cooldown += config.RESET_COOLDOWN
                self.physics_engine.set_position(self.player_sprite, (
                    config.WALL_LEFT + (config.WALL_RIGHT - config.WALL_LEFT) / 2,
                    config.BOX_DROP_HEIGHT - config.BOX_SIZE / 2,
                    ),
                )

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

    def on_update(self, delta_time: float):
        self.process_keychange()
        self.physics_engine.step(1 / 60.0)

        self.player_light.position = self.player_sprite.position

        if self.player_sprite.dead and not self.funeral:
            self.player_sprite.texture = \
                self.player_sprite.death_textures[9][self.player_sprite.character_face_direction]
            self.add_box(delta_time)
            self.physics_engine.remove_sprite(self.player_sprite)
            self.funeral = True

            if self.wall_bulb_left in self.light_layer:
                arcade.play_sound(self.switch_off_sound, volume=0.2)
                self.light_layer.remove(self.wall_bulb_left)
                self.light_layer.remove(self.wall_bulb_right)

            arcade.unschedule(self.start_timer)
            arcade.schedule_once(self.game_over, 5)
            player = self.start_bg_player
            if self.bg_player:
                player = self.bg_player
            arcade.stop_sound(player)
            self.dies_irae_player = arcade.play_sound(self.dies_irae_sound, looping=True, volume=0.2)

        if self.funeral:
            self.add_box(delta_time)
            for sprite in self.boxes_sprite_list:
                if self.physics_engine.get_physics_object(sprite).body.position.y < 0:
                    sprite.remove_from_sprite_lists()
            return

        self.check_straight_line()

        if not config.DEBUG:
            return

        if int(self.total_game_time) % 3 == 0:
            self.fps_text.text = f"FPS: {int(1 / delta_time) + 1}"

    def check_straight_line(self):
        for y in self.box_center_y_list.copy():
            sprites_line = []
            for x in self.box_center_x_list.copy():
                sprites = arcade.get_sprites_at_point(
                    (x, y - config.BOX_SIZE / 2 + config.FREE_SPACE),
                    self.boxes_sprite_list
                )
                if not sprites:
                    return
                sprites_line.extend(sprites)
            if not sprites_line:
                return
            if len(sprites_line) == 7:
                self.box_center_y_list.remove(y)

                self.score += 100
                self.score_text.text = f"Score: {self.score}"

                for box in sprites_line:
                    box.react_to_player = False
                    # To improve performance.
                    if config.PERFORMANCE:
                        self.physics_engine.remove_sprite(box)
                        self.physics_engine.add_sprite(
                            box,
                            mass=1.0,
                            friction=config.GROUND_FRICTION / 3,
                            elasticity=0.5,
                            body_type=pymunk.Body.STATIC,
                            collision_type="wall",
                        )
                if config.DEBUG:
                    print(f"DAMN! You got 7 in a row, current score {self.score}")
                return
