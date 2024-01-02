import constant
import gameUtils
import pyglet
from building import Building

class Building_blue(Building):

    def __init__(self, name: str, shape: str, cooldown: int, radius: float, x: int, y: int, z: int, batch: pyglet.graphics.Batch):
        super().__init__(name, shape, cooldown, radius, x, y, z, batch)

        self.image = pyglet.image.load(gameUtils.getFilePath(constant.BLUE + shape, constant.TYPE_IMAGE))
        self.sprite = pyglet.sprite.Sprite(img = self.image, x = x, y = y, z = z, batch = batch)
