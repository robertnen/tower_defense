import mainMenu
import pyglet
import constant
import map

# do not change
pyglet.resource.path = ["../assets"] # assets needs to be the default resource directory
pyglet.resource.reindex()

main_menu = mainMenu.MainMenu()
# this

map = map.Map(constant.MAP1_PATH)

if not map.isValid:
    exit(1)

pyglet.app.run(1 / 144) # 144 Hz
