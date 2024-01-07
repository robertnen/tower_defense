import pyglet
import math
import constant
from enemy import Enemy

class Building():
    color = None
    shape = None    # hexagon, square or triangle
    radius = None
    cooldown = None

    x = None        # coordinates
    y = None
    z = None        # z-index

    image = None
    sprite = None
    batch = None

    def __init__(self, color: str, shape: str, cooldown: int, radius: float, x: int, y: int, z: int, batch: pyglet.graphics.Batch):
        self.color = color
        self.shape = shape
        self.cooldown = cooldown
        self.radius = radius
        self.x = x
        self.y = y
        self.z = z
        self.batch = batch

        self.image = pyglet.resource.image('img/' + color + shape)
        self.image.anchor_x = 30
        self.image.anchor_y = 30
        self.sprite = pyglet.sprite.Sprite(self.image, x = x, y = y, z = z, batch = self.batch)

    def calculate_distance(self, enemy_x: int, enemy_y: int):

        result = math.sqrt((self.sprite.x - enemy_x) ** 2 + (self.sprite.y - enemy_y) ** 2)

        if constant.DEBUG or constant.DEBUG_BUILDING:
            print(f'Coords: Building({self.x}, {self.y}) -> Enemy({enemy_x}, {enemy_y}) = {result}')

        return result

    def is_enemy_in_radius(self, enemy: Enemy):
        distance = self.calculate_distance(enemy.sprite.x, enemy.sprite.y)

        if constant.DEBUG or constant.DEBUG_BUILDING:
            print(f'Distance from enemy = {distance} | Coords = ({enemy.sprite.x}, {enemy.sprite.y}) | Radius = {self.radius} | isInRadius = {distance <= self.radius}')

        return distance <= self.radius

    def find_closest_enemy(self, enemies: list[Enemy]) -> (Enemy, int):
        if not enemies:
            return None

        # Initialize variables to store the closest enemy and the minimum distance
        closest_enemy = None
        min_distance = float('inf')

        i = 0

        # Iterate through each enemy and find the closest one within the radius
        for enemy in enemies:
            if enemy == None:
                continue

            i = i + 1
            distance = self.calculate_distance(enemy.sprite.x, enemy.sprite.y)
            if distance < min_distance and self.is_enemy_in_radius(enemy):
                min_distance = distance
                closest_enemy = enemy

        if constant.DEBUG or constant.DEBUG_BUILDING:
            print("=======================================================================")
            print(f'Enemy list coors:')
            for enemy in enemies:
                if enemy != None:
                    print(f'({enemy.sprite.x}, {enemy.sprite.y}) | distance = {self.calculate_distance(enemy.sprite.x, enemy.sprite.y)}', end=' ')

            if closest_enemy != None:
                print(f'\nMin distance = {min_distance} | Enemy coords = ({closest_enemy.x}, {closest_enemy.y})')
            print("=======================================================================")

        return closest_enemy, i

    def hide(self):
        self.sprite.batch = None
        self.image.batch = None

    def show(self):
        self.sprite.batch = self.batch
        self.image.batch = self.batch