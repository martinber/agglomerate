import PIL.Image
import os
from classes import Vector2

class Sprite:
    """
    Contains a PIL image and it's metadata

    **Fields**
    image
        PIL image
    size
        tuple in pixels
    rotation
        rotation in degrees to be applied when creating the sheet
    position
        tuple position in the sheet in pixels, top-left corner regardless of
        rotation
    name
        name to be used when creating the coordinates file

    """

    def __init__(self, path):
        """
        Opens the image in the specified file and processes it

        :param str path: path to image file
        """
        self.image = PIL.Image.open(path)

        w, h = self.image.size
        self.size = Vector2(w, h)

        self.rotation = 0
        self.position = None
        self.name = self.get_name_from_path(path)

    def get_name_from_path(self, path):
        """
        Generates a name from the file name

        The name is the file name

        :param str path: path to file
        :return: file name
        :rtype: str
        """
        return os.path.basename(path)
