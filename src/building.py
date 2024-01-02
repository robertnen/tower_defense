import pyglet
import math
import constant
from enemy import Enemy

class Building():
    name = None
    shape = None    # hexagon, square or triangle
    radius = None
    cooldown = None

    x = None        # coordinates
    y = None
    z = None        # z-index

    image = None
    sprite = None
    batch = None

    def __init__(self, name: str, shape: str, cooldown: int, radius: float, x: int, y: int, z: int, batch: pyglet.graphics.Batch):
        self.name = name
        self.shape = shape
        self.cooldown = cooldown
        self.radius = radius
        self.x = x
        self.y = y
        self.z = z
        self.batch = batch

    def calculate_distance(self, enemy_x: int, enemy_y: int):

        result = math.sqrt((self.x - enemy_x) ** 2 + (self.y - enemy_y) ** 2)

        if constant.DEBUG or constant.DEBUG_BUILDING:
            print(f'Coords: Building({self.x}, {self.y}) -> Enemy({enemy_x}, {enemy_y}) = {result}')

        return result

    def is_enemy_in_radius(self, enemy: Enemy):
        distance = self.calculate_distance(enemy.x, enemy.y)

        if constant.DEBUG or constant.DEBUG_BUILDING:
            print(f'Distance from enemy = {distance} | Coords = ({enemy.x}, {enemy.y}) | Radius = {self.radius} | isInRadius = {distance <= self.radius}')

        return distance <= self.radius

    def find_closest_enemy(self, enemies: list[Enemy]) -> Enemy:
        if not enemies:
            return None

        # Initialize variables to store the closest enemy and the minimum distance
        closest_enemy = None
        min_distance = float('inf')

        # Iterate through each enemy and find the closest one within the radius
        for enemy in enemies:
            distance = self.calculate_distance(enemy.x, enemy.y)
            if distance < min_distance and self.is_enemy_in_radius(enemy):
                min_distance = distance
                closest_enemy = enemy

        if constant.DEBUG or constant.DEBUG_BUILDING:
            print("=======================================================================")
            print(f'Enemy list coors:')
            for enemy in enemies:
                print(f'({enemy.x}, {enemy.y}) | distance = {self.calculate_distance(enemy.x, enemy.y)}', end=' ')

            print(f'\nMin distance = {min_distance} | Enemy coords = ({closest_enemy.x}, {closest_enemy.y})')
            print("=======================================================================")

        return closest_enemy

    def hide(self):
        self.sprite.batch = None
        self.label.batch = None

    def show(self):
        self.sprite.batch = self.batch
        self.label.batch = self.batch