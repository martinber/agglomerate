import PIL.Image
import os
from agglomerate.main.classes import Vector2


class Sprite:
    """
    Contains a PIL image and it's metadata

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

        w, h = self.image.size
        self.size = Vector2(w, h)
        self.original_size = self.size

        self.crop_l = 0
        self.crop_t = 0
        self.crop_r = 0
        self.crop_d = 0

    def get_name_from_path(self, path):
        """
        Generates a name from the file name

        The name is the file name

        :param str path: path to file
        :return: file name
        :rtype: str
        """
        return os.path.basename(path)
