import pyglet
import button
import constant
import option
import gameUtils
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

def isInSquare(x, y, tx, ty, bar: pyglet.sprite.Sprite, level: int):
    if x >= tx and x <= tx + constant.BAR_WIDTH and \
        y >= ty and y <= ty + constant.BAR_HEIGHT:
            if level >= 5: # from 100% to 0%
                level = 0
            else:
                level = level + 1

            bar.image = pyglet.resource.image('img/' + str(level) + constant.BAR)
            return True
    else:
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

    # for settings
    music_label = None
    sfx_label = None

    music_bar = None
    sfx_bar = None

    music_level = 3
    sfx_level = 3

    back_button = None

    isHiddenSettings = True         # the settings tab is hidden by default

    player = pyglet.media.Player()

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

        # define settings tab
        self.music_label = option.Option(constant.MUSIC, self.width / 2 - 330, self.height / 2 + 60, self.batch)
        self.sfx_label = option.Option(constant.SFX, self.width / 2 - 330, self.height / 2 - 60, self.batch)

        self.music_bar = pyglet.sprite.Sprite(pyglet.resource.image('img/' + str(self.music_level) + constant.BAR),
                                              x = self.music_label.x + 50 + constant.TEXT_BG_WIDTH,
                                              y = self.music_label.y - 9,
                                              z = 100,
                                              batch = self.batch)

        self.sfx_bar = pyglet.sprite.Sprite(pyglet.resource.image('img/' + str(self.sfx_level) + constant.BAR),
                                              x = self.sfx_label.x + 50 + constant.TEXT_BG_WIDTH,
                                              y = self.sfx_label.y - 9,
                                              z = 100,
                                              batch = self.batch)

        self.back_button = button.Button(constant.BACK, constant.GREY,
                                         self.width / 2 - 150, self.height / 2 - 200, self.batch)

        # settings tab are hidden by default
        self.hideSet()

        self.player.queue(pyglet.media.load(gameUtils.getFilePath('Main_Menu.wav', constant.TYPE_SONG)))

        self.player.volume = 0.5
        self.player.play()
        self.player.loop = True

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

            # if in menu settings
            if self.isHiddenSettings == False:
                if isInRect(x, y, self.back_button.x, self.back_button.y, self.back_button):
                    if constant.DEBUG:
                        print('Back to main menu button pressed')
                    self.menu_func()

                if isInSquare(x, y, self.music_bar.x, self.music_bar.y, self.music_bar, self.music_level) == True:

                    if self.music_level >= 5:
                        self.music_level = 0
                    else:
                        self.music_level = self.music_level + 1

                    self.player.volume = gameUtils.volumes(self.music_level)

                if isInSquare(x, y, self.sfx_bar.x, self.sfx_bar.y, self.sfx_bar, self.sfx_level) == True:
                    if self.sfx_level >= 5:
                        self.sfx_level = 0
                    else:
                        self.sfx_level = self.sfx_level + 1

        @self.win.event
        def on_mouse_motion(x, y, dx, dy):
            if constant.DEBUG or constant.DEBUG_MOUSE:
                print(f'({x}, {y})') # use this for debugging

            # if still in main menu
            if self.isHidden == False:
                isInRect(x, y, self.play_button.x, self.play_button.y, self.play_button)
                isInRect(x, y, self.settings_button.x, self.settings_button.y, self.settings_button)
                isInRect(x, y, self.exit_button.x, self.exit_button.y, self.exit_button)

            # if in menu settings
            if self.isHiddenSettings == False:
                isInRect(x, y, self.back_button.x, self.back_button.y, self.back_button)

        @self.win.event
        def on_close():
            print('The game was closed')
            pyglet.app.exit()

    def set_icon(self, filePath : str):
        icon = pyglet.resource.image(filePath)
        self.win.set_icon(icon)

    def menu_func(self):
        self.hideSet()                      # hide the settings tab
        self.show()                         # show the main menu tab

    def play_func(self):
        pass                                # TODO: implement here the game

    def settings_func(self):
        self.hide()                         # hide the main menu tab
        self.showSet()                      # show the settings tab
        self.bg_sprite.batch = self.batch   # keep the background for the settings tab

    def exit_func(self):
        self.win.on_close()

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

    def hideSet(self): # used for settings tab
        self.music_label.hide()
        self.music_bar.batch = None

        self.sfx_label.hide()
        self.sfx_bar.batch = None

        self.back_button.hide()

        self.isHiddenSettings = True

    def showSet(self): # used for settings tab
        self.music_label.show()
        self.music_bar.batch = self.batch

        self.sfx_label.show()
        self.sfx_bar.batch = self.batch

        self.back_button.show()

        self.isHiddenSettings = False
