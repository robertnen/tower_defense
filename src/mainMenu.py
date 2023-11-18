import pyglet
import button
import constant
from pyglet.window import key
from pyglet.window import mouse

def isInRect(x, y, tx, ty, button: button.Button): # animates the buttons
    if x >= tx and x <= tx + constant.MM_BUTTON_WIDTH and \
        y >= ty and y <= ty + constant.MM_BUTTON_HEIGHT:
            button.setSpriteColor(constant.LIGHT_GREY)
            return True
    else:
            button.setSpriteColor(constant.GREY)
            return False

class MainMenu():
    win = None

    logo_img = None                 # logo
    logo_sprite = None

    bg_img = None                   # background
    bg_sprite = None

    batch = None                    # used for graphics

    width = None                    # of window
    height = None                   # of window

    play_button = None
    exit_button = None
    settings_button = None

    isHidden = False                # used for mouse / keys events

    def __init__(self):
        self.win = pyglet.window.Window(fullscreen = True, caption = constant.GAME_TITLE)

        # for graphics shapes
        self.batch = pyglet.graphics.Batch()

        self.width = self.win.width;
        self.height = self.win.height;

        # define main menu logo and background
        self.logo_img = pyglet.resource.image(constant.LOGO_PATH)
        self.bg_img = pyglet.resource.image(constant.BG_PATH)

        self.bg_img.width = self.width
        self.bg_img.height = self.height

        self.logo_img.width = constant.LOGO_WIDTH
        self.logo_img.height = constant.LOGO_HEIGHT

        self.bg_sprite = pyglet.sprite.Sprite(self.bg_img, x = 0, y = 0, z = 96, batch = self.batch)

        self.logo_sprite = pyglet.sprite.Sprite(self.logo_img, x = self.width / 2 - 300, y = self.height / 2 + 80, z = 98,
                                                batch = self.batch)

        # define buttons
        self.play_button = button.Button(constant.PLAY, constant.GREY,
                                         self.width / 2 - 150, self.height / 2, self.batch)

        self.settings_button = button.Button(constant.SETTINGS, constant.GREY,
                                         self.width / 2 - 150, self.height / 2 - 100, self.batch)

        self.exit_button = button.Button(constant.EXIT, constant.GREY,
                                         self.width / 2 - 150, self.height / 2 - 200, self.batch)

        # override win events for main menu
        @self.win.event
        def on_draw():
            self.win.clear()
            self.batch.draw()

        @self.win.event
        def on_key_press(symbol, modifiers):
            if constant.DEBUG or constant.DEBUG_KEYS:
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
            if constant.DEBUG or constant.DEBUG_MOUSE:
                match button:
                    case mouse.LEFT:
                        print('LM', end = ' ')
                    case mouse.RIGHT:
                        print('RM', end = ' ')
                    case _:
                        print('Another mouse button was pressed')
                print(f'({x}, {y})')

            # if still in main menu
            if self.isHidden == False:
                if isInRect(x, y, self.play_button.x, self.play_button.y, self.play_button):
                    if constant.DEBUG:
                        print('Play button pressed')

                    self.play_func()

                if isInRect(x, y, self.settings_button.x, self.settings_button.y, self.settings_button):
                    if constant.DEBUG:
                        print('Settings button pressed')

                    self.settings_func()

                if isInRect(x, y, self.exit_button.x, self.exit_button.y, self.exit_button):
                    if constant.DEBUG:
                        print('Exit button pressed')

                    self.exit_func() # the user wants to leave the game

        @self.win.event
        def on_mouse_motion(x, y, dx, dy):
            if constant.DEBUG or constant.DEBUG_MOUSE:
                print(f'({x}, {y})') # use this for debugging

            # if still in main menu
            if self.isHidden == False:
                isInRect(x, y, self.play_button.x, self.play_button.y, self.play_button)
                isInRect(x, y, self.settings_button.x, self.settings_button.y, self.settings_button)
                isInRect(x, y, self.exit_button.x, self.exit_button.y, self.exit_button)

        @self.win.event
        def on_close():
            print('The main menu window was closed')
            pyglet.app.exit()

    def set_icon(self, filePath : str):
        icon = pyglet.resource.image(filePath)
        self.win.set_icon(icon)

    def play_func(self):
        pass

    def settings_func(self):
        pass

    def exit_func(self):
        self.win.on_close()

    def addBackground(self):
        pass

    def hide(self): # use this when you want to clear the window
        self.logo_sprite.batch = None
        self.bg_sprite.batch = None

        self.play_button.hide()
        self.settings_button.hide()
        self.exit_button.hide()

        self.isHidden = True

    def show(self): # use this when you want to use the window for the main menu
        self.logo_sprite.batch = self.batch
        self.bg_sprite.batch = self.batch

        self.play_button.show()
        self.settings_button.show()
        self.exit_button.show()

        self.isHidden = False
