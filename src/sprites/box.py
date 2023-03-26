import arcade


class Box(arcade.Sprite):
    def __init__(self, pathname: str):
        super().__init__(pathname)

        # For static boxes this should be False.
        self.react_to_player = True
