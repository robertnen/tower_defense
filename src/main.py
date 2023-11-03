import mainMenu
import pyglet
from pyglet.window import key
from pyglet.window import mouse

def getFilePath(name: str):
    filePath = __file__
    filePath = filePath[:filePath.rfind('src')]
    filePath = filePath + '\\assets\songs\\' + name;
    return filePath

pyglet.resource.path = ["../assets"] # assets needs to be the default resource directory
pyglet.resource.reindex()

main_menu = mainMenu.MainMenu()
# main_menu.set_icon('img/image_test.jpg') # taskbar icon will be added at installer

audio = pyglet.media.load(getFilePath('Main_Menu.wav'))
# audio = pyglet.media.load(getFilePath('Level_1.wav'))

player = pyglet.media.Player()
player.queue(audio)

player.volume = 0.3
player.play()
player.loop = True

pyglet.app.run(1 / 144) # 144 Hz