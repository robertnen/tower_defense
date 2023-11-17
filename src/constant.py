# debug (before doing a commit please put everything to false)
DEBUG = False                   # change to true if you want to get info from everything
DEBUG_KEYS = False              # change to true if you want to get info from mouse
DEBUG_MOUSE = False             # change to true if you want to get info from keyboard
DEBUG_MAP_READER = False        # change to true if you want to get info from map reader

# used for buttons (for now on main menu)
MM_BUTTON_WIDTH = 300
MM_BUTTON_HEIGHT = 50

# game info
GAME_TITLE = 'Tower Defense'

# logo
LOGO_PATH = 'img/tower_defense.png'
LOGO_WIDTH = 600
LOGO_HEIGHT = 200

# used for getFilePath second argument
TYPE_IMAGE = '\\assets\img\\'
TYPE_SONG = '\\assets\songs\\'
TYPE_MAP = '\\assets\maps\\'

# text for main menu buttons
PLAY = 'Play'
SETTINGS = 'Settings'
EXIT = 'Exit'

# used for button class
BUTTON = '_button.png'

# to get a building just write gameUtils.getFilePath(COLOR + SHAPE, constant.TYPE_IMAGE)

# shapes for file path
CIRCLE = '_circle.png'
SQUARE = '_square.png'
HEXAGO = '_hexagon.png'
TRIANG = '_triangle.png'
TRAPEZ = '_trapezoid.png'

# colors
RED = 'red'
GREY = 'grey'
BLUE = 'blue'
GREEN = 'green'
PURPLE = 'purple'
YELLOW = 'yellow'
LIGHT_GREY = 'light_grey'

# used for maps
LINE = 9
COLUMN = 18
WIDTH_MAP = 1440
HEIGHT_MAP = 720
X_START_MAP = 100
Y_START_MAP = 100
MAP1_PATH = 'map1.txt'