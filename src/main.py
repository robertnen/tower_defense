import mainMenu
import pyglet
from pyglet.window import key
from pyglet.window import mouse

pyglet.resource.path = ["../assets"] # assets needs to be the default resource directory
pyglet.resource.reindex()

window = pyglet.window.Window(fullscreen = True)
image = pyglet.resource.image('img/image_test.jpg')
label = pyglet.text.Label('144 Hz if VSync off! Press ESC to close it',
                          font_name = 'Times New Roman',
                          font_size = 36,
                          x = window.width / 2, y = window.height / 2,
                          anchor_x = 'center', anchor_y = 'center')

filepath = __file__
filepath = filepath[:filepath.rfind('src')]
print(filepath + '\assets\songs\Main_Menu.wav')

audio = pyglet.media.load(filepath + '\\assets\songs\Main_Menu.wav')

player = pyglet.media.Player()
player.queue(audio)

player.volume = 0.3
player.play()
player.loop = True

@window.event
def on_draw():
    window.clear()
    label.draw()
    # image.blit(0, 0) # just an image test

@window.event
def on_key_press(symbol, modifiers):
    match symbol:
        case key.W:
            print('W', end = ' ')
        case key.A:
            print('A', end = ' ')
        case key.S:
            print('S', end = ' ')
        case key.D:
            print('D', end = ' ')
        case _:
            print('A key was pressed')

@window.event
def on_mouse_press(x, y, button, modifiers):
    match button:
        case mouse.LEFT:
            print('LM', end = ' ')
        case mouse.RIGHT:
            print('RM', end = ' ')
        case _:
            print('Another mouse button was pressed')

    print(f'({x}, {y})')

pyglet.app.run(1 / 144) # 144 Hz

main_menu = mainMenu.MainMenu()
