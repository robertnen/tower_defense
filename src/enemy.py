import pyglet
import constant
import gameUtils
from constant import LINE, COLUMN

class Enemy():
    name = None
    colour = None
    speed = None
    hp = None

    x = None        # coordinates
    y = None

    z = None        # z-index

    image = None
    sprite = None
    batch = None

    visited = None      # visited places

    def __init__(self, name: str, color: str, speed: float, hp: int, x: int, y: int, z: int, batch: pyglet.graphics.Batch):
        self.name = name
        self.colour = color
        self.speed = speed
        self.hp = hp
        self.x = x
        self.y = y
        self.z = z
        self.batch = batch

        self.image = pyglet.resource.image('img/' + color + constant.ENEMY)

        self.sprite = pyglet.sprite.Sprite(self.image, x = 160 + x * 80 + 20, y = 170 + (constant.LINE - 1 - y) * 80 + 20, z = z, batch = self.batch)

        if constant.DEBUG or constant.DEBUG_ENEMY:
            print(f'(i, j) = ({y}, {x}) -> (x, y) -> ({160 + x * 80 - 20}, {170 + (constant.LINE - 1 - y) * 80})')

        self.visited = [[0 for x in range(COLUMN)] for y in range(LINE)]

    # calculate the new coordinates
    def newCoordinates(self, x: int, y: int, matrix: list):
        i = (x - 160) / 80      # i = line in the matrix
        j = (820 - y) / 80      # j = column in the matrix

        i = round(i)
        j = round(j)

        isValid = False

        if constant.DEBUG_ENEMY:
            print(f'matrix:')
            for k in range(0, constant.LINE):
                print(matrix[k])
            print (f'(x_prev, y_prev) = ({x}, {y})')
            print (f'(i, j) = ({i}, {j})')

        self.visited[i][j] = 1

        if(matrix[i - 1][j] == 0 and self.visited[i - 1][j] == 0):     # free position up
            self.visited[i - 1][j] = 1
            i = i - 1
            isValid = True
        elif(matrix[i + 1][j] == 0 and self.visited[i + 1][j] == 0):   # free position down
            self.visited[i + 1][j] = 1
            i = i + 1
            isValid = True
        elif(matrix[i][j - 1] == 0 and self.visited[i][j - 1] == 0):   # free position left
            self.visited[i][j - 1] = 1
            j = j - 1
            isValid = True
        elif(matrix[i][j + 1] == 0 and self.visited[i][j + 1] == 0):   # free position right
            self.visited[i][j + 1] = 1
            j = j + 1
            isValid = True

        x = 80 * i + 160        # new x(pixel)
        y = 820 - 80 * j        # new y(pixel)

        if constant.DEBUG_ENEMY:
            print(f'visited:')
            for k in range(0, constant.LINE):
                print(self.visited[k])
            print (f'(x_next, y_next) = ({x}, {y})')
            print (f'(i, j) = ({i}, {j})')

        if isValid:
            return (x, y)

        return -1

    def hide(self):
        self.sprite.batch = None
        self.image.batch = None

    def show(self):
        self.sprite.batch = self.batch
        self.image.batch = self.batch