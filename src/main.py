import mainMenu
import pyglet
import constant
import map
import enemy
import building


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

# building test (can be removed)
b = building.Building("name", constant.SQUARE, 5, 5.0, 50, 50, 100, main_menu.batch)

e2 = enemy.Enemy("name", "color", 0.1, 1, 45, 46, 1, main_menu.batch)
e1 = enemy.Enemy("name", "color", 0.1, 1, 53, 54, 1, main_menu.batch)
e3 = enemy.Enemy("name", "color", 0.1, 1, 44, 46, 1, main_menu.batch)

el = [e2, e1, e3]

b.find_closest_enemy(el)

# testare
# main_menu.hide()
pyglet.app.run(1 / 144) # 144 Hz
