# ecran de 1600 x 900
# un dreptunghi format din patrate de 80 x 80
# matrice bordata de cifra 3
# functie care valideaza mapa
# functie care citeste matricea si o retine
# 9 patrate latime, 18 patrate lungime
import os
import os.path


class Map:
    def find_start(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == 4:
                    return i, j

    def find_destination(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == 5:
                    return i, j

    def dfs(self, i, j):
        if not (0 <= i < len(self.matrix) and 0 <= j < len(self.matrix[0])) or self.visited[i][j]:
            return False
        if self.matrix[i][j] == 5:
            return True
        if self.matrix[i][j] not in [0, 4]:
            return False
        self.visited[i][j] = True
        if self.dfs(i, j+1) or self.dfs(i+1, j) or self.dfs(i, j-1) or self.dfs(i-1, j):
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
    
    def read_matrix_from_file(self, filepath):
        matrix = []
        with open(filepath, 'r') as file:
            for line in file:
                # split line into list of values and convert them to int
                row = list(map(int, line.split()))
                matrix.append(row)
        return matrix

    def __init__(self):
        self.height = 720
        self.width = 1440
        self.xStart = 100
        self.yStart = 100
        self.pathfile = os.path.abspath('map1.txt')
        self.matrix = self.read_matrix_from_file(self.pathfile)
        self.start = self.find_start()
        self.destination = self.find_destination()
        self.visited = [[False for _ in range(len(self.matrix[0]))] for _ in range(len(self.matrix))]


map = Map()
for row in map.matrix:
    print(row)
print(map.check_path_exists())
