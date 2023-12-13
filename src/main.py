import mainMenu
import pyglet
import constant
import map
import enemy

# do not change
pyglet.resource.path = ["../assets"] # assets needs to be the default resource directory
pyglet.resource.reindex()

main_menu = mainMenu.MainMenu()
# this

map = map.Map(constant.MAP1_PATH)

if not map.isValid:
    exit(1)

# enemy test (can be removed)
e = enemy.Enemy("name", "color", 0.1, 1, 1, 1, 1, main_menu.batch)
result = e.newCoordinates(360, 290, map.matrix)

while not type(result) == int:
    x, y = result
    result = e.newCoordinates(x, y, map.matrix)

# testare
# main_menu.hide()
print(type(map.matrix))
pyglet.app.run(1 / 144) # 144 Hz
