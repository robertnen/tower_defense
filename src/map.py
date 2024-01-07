import constant
import gameUtils
import pyglet

class Map:
    height = constant.HEIGHT_MAP
    width = constant.WIDTH_MAP

    xStart = constant.X_START_MAP     # coords of starting position
    yStart = constant.Y_START_MAP

    matrix = None
    pathfile = None

    isValid = True           # if the map is valid or not

    batch = None
    imgs = [[None for _ in range(constant.COLUMN)] for _ in range(constant.LINE)]
    bgs = None

    place_b = [(0, 0) for _ in range(180)]
    place_size = 0

    def find_start(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == 5:
                    return i, j
        return -1  # invalid map

    def find_destination(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == 4:
                    return i, j
        return -1  # invalid map

    def dfs(self, i: int, j: int):
        if i < 0 or i >= constant.LINE:
            return False

        if j < 0 or j >= constant.COLUMN:
            return False

        if self.visited[i][j]:
            return False

        if self.matrix[i][j] == 5:
            return True

        if self.matrix[i][j] not in [0, 4]:
            return False

        self.visited[i][j] = True

        if self.dfs(i, j + 1) or self.dfs(i + 1, j) or self.dfs(i, j - 1) or self.dfs(i - 1, j):
            return True

        self.visited[i][j] = False  # unmark the cell before returning False
        return False

    def check_path_exists(self):
        result = self.dfs(*self.start)
        if not result:
            for row in self.visited:
                if False in row:  # if there's a cell that hasn't been visited
                    return False
        return True

    def read_matrix(self, filepath):
        matrix = []
        with open(filepath, 'r') as file:
            for line in file:
                # split line into list of values and convert them to int
                row = list(map(int, line.split()))
                matrix.append(row)
        return matrix

    def __init__(self, map_path, batch: pyglet.graphics.Batch):

        self.batch = batch
        self.pathfile = gameUtils.getFilePath(map_path, constant.TYPE_MAP)
        self.matrix = self.read_matrix(self.pathfile)

        if not self.matrix:
            print('Invalid map (null matrix)')
            self.isValid = False

        self.start = self.find_start()
        self.destination = self.find_destination()

        if self.start == -1 or self.destination == -1:
            print('Invalid map (no start nor destination)')
            self.isValid = False

        if constant.DEBUG or constant.DEBUG_MAP_READER: # map debug
            print(f'Pathfile = {self.pathfile}')
            print(f'isValid = {self.isValid}')
            print(f'Start = {self.start} End = {self.destination}')
            print('Map char:')
            for i in range(constant.LINE):
                for j in range(constant.COLUMN):
                    print(self.matrix[i][j], end = ' ')
                print()

        self.visited = [[False for _ in range(len(self.matrix[0]))] for _ in range(len(self.matrix))]

        if not self.dfs(self.start[0], self.start[1]):
            print('Invalid map (no path from start to destination)')
            self.isValid = False

    def drawMap(self):
        if constant.DEBUG or constant.DEBUG_MAP_READER:
            print("Map matrix: ")
            for i in range(0, constant.LINE):
                print(self.matrix[i])

        for y in range(0, constant.LINE):
            for x in range(0, constant.COLUMN):

                bg = pyglet.resource.image(constant.BACKGROUND)
                self.bgs = pyglet.sprite.Sprite(bg, x = 0, y = 0, z = 149, batch = self.batch)
                self.bgs.scale = 16 / 9

                img = None

                match self.matrix[y][x]:
                    case 0:
                        img = pyglet.resource.image(constant.ENEMY_PATH)
                    case 1:
                        img = pyglet.resource.image(constant.SAND)
                    case 2:
                        img = pyglet.resource.image(constant.GRASS)
                    case 3:
                        img = pyglet.resource.image(constant.BORDER)
                    case 4:
                        img = pyglet.resource.image(constant.PLAYER_BASE)
                    case 5:
                        img = pyglet.resource.image(constant.ENEMY_BASE)
                    case _:
                        print('Map corrupted in-game')

                self.imgs[y][x] = pyglet.sprite.Sprite(img, x = 160 + x * 80, y = 180 + (constant.LINE - 1 - y) * 80, z = 150, batch = self.batch)

                if self.matrix[y][x] == 1:
                    self.place_b[self.place_size] = (160 + x * 80, 180 + (constant.LINE - 1 - y) * 80)
                    self.place_size = self.place_size + 1

                if constant.DEBUG or constant.DEBUG_MAP_READER:
                    print(f'(i, j) = ({y}, {x}) -> (x, y) = ({160 + x * 80}, {180 + y * 80})')

    def hide(self):
        for y in range(constant.LINE):
            for x in range(constant.COLUMN):
                self.imgs[y][x].batch = None

        self.bgs.batch = None

    def show(self):
        for y in range(constant.LINE):
            for x in range(constant.COLUMN):
                self.imgs[y][x].batch = self.batch

        self.bgs.batch = self.batch