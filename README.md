# Tetris-in-Ohio
PyWeek 35 entry


## How to run

Theres no addditional dependancies other than arcade. Supports python3.8-11. Although if you want to use run the `dev_tools` directory make sure to keep it below python3.10 due to a limitation with PyAudio. The `dev_tools` is not used by the game itself but was used by me to handle the assets.

```commandline
$ pip install arcade==3.0.0.dev18 || pip install -r requirements.txt
```

There are two parameters you can pass to run the game i.e debug and performance. Pass true for performance if you have a low end pc.
```commandline
python src/main.py # normal run
python src/main.py true # debug run
python src/main.py false true # performance run
```


## Production

+ The player has 6 animations -> (Death, Hurt, Idle, Jump, Push, Run)
+ Has two background music
+ Has a rainy effect for the loosing screen
+ Has a different music which for dying(the famous gregorian chant dies irae) which is coded by me see `src/dev_tools/generate_music.py`
+ Uses shaders for lighting effect


## Innovation

+ The game is an extract of the age old game Tetris, but instead of normally controlling the columns in which the boxes fall in you get a character which does that
+ Tetris in Ohio comes from the meme "Only in Ohio" which basically means things are different in Ohio, thus reflecting the concept of the game
+ Theres a backstory included in the game's `Story?` button, which co-relates with the theme
+ Dies Irae(literally means day of wrath in latin) the Gregorian Chant starts playing when you die, showing the extent of darkness


## Fun

Did you had fun playing it? I hope you did. The game contains meme reference hope you had a laugh.


## Bugs

+ Some times the player the gets stuck between two press 'R' to reset the player's position.
