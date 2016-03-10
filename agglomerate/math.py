import collections
import math


class Vector2:
    """
    Class used for storing sizes, rectangles, coordinates, etc.
    """
    def __init__(self, x=0, y=0):
        """
        Initialize to given values, defaults to 0
        """
        self.x = x
        self.y = y


    @classmethod
    def from_tuple(cls, tuple):
        """
        Creates a Vector2 from a tuple.

        Tuple must be (x, y)
        """
        x, y = tuple
        return Vector2(x, y)


    @classmethod
    def from_dict(cls, dictionary):
        """
        Creates a Vector2 from a dictionary.

        Dictionary must have "x" and "y" values
        """
        return Vector2(dictionary["x"], dictionary["y"])


    def set(self, x, y):
        """
        Set to given values.
        """
        self.x = x
        self.y = y


    def set_x(self, x):
        """
        Set x value.
        """
        self.x = x


    def set_y(self, y):
        """
        Set y value.
        """
        self.y = y


    def length(self):
        """
        Returns length
        """
        return math.sqrt(x*x + y*y)


    def to_tuple(self):
        """
        Return a tuple containing (x, y)
        """
        return (self.x, self.y)


    def to_dict(self):
        """
        Return a dictionary containing "x" and "y" values
        """
        return {"x": self.x, "y": self.y}


    def __repr__(self):
        return "({}, {})".format(self.x, self.y)


    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)


    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
