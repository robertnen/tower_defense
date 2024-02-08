# Tower_defense
A 2D game made in Python using [Pyglet](https://pyglet.org). Are you bored of looking at towers? Do you want them to shoot some enemies and to hear some cool music?
We have the solution! Tower defense is a game containing simple shapes as buildings trying to save your base from being killed by unknown foes. Just pick a building from the right side and place it on sand. It is awesome!

Preview: [Tower Defense Preview](https://www.youtube.com/watch?v=9fCq2ZyGRy8)

# How to play the game
You will need to install Pyglet[^1] before playing the game.

```
    pip install --upgrade --user pyglet
```

After open the [main.py](./src/main.py) and run it. Press ESC if you want to force quit the game.

# Team members
Nenciu George-Robert (323CC)
    - created the main menu, buttons, options
    - added music and sounds for the game
    - added textures for main menu and others
    - made debug for menu
    - made the README

Fulop Adelin-Andrei  (321CC)
    - created the maps
    - made functions to check if the game can be player (e.g. map is legit)
    - added textures for the map (sand, grass, border etc)
    - made debug for map

Tanase Elena-Ramona  (323CC)
    - created the enemies
    - made functions for the enemie's movement animation
    - added textures for enemies
    - made debug for enemies

Apostu Izabela-Elena (323CC)
    - created the buildings
    - made functions for the building's movement animation
    - added textures for the buildings
    - made debug for buildings

# About the game's implementation
This game took over 60 hours to make. The game is simple: a 2D board where you have to defend a base using only buildings. The game looks simple, but it can be used in many ways. For example, the map can be changed with any map that has an enemy base and a player base with a unique path between them. The game will work perfectly. The number of enemies can be changed by replacing a number from constant.py (where all the constants of the game are).
No one from the team have worked with Pyglet[^1] (some of us never worked with Python before this project).

# Map Editor
You can change the map however you want. In the [maps](./assets/maps) folder you will find 3 maps which can be edited however you want. What the numbers represent:
0. Enemy path
1. Sand (buildings can be placed there)
2. Grass (nothing can happen there)
3. Border (nothing can happen there)
4. Player base
5. Enemy base

# Objectives:
- [x] Find a good game engine
- [x] Find songs for the game
- [x] Find good sfx sounds
- [x] Find / Make textures or images
- [x] Make the main Menu
    - [x] Make an "exit" button
    - [x] Make a "settings" button
    - [x] Make a "play" button
    - [x] Finish the settings
    - [x] Add background
- [x] Make a map reader
- [x] Make a map drawer
- [x] Define buildings
- [x] Define enemies
- [x] Make buildings to attack enemies
- [x] Make small animations
- [x] Finish the README.md

[^1]: Pyglet isn't made by us. [Link](https://pyglet.org) to the official site.
