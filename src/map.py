import constant
import gameUtils

class Map:
    height = constant.HEIGHT_MAP
    width = constant.WIDTH_MAP

    xStart = constant.X_START_MAP     # coords of starting position
    yStart = constant.Y_START_MAP

    matrix = None
    pathfile = None

    isValid = True           # if the map is valid or not

    def find_start(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == 4:
                    return i, j
        return -1  # invalid map

    def find_destination(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == 5:
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

    def __init__(self, map_path):

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
