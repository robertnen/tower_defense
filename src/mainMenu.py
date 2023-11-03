import pyglet
from pyglet.window import key
from pyglet.window import mouse
from pyglet import image
import constant

def isInRect(x, y, tx, ty, isAnim, button : pyglet.shapes.Rectangle): # animates the buttons
    if x >= tx and x <= tx + constant.MM_BUTTON_WIDTH and \
        y >= ty and y <= ty + constant.MM_BUTTON_HEIGHT:
            if isAnim is False:
                for i in range(100, 206):
                    button.color = (i, i, i)
                    isAnim = True

            else:
                for i in range(205, 99, -1):
                    button.color = (i, i, i)
                isAnim = False
    return isAnim

class MainMenu(pyglet.window.Window):
    win = None
    img = None
    batch = None # used for graphics
    width = None        # of window
    height = None       # of window
    play_label = None
    exit_label = None
    play_button = None
    exit_button = None
    settings_label = None
    settings_button = None
    isAnimPlay = False      # used for pseudo-hover
    isAnimExit = False      # used for pseudo-hover
    isAnimSettings = False  # used for pseudo-hover

    def __init__(self):
        super(MainMenu, self).__init__()

        self.win = pyglet.window.Window(fullscreen = True)

        # temporary label
        label = pyglet.text.Label('144 Hz if VSync off! Press ESC to close it',
                          font_name = 'Times New Roman',
                          font_size = 36,
                          x = self.win.width / 2, y = self.win.height / 2 + 100,
                          anchor_x = 'center', anchor_y = 'center')

        self.width = self.win.width;
        self.height = self.win.height;

        # define main menu logo
        self.img = pyglet.resource.image('img/tower_defense.png')
        self.img.width = 600
        self.img.height = 200

        # for shapes
        self.batch = pyglet.graphics.Batch()

        self.play_label = pyglet.text.Label('Play',
                                       font_name = 'Times New Roman',
                                       font_size = 28,
                                       x = self.win.width / 2,
                                       y = self.win.height / 2,
                                       anchor_x = 'center', anchor_y = 'center')

        self.play_button = pyglet.shapes.Rectangle(x = self.width / 2 - 150, y = self.height / 2 - 30,
                                            width = constant.MM_BUTTON_WIDTH, height = constant.MM_BUTTON_HEIGHT,
                                            color = (100, 100, 100), batch = self.batch)

        self.settings_label = pyglet.text.Label('Settings',
                                       font_name = 'Times New Roman',
                                       font_size = 28,
                                       x = self.win.width / 2,
                                       y = self.win.height / 2  - 100,
                                       anchor_x = 'center', anchor_y = 'center')

        self.settings_button = pyglet.shapes.Rectangle(x = self.width / 2 - 150, y = self.height / 2 - 130,
                                            width = constant.MM_BUTTON_WIDTH, height = constant.MM_BUTTON_HEIGHT,
                                            color = (100, 100, 100), batch = self.batch)

        self.exit_label = pyglet.text.Label('Exit',
                                       font_name = 'Times New Roman',
                                       font_size = 28,
                                       x = self.win.width / 2,
                                       y = self.win.height / 2 - 200,
                                       anchor_x = 'center', anchor_y = 'center')

        self.exit_button = pyglet.shapes.Rectangle(x = self.width / 2 - 150, y = self.height / 2 - 230,
                                            width = constant.MM_BUTTON_WIDTH, height = constant.MM_BUTTON_HEIGHT,
                                            color = (100, 100, 100), batch = self.batch)

        # play_button.opacity = 100

        @self.win.event
        def on_draw():
            self.win.clear()
            self.img.blit(self.width / 2 - 300, self.height / 2 + 80) # just an image test
            label.draw()
            self.batch.draw()
            self.play_button.draw()
            self.play_label.draw()
            self.settings_button.draw()
            self.settings_label.draw()
            self.exit_button.draw()
            self.exit_label.draw()

        @self.win.event
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

        @self.win.event
        def on_mouse_press(x, y, button, modifiers):
            match button:
                case mouse.LEFT:
                    print('LM', end = ' ')
                case mouse.RIGHT:
                    print('RM', end = ' ')
                case _:
                    print('Another mouse button was pressed')

            tx = self.exit_button.x
            ty = self.exit_button.y

            if x >= tx and x <= tx + constant.MM_BUTTON_WIDTH and \
                y >= ty and y <= ty + constant.MM_BUTTON_HEIGHT:
                    self.exit_func() # the user wants to leave the game

            print(f'({x}, {y})')

        @self.win.event
        def on_mouse_motion(x, y, dx, dy):
            # print(f'({x}, {y})') # use this for debugging

            self.isAnimPlay = isInRect(x, y, self.play_button.x, self.play_button.y, self.isAnimPlay, self.play_button)
            self.isAnimExit = isInRect(x, y, self.exit_button.x, self.exit_button.y, self.isAnimExit, self.exit_button)
            self.isAnimSettings = isInRect(x, y, self.settings_button.x, self.settings_button.y, self.isAnimSettings, self.settings_button)

        @self.win.event
        def on_close():
            print('The main menu window was closed')
            pyglet.app.exit()

    def set_icon(self, filePath : str):
        icon = pyglet.resource.image(filePath)
        self.win.set_icon(icon)

    def exit_func(self):
        self.win.on_close()
