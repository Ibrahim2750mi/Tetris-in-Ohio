import arcade

import config
from views import StartMenu


def main():
    window = arcade.Window(config.SCREEN_WIDTH, config.SCREEN_HEIGHT, title='Tetris in Ohio')
    start_view = StartMenu()
    window.show_view(start_view)
    window.run()


if __name__ == '__main__':
    main()
