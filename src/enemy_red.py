import constant
import gameUtils
import pyglet
from enemy import Enemy

class Enemy_red(Enemy):
   def __init__(self, name: str, color: str, speed: float, hp: int, x: int, y: int, z: int, batch: pyglet.graphics.Batch):
      super().__init__(name, color, speed, hp, x, y, z, batch)
      self.image= pyglet.image.load(gameUtils.getFilePath(color + constant.ENEMY, constant.TYPE_IMAGE))

      self.sprite = pyglet.sprite.Sprite(img = self.image, x = x, y = y, z = z, batch = batch)

   


