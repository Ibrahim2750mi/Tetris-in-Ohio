import arcade
import arcade.gui

from views import Game


class StartMenu(arcade.View):
    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.anchor = self.manager.add(arcade.gui.UIAnchorLayout())

        self.v_box = arcade.gui.UIBoxLayout(space_between=20)

        start_button = arcade.gui.UIFlatButton(text="Start Game", width=250)

        @start_button.event("on_click")
        def on_click_start_button(_event):
            self.window.show_view(Game())

        exit_button = arcade.gui.UIFlatButton(text="Exit", width=250)

        @exit_button.event("on_click")
        def on_click_exit_button(_event):
            arcade.exit()

        self.v_box.add(start_button)
        self.v_box.add(exit_button)

        self.anchor.add(
            child=self.v_box,
            anchor_x="center_x",
            anchor_y="center_y",
        )

    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()
