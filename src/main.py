import mainMenu
import pyglet
import gameUtils
import constant
from pyglet.window import key
from pyglet.window import mouse

from src.map import Map

pyglet.resource.path = ["../assets"] # assets needs to be the default resource directory
pyglet.resource.reindex()

main_menu = mainMenu.MainMenu()

player = pyglet.media.Player()
player.queue(pyglet.media.load(gameUtils.getFilePath('Main_Menu.wav', constant.TYPE_SONG)))

player.volume = 0.3
player.play()
player.loop = True

map = Map(constant.MAP1_PATH)

if not map.isValid:
    exit(1)

pyglet.app.run(1 / 144) # 144 Hz
