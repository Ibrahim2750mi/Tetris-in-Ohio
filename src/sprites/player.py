import arcade

import config
from config import Player


class PlayerCharacter(arcade.Sprite):
    """Player Sprite"""

    def __init__(self):
        super().__init__()

        self.center_x = 400
        self.center_y = 300

        # Default to face-right
        self.character_face_direction = Player.right_facing

        # Used for flipping between image sequences
        self.cur_texture = 0
        self.jump_cycles = 0
        self.hurt_cycles = 0
        self.death_cycles = 0
        self.idling_cycles = 0
        self.scale = Player.scaling

        # Track our state
        self.jumping = False
        self.pushing = False
        self.can_push = False
        self.crushed = False
        self.health = 100
        self.dead = False

        # --- Load Textures ---

        # Load textures for jumping
        self.jump_textures = []
        for i in range(3):
            texture = arcade.load_texture_pair(
                Player.asset_path / f"Jump_48x48_{i}.png",
                arcade.hitbox.PymunkHitBoxAlgorithm()
            )
            self.jump_textures.append(texture)

        # Load textures for running
        self.run_textures = []
        for i in range(8):
            texture = arcade.load_texture_pair(
                Player.asset_path / f"Run_48x48_{i}.png",
                arcade.hitbox.PymunkHitBoxAlgorithm()
            )
            self.run_textures.append(texture)

        # Load textures for idling
        self.idle_textures = []
        for i in range(10):
            texture = arcade.load_texture_pair(
                Player.asset_path / f"Idle_48x48_{i}.png",
                arcade.hitbox.PymunkHitBoxAlgorithm()
            )
            self.idle_textures.append(texture)

        # Load textures for pushing
        self.push_textures = []
        for i in range(10):
            texture = arcade.load_texture_pair(
                Player.asset_path / f"Push_48x48_{i}.png",
                arcade.hitbox.PymunkHitBoxAlgorithm()
            )
            self.push_textures.append(texture)

        self.hurt_textures = []
        for i in range(4):
            texture = arcade.load_texture_pair(
                Player.asset_path / f"Hurt_48x48_{i}.png",
                arcade.hitbox.PymunkHitBoxAlgorithm()
            )
            self.hurt_textures.append(texture)

        self.death_textures = []
        for i in range(10):
            texture = arcade.load_texture_pair(
                Player.asset_path / f"Death_48x48_{i}.png",
                arcade.hitbox.PymunkHitBoxAlgorithm()
            )
            self.death_textures.append(texture)

        # Set the initial texture
        self.texture = self.idle_textures[0][0]

        # Hit box will be set based on the first image used. If you want to specify
        # a different hit box, you can do it like the code below.
        # set_hit_box = [[-22, -64], [22, -64], [22, 28], [-22, 28]]
        # self.hit_box = self.texture.hit_box_points

        self.x_odometer = 0
        self.y_odometer = 0

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        """ Handle being moved by the pymunk engine """

        # Figure out if we need to face left or right
        if dx < -config.DEAD_ZONE and self.character_face_direction == Player.right_facing:
            self.character_face_direction = Player.left_facing
        elif dx > config.DEAD_ZONE and self.character_face_direction == Player.left_facing:
            self.character_face_direction = Player.right_facing

        # Add to the odometer how far we've moved
        self.x_odometer += dx
        self.y_odometer += dy

        # Death Animation
        if self.death_cycles > 8:
            self.death_cycles = 0
            self.dead = True

        if self.health <= 0 and not self.dead:
            self.cur_texture += 1
            if self.cur_texture > 10:
                self.death_cycles += 1
                self.cur_texture = 0

            self.texture = self.death_textures[self.death_cycles][
                self.character_face_direction
            ]
            return

        # Hurt animation
        if self.hurt_cycles > 2:
            self.hurt_cycles = 0

        if self.crushed:
            self.cur_texture += 1
            if self.cur_texture > 12:
                self.hurt_cycles += 1
                self.cur_texture = 0
            self.texture = self.hurt_textures[self.hurt_cycles][
                self.character_face_direction
            ]
            return

        # Jumping animation
        if self.jump_cycles > 1:
            self.jump_cycles = 0
            self.jumping = False

        if self.jumping:
            self.cur_texture += 1
            if self.cur_texture > 9:
                self.jump_cycles += 1
                self.cur_texture = 0
            self.texture = self.jump_textures[self.jump_cycles][
                self.character_face_direction
            ]
            return

        # Idle animation
        if self.idling_cycles > 8:
            self.idling_cycles = 0

        if abs(dx) <= config.DEAD_ZONE:
            self.cur_texture += 1
            if self.cur_texture > 4:
                self.idling_cycles += 1
                self.cur_texture = 0
            self.texture = self.idle_textures[self.idling_cycles][
                self.character_face_direction
            ]
            return

        # Pushing animation
        if self.pushing:
            self.cur_texture += 1
            if self.cur_texture > 9:
                self.cur_texture = 0
            self.texture = self.push_textures[self.cur_texture][
                self.character_face_direction
            ]
            return

        # Have we moved far enough to change the texture?
        if abs(self.x_odometer) > Player.distance_to_change_texture:

            # Reset the odometer
            self.x_odometer = 0

            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.run_textures[self.cur_texture][
                self.character_face_direction
            ]
