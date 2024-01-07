import mainMenu
import pyglet
import constant
import map

# do not change
pyglet.resource.path = ["../assets"] # assets needs to be the default resource directory
pyglet.resource.reindex()

# this
main_menu = mainMenu.MainMenu()
map = map.Map(constant.MAP1_PATH, main_menu.batch)

if not map.isValid:
    exit(1)

# enemy test (can be removed)
# (y, x) = map.find_start()
# e = enemy.Enemy("name", "purple", 0.1, 1, x, y, 151, main_menu.batch)

# testare
# main_menu.hide()
pyglet.app.run(1 / 144) # 144 Hz