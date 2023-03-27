import arcade
import arcade.gui

import config


class Aftermath(arcade.View):
    def __init__(self, score, win, dies_irae_player=None):
        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.anchor = self.manager.add(arcade.gui.UIAnchorLayout())

        self.v_box = arcade.gui.UIBoxLayout(space_between=20)

        win_loose_message = "You win!\nCongrats for escaping!!"
        if not win:
            arcade.set_background_color(arcade.color.EERIE_BLACK)
            win_loose_message = "You lose\nYOU ARE NOW TRAPPED"

        win_loose_text = arcade.gui.UILabel(text=win_loose_message, multiline=True, width=250, align="center")

        play_again_button = arcade.gui.UIFlatButton(text="Play again", width=250)

        score_text = arcade.gui.UILabel(text=f"Your score: {score}", width=250, align="center")

        @play_again_button.event("on_click")
        def on_click_play_again_button(_event):
            from views import Game
            if dies_irae_player:
                arcade.stop_sound(dies_irae_player)
            self.start_bg_player = arcade.play_sound(self.start_bg_music)
            self.window.show_view(Game(self.start_bg_player))

        self.v_box.add(win_loose_text)
        self.v_box.add(play_again_button)
        self.v_box.add(score_text)

        self.anchor.add(
            child=self.v_box,
            anchor_x="center_x",
            anchor_y="center_y",
        )

        self.start_bg_music = arcade.load_sound(config.ASSET_PATH / "02.A-Creepyscape.ogg", streaming=False)
        self.start_bg_player = None

    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()
