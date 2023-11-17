import pyglet
import gameUtils
import constant

class Button():
    x = None        # coords
    y = None

    label = None    # main text

    image = None    # display the button
    sprite = None

    batch = None    # graphics

    def __init__(self, name: str, color: str, x: int, y: int, batch: pyglet.graphics.Batch):

        # gameUtils.getFilePath('grey_button.png', '\\assets\img\\')
        self.image = pyglet.image.load(gameUtils.getFilePath(color + constant.BUTTON, constant.TYPE_IMAGE))

        self.sprite = pyglet.sprite.Sprite(self.image, x = x, y = y, z = 100, batch = batch)

        self.label = pyglet.text.Label(name,
                                       font_name = 'Times New Roman',
                                       font_size = 28,
                                       x = x + 150,
                                       y = y + 30,
                                       z = 99,
                                       anchor_x = 'center', anchor_y = 'center',
                                       batch = batch)

        self.x = x
        self.y = y

        self.batch = batch

    def setSpriteColor(self, color : str):
        image = pyglet.image.load(gameUtils.getFilePath(color + constant.BUTTON, constant.TYPE_IMAGE))

        self.sprite.image = image
        self.image = image

    def hide(self):
        self.sprite.batch = None
        self.label.batch = None

    def show(self):
        self.sprite.batch = self.batch
        self.label.batch = self.batch