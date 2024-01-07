import math
import random
import pyglet
from building import Building
import button
import constant
from enemy import Enemy
import option
import gameUtils
from pyglet.window import key
from pyglet.window import mouse
from map import Map

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
    isInGame = False                # wait for game to start
    isClicked = False               # check if building is on the mouse
    isWin = True                    # chcek if game is won

    map1 = None

    enemies = [None for _ in range(500)]     # enemies of the game
    enemies_size = 0

    buildings_preview = [None for _ in range(26)]       # buildings preview
    buildings_size = 0

    buildings = [None for _ in range(180)]              # buildings
    b_size = 0

    locations = [[(0, 0), (0, 0), (0, 0)],
                 [(0, 0), (0, 0), (0, 0)],
                 [(0, 0), (0, 0), (0, 0)],
                 [(0, 0), (0, 0), (0, 0)],
                 [(0, 0), (0, 0), (0, 0)]]               # locations of the preview buildings

    preview = None                  # sprite image of building
    (ti, tj) = (0, 0)               # location of placeable building
    tick = 0                        # game ticks

    player = pyglet.media.Player()
    sfx = pyglet.media.Player()

    livesLabel = None
    lives = 1

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

        self.map1 = Map(constant.MAP1_PATH, self.batch)
        self.livesLabel = pyglet.text.Label('Number of lives: 1', font_name='Times New Roman', font_size=24,
                                x=200, y=100, z=200, anchor_x='center', anchor_y='center', batch=None, color=(0, 0, 0, 150))

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

                    self.sfx.delete()
                    self.sfx = pyglet.media.Player()
                    self.sfx.queue(pyglet.media.load(gameUtils.getFilePath('button_clicked.wav', constant.TYPE_SOUND)))
                    self.sfx.volume = gameUtils.volumes(self.sfx_level)
                    self.sfx.play()
                    self.play_func()

                if isInRect(x, y, self.settings_button.x, self.settings_button.y, self.settings_button):
                    if constant.DEBUG:
                        print('Settings button pressed')

                    self.sfx.delete()
                    self.sfx = pyglet.media.Player()
                    self.sfx.queue(pyglet.media.load(gameUtils.getFilePath('button_clicked.wav', constant.TYPE_SOUND)))
                    self.sfx.volume = gameUtils.volumes(self.sfx_level)
                    self.sfx.play()
                    self.settings_func()

                if isInRect(x, y, self.exit_button.x, self.exit_button.y, self.exit_button):
                    if constant.DEBUG:
                        print('Exit button pressed')

                    self.sfx.delete()
                    self.sfx = pyglet.media.Player()
                    self.sfx.queue(pyglet.media.load(gameUtils.getFilePath('button_clicked.wav', constant.TYPE_SOUND)))
                    self.sfx.volume = gameUtils.volumes(self.sfx_level)
                    self.sfx.play()
                    self.exit_func() # the user wants to leave the game

            # if in menu settings
            if self.isHiddenSettings == False:
                if isInRect(x, y, self.back_button.x, self.back_button.y, self.back_button):
                    if constant.DEBUG:
                        print('Back to main menu button pressed')

                    self.sfx.delete()
                    self.sfx = pyglet.media.Player()
                    self.sfx.queue(pyglet.media.load(gameUtils.getFilePath('button_clicked.wav', constant.TYPE_SOUND)))
                    self.sfx.volume = gameUtils.volumes(self.sfx_level)
                    self.sfx.play()
                    self.menu_func()

                if isInSquare(x, y, self.music_bar.x, self.music_bar.y, self.music_bar, self.music_level) == True:

                    if self.music_level >= 5:
                        self.music_level = 0
                    else:
                        self.music_level = self.music_level + 1

                    self.sfx.delete()
                    self.sfx = pyglet.media.Player()
                    self.sfx.queue(pyglet.media.load(gameUtils.getFilePath('sfx_settings.mp3', constant.TYPE_SOUND)))
                    self.sfx.volume = gameUtils.volumes(self.sfx_level)
                    self.sfx.play()
                    self.player.volume = gameUtils.volumes(self.music_level)

                if isInSquare(x, y, self.sfx_bar.x, self.sfx_bar.y, self.sfx_bar, self.sfx_level) == True:
                    if self.sfx_level >= 5:
                        self.sfx_level = 0
                    else:
                        self.sfx_level = self.sfx_level + 1

                    self.sfx.delete()
                    self.sfx = pyglet.media.Player()
                    self.sfx.queue(pyglet.media.load(gameUtils.getFilePath('sfx_settings.mp3', constant.TYPE_SOUND)))
                    self.sfx.volume = gameUtils.volumes(self.sfx_level)
                    self.sfx.play()

            if self.isInGame == True:
                shapes = [constant.HEXAGO, constant.SQUARE, constant.TRIANG, constant.TRAPEZ, constant.CIRCLE]
                colors = ["blue", "yellow", "red"]
                cooldowns = [constant.BUILDING_BLUE_COOLDOWN, constant.BUILDING_YELLOW_COOLDOWN, constant.BUILDING_RED_COOLDOWN]
                radii = [constant.BUILDING_BLUE_RADIUS, constant.BUILDING_YELLOW_RADIUS, constant.BUILDING_RED_RADIUS]

                (tx, ty) = (-1, -1)
                (ti, tj) = (-1, -1)

                for i in range(5):
                    if (tx, ty) == (-1, -1):
                        for j in range(3):
                            (lx, ly) = self.locations[i][j]

                            if x >= lx - 10 and x <= lx + 10 and y >= ly - 10 and y <= ly + 10:
                                (tx, ty) = (x, y)
                                (ti, tj) = (i, j)
                                break


                if self.isClicked == False and (tx, ty) != (-1, -1):
                    (self.ti, self.tj) = (ti, tj)
                    self.isClicked = True
                    img = pyglet.resource.image('img/' + colors[tj] + shapes[ti])
                    self.preview = pyglet.sprite.Sprite(img, x = x, y = y, z = 155, batch = self.batch)
                elif self.isClicked == True:
                    self.isClicked = False

                    (tx, ty) = (-1, -1)
                    for i in range(self.map1.place_size):
                        (lx, ly) = self.map1.place_b[i]

                        if x >= lx and x <= lx + 80 and y >= ly and y <= ly + 80 and self.buildings[i] == None:
                            b = Building(colors[self.tj], shapes[self.ti], cooldowns[self.tj], radii[self.tj], lx + 40, ly + 40, 160, self.batch)
                            self.buildings[i] = b
                            self.sfx.delete()
                            self.sfx = pyglet.media.Player()
                            self.sfx.queue(pyglet.media.load(gameUtils.getFilePath('placed.wav', constant.TYPE_SOUND)))
                            self.sfx.volume = gameUtils.volumes(self.sfx_level)
                            self.sfx.play()
                            (tx, ty) = (x, y)

                    if (tx, ty) == (-1, -1):
                        self.sfx.delete()
                        self.sfx = pyglet.media.Player()
                        self.sfx.queue(pyglet.media.load(gameUtils.getFilePath('cancel.wav', constant.TYPE_SOUND)))
                        self.sfx.volume = gameUtils.volumes(self.sfx_level)
                        self.sfx.play()

                    self.preview.batch = None
                    self.preview = None

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

            if self.isClicked == True:
                self.preview.x = x
                self.preview.y = y

        @self.win.event
        def on_close():
            print('The game was closed')
            pyglet.app.exit()

    def set_icon(self, filePath: str):
        icon = pyglet.resource.image(filePath)
        self.win.set_icon(icon)

    def menu_func(self):
        self.hideSet()                      # hide the settings tab
        self.show()                         # show the main menu tab

    def play_func(self):
        self.hide()
        self.isInMenu = False

        self.player.pause()

        self.player.queue(pyglet.media.load(gameUtils.getFilePath('Level_1.wav', constant.TYPE_SONG)))
        self.player.queue(pyglet.media.load(gameUtils.getFilePath('Level_2.wav', constant.TYPE_SONG)))
        self.player.queue(pyglet.media.load(gameUtils.getFilePath('Level_3.wav', constant.TYPE_SONG)))
        self.player.queue(pyglet.media.load(gameUtils.getFilePath('Ending.wav', constant.TYPE_SONG)))

        self.player.volume = gameUtils.volumes(self.music_level)
        self.player.play()
        self.player.loop = False

        self.mainGame()

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

    def gameTicks(self, dt):
        self.tick = self.tick + 1

# functions for the main game
    def spawnEnemy(self, dt):
        (y, x) = self.map1.find_start()
        colors = ["purple", "green", "blue", "yellow", "red"]
        speeds = [constant.ENEMY_SPEED_SLOW, constant.ENEMY_SPEED_NORMAL, constant.ENEMY_SPEED_FAST]
        hps = [constant.ENEMY_PURPLE_HP, constant.ENEMY_GREEN_HP, constant.ENEMY_BLUE_HP, constant.ENEMY_YELLOW_HP, constant.ENEMY_RED_HP]

        r1 = random.randint(0, 4)
        r2 = random.randint(0, 2)

        e = Enemy("name", colors[r1], speeds[r2], hps[r1], x, y, 151, self.batch)

        self.enemies[self.enemies_size] = e
        self.enemies_size = self.enemies_size + 1

    def moveEnemies(self, dt):
        for i in range(constant.TOTAL):
            if self.enemies[i] is None: # enemy dead or didn't spawn yet
                continue

            e: Enemy
            e = self.enemies[i]

            x = (e.sprite.x - 180) / 80
            y = (200 - e.sprite.y) / 80 - 1 + constant.LINE

            (dy, dx) = self.map1.find_destination()

            if abs(dx - x) <= 1 and abs(dy - y) <= 1:
                self.enemies[i].hide()
                self.enemies[i] = None
                self.lives = self.lives - 1
                self.livesLabel.text = 'Number of lives: ' + str(self.lives)

                self.sfx.delete()
                self.sfx = pyglet.media.Player()
                self.sfx.queue(pyglet.media.load(gameUtils.getFilePath('life_lost.mp3', constant.TYPE_SOUND)))
                self.sfx.volume = gameUtils.volumes(self.sfx_level)
                self.sfx.play()

                if self.lives <= 0:
                    self.isWin = False
                    pyglet.clock.unschedule(self.endGame)
                    self.endGame(0)
                continue

            r = e.newCoordinates(e.sprite.x, e.sprite.y, self.map1.matrix)

            if r != -1:
                (x, y) = r
                self.enemies[i].tx = x - e.sprite.x
                self.enemies[i].ty = y - e.sprite.y

            self.enemies[i].sprite.x = self.enemies[i].sprite.x + (int) (self.enemies[i].tx * self.enemies[i].speed)
            self.enemies[i].sprite.y = self.enemies[i].sprite.y + (int) (self.enemies[i].ty * self.enemies[i].speed)

    def shootEnemies(self, dt):
        for i in range(self.map1.place_size):
            if self.buildings[i] != None:
                (e, j) = self.buildings[i].find_closest_enemy(self.enemies)
                if e == None:
                    continue

                self.buildings[i].sprite.rotation = 180 - (int) (math.atan2(e.sprite.y - self.buildings[i].sprite.y, e.sprite.x - self.buildings[i].sprite.x) * 180 / math.pi)

                if self.tick % self.buildings[i].cooldown == 0:
                    e.hp = e.hp - 1
                    self.enemies[j] = e
                    if self.enemies[j].hp < 1:
                        # self.enemies[j].hide()
                        (y, x) = self.map1.find_start()
                        self.enemies[j].sprite.x = 190 + x * 80;
                        self.enemies[j].sprite.y = 210 + (constant.LINE - 1 - y) * 80;
                        self.enemies[j].visited = [[0 for x in range(constant.COLUMN)] for y in range(constant.LINE)]
                        # self.enemies[j] = None
                        self.sfx.delete()
                        self.sfx = pyglet.media.Player()
                        self.sfx.queue(pyglet.media.load(gameUtils.getFilePath('enemy_killed.wav', constant.TYPE_SOUND)))
                        self.sfx.volume = gameUtils.volumes(self.sfx_level)
                        self.sfx.play()

    def endGame(self, dt):
        self.isInGame = False
        self.isClicked = False
        if self.preview != None:
            self.preview.batch = None
            self.preview = None

        self.locations = [[(0, 0), (0, 0), (0, 0)],
                          [(0, 0), (0, 0), (0, 0)],
                          [(0, 0), (0, 0), (0, 0)],
                          [(0, 0), (0, 0), (0, 0)],
                          [(0, 0), (0, 0), (0, 0)]]

        self.tick = 0

        self.sfx.delete()
        self.sfx = pyglet.media.Player()

        if self.isWin == True:
            self.livesLabel.text = 'Congrats! You\'ve won the game. Press ESC to exit...'
            self.sfx.queue(pyglet.media.load(gameUtils.getFilePath('game_won.wav', constant.TYPE_SOUND)))
        else:
            self.livesLabel.text = 'You lost the game! Press ESC to exit...'
            self.sfx.queue(pyglet.media.load(gameUtils.getFilePath('game_lost.mp3', constant.TYPE_SOUND)))

        self.livesLabel.x = self.livesLabel.x + 200
        self.sfx.volume = gameUtils.volumes(self.sfx_level)
        self.sfx.play()

        # for menu
        self.player.delete()

        self.player = pyglet.media.Player()
        self.player.queue(pyglet.media.load(gameUtils.getFilePath('Main_Menu.wav', constant.TYPE_SONG)))

        self.player.volume = gameUtils.volumes(self.music_level)
        self.player.play()
        self.player.loop = True
        self.show()
        self.play_button.hide()
        self.settings_button.hide()
        pyglet.clock.unschedule(self.moveEnemies)
        pyglet.clock.unschedule(self.gameTicks)
        pyglet.clock.unschedule(self.shootEnemies)

    def mainGame(self):
        self.map1.drawMap()
        self.isInGame = True
        self.livesLabel.batch = self.batch

        shapes = [constant.HEXAGO, constant.SQUARE, constant.TRIANG, constant.TRAPEZ, constant.CIRCLE]
        colors = ["blue", "yellow", "red"]

        for i in range(5):
            for j in range(3):
                b = Building(colors[j], shapes[i], 1, 1, 1650 + j * 80 + 60, self.height / 2 - 80 + i * 80 + 60, 152, self.batch)

                self.locations[i][j] = (1650 + j * 80 + 60, self.height / 2 - 80 + i * 80 + 60)

                self.buildings_preview[self.buildings_size] = b
                self.buildings_size = self.buildings_size + 1

        # spawn enemies
        for i in range(constant.TOTAL):
            pyglet.clock.schedule_once(self.spawnEnemy, i * 5)

        pyglet.clock.schedule_interval(self.moveEnemies, 0.8)
        pyglet.clock.schedule_interval(self.gameTicks, 1)
        pyglet.clock.schedule_interval(self.shootEnemies, 1)
        pyglet.clock.schedule_once(self.endGame, 300)

