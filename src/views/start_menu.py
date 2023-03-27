import arcade
import arcade.gui

import config
from views import Game


class StartMenu(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.STORMCLOUD)

        self.manager = arcade.gui.UIManager()
        self.anchor = self.manager.add(arcade.gui.UIAnchorLayout())

        self.v_box = arcade.gui.UIBoxLayout(space_between=20)

        start_button = arcade.gui.UIFlatButton(text="Start Game", width=250)

        @start_button.event("on_click")
        def on_click_start_button(_event):
            self.window.show_view(Game(self.start_bg_player))

        story_button = arcade.gui.UIFlatButton(text="Story?", width=250)
        story_box = arcade.gui.UIMessageBox(
            message_text=config.STORY,
            width=500,
            height=350,
            buttons=("Pop culture", "Back"),
        )
        pop_culture_box = arcade.gui.UIMessageBox(
            message_text=config.POPCULTURE_REFERENCE,
            width=500,
            height=350,
            buttons=("Back", ),
        )

        @story_button.event("on_click")
        def on_click_story_button(_event):
            self.manager.add(story_box)

        @story_box.event("on_action")
        def on_click_story_box_buttons(event: arcade.gui.UIOnActionEvent):
            if event.action == "Pop culture":
                self.manager.add(pop_culture_box)

        exit_button = arcade.gui.UIFlatButton(text="Exit", width=250)

        @exit_button.event("on_click")
        def on_click_exit_button(_event):
            arcade.exit()

        self.v_box.add(start_button)
        self.v_box.add(story_button)
        self.v_box.add(exit_button)

        self.anchor.add(
            child=self.v_box,
            anchor_x="center_x",
            anchor_y="center_y",
        )

        self.start_bg_music = arcade.load_sound(config.ASSET_PATH / "02.A-Creepyscape.ogg", streaming=False)
        self.start_bg_player = None

    def on_show_view(self):
        self.manager.enable()
        self.start_bg_player = arcade.play_sound(self.start_bg_music)

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()
