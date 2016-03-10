import PIL.Image
import os
import agglomerate.main.math

class Item:
    """
    Represents a sprite or a group of sprites, with a rectangular shape.
    Something that will be managed by an algorithm.

    Sprites can be cropped but groups not.

    An algorithm works with items, placing them and rotating if necessary,
    algorithms can crop sprites but can't crop groups, so they need to check the
    type field.

    **Fields**
    position
        Vector2 position in the container (sheet or group) in pixels, top-left
        corner regardless of rotation.
    size
        Vector2 in pixels of the sprite in the sheet
    rotated
        true if the item was rotated 90 degrees clockwise by the algorithm
    type
        string, can be "sprite", "group", "parameters" or None
    """

    def __init__(self, position=agglomerate.main.math.Vector2(),
                 size=agglomerate.main.math.Vector2()):
        """
        Creates an item with the optional given position and size Vector2
        """
        self.position = position
        self.size = size
        self.rotated = False
        self.type = None



class Sprite(Item):
    """
    Item that contains a PIL image and it's metadata.

    Sprites can be cropped analysing the images.

    **Fields**
    image
        PIL image
    name
        name string to be used when creating the coordinates file

    rotated
        true if the sprite was rotated 90 degrees clockwise by the algorithm
    cropped
        true if the sprite was cropped

    position
        Vector2 position in the sheet in pixels, top-left corner regardless of
        rotation.
    size
        Vector2 in pixels of the sprite in the sheet, this is'nt the original
        size if the sprite was cropped
    original_size
        Vector2 in pixels of the original size of the sprite

    crop_l
        Amount of pixels cropped in the left
    crop_t
        Amount of pixels cropped in the top
    crop_r
        Amount of pixels cropped in the right
    crop_b
        Amount of pixels cropped in the bottom
    """

    def __init__(self, path):
        """
        Opens the image in the specified file and processes it

        :param str path: path to image file
        """
        self.image = PIL.Image.open(path)
        self.name = self.get_name_from_path(path)

        self.rotated = False
        self.cropped = False

        self.position = None

        self.size = agglomerate.main.math.Vector2.from_tuple(self.image.size)
        self.original_size = self.size

        self.crop_l = 0
        self.crop_t = 0
        self.crop_r = 0
        self.crop_d = 0

        self.type = "sprite"

    def get_name_from_path(self, path):
        """
        Generates a name from the file name

        The name is the file name

        :param str path: path to file
        :return: file name
        :rtype: str
        """
        return os.path.basename(path)


class Group(Item):
    """
    Has a list of items, a settings instance, and the inherited attributes
    from Item

    Example tree::

        group
        ├─ items (list)
        |  ├─ group1
        |  |  ├─ items (list)
        |  |  └─ settings
        |  ├─ group2
        |  |  ├─ items (list)
        |  |  └─ settings
        |  ├─ sprite1
        |  ├─ sprite2
        |  └─ ...
        |
        └─ settings
    """
    def __init__(self, items, settings):
        self.items = items
        self.settings = settings
        self.position = None
        self.size = settings.size
        self.rotated = False
        self.type = "group"
