from agglomerate.main.misc.vector2 import Vector2
from agglomerate.main.misc.color import Color


class Settings:
    """
    Keeps track of all the packer settings

    **Settings**
    algorithm
        name of the algorithm to use
    format
        name of the coordinates file format
    output_sheet_path
        where to save the generated sprite sheet
    output_coordinates_path
        where to save the generated coordinates file
    allow
        dictionary containing allowed settings
    require
        dictionary containing required settings
    sheet_size
        Vector2 that contains size of the generated sprite sheet image,
        values can be "auto"
    background_color
        color to use as the background of the sheet

    **Allowed dictionary**
    - rotation: True if the user allows the rotation of sprites
    - cropping: True if the user allows cropping of sprites

    **Required dictionary**
    - square_sheet_size: True if a squared sheet is required
    - power_of_two_sheet_size: True if power-of-two dimensions are required
    - padding: Padding to apply to sprites, can be False or an integer
    """
    def __init__(self, algorithm=None, format=None):
        """
        Creates a settings object.

        Sets remaining options to default values, must specify an algorithm,
        format, output_sheet_path and output_coordinates_path because these
        have no default values

        **Default values**
        - algorithm: None
        - format: None
        - output_sheet_path: None
        - output_coordinates_path: None

        - allow
            - "rotation": False
            - "cropping": False

        - require
            - "square_sheet_size": False
            - "power_of_two_sheet_size": False
            - "padding": False

        - sheet_size: both x and y set to auto
        - background_color: transparent (#00000000)
        """
        self.algorithm = algorithm
        self.format = format
        self.output_sheet_path = None
        self.output_coordinates_path = None

        self.allow = {
                     "rotation": False,
                     "cropping": False
                     }

        self.require = {
                        "square_sheet_size": False,
                        "power_of_two_sheet_size": False,
                        "padding": False
                        }

        self.sheet_size = Vector2("auto", "auto")
        self.background_color = Color.from_hex("#00000000")


    @classmethod
    def from_dict(cls, dictionary):
        """
        Returns a Settings instance with values set from a dictionary.

        All values must be in the dictionary, sheet_size value must be also a
        dictionary, background_color must be a hex value string
        """
        # create a settings instance
        s = Settings()

        # fill it with the dictionary values
        s.algorithm = dictionary["algorithm"]
        s.format = dictionary["format"]
        s.output_sheet_path = dictionary["output_sheet_path"]
        s.output_coordinates_path = dictionary["output_coordinates_path"]
        s.allow = dictionary["allow"]
        s.require = dictionary["require"]
        # sheet_size is a dictionary, we need to create a Vector2 instance
        # Vector2 can be initialized from a dict
        s.sheet_size = Vector2()
        s.sheet_size = Vector2.from_dict(dictionary["sheet_size"])
        # background_color is a hex code string, we need a Color instance
        s.background_color = Color.from_hex(dictionary["background_color"])

        return s


    def to_dict(self):
        """
        Returns a dictionary of the fields in the settings instance. Also
        converts sheet_size to a dictionary and beckground_color to a hex code
        """
        return {
            "algorithm": self.algorithm,
            "format": self.format,
            "output_sheet_path": self.output_sheet_path,
            "output_coordinates_path": self.output_coordinates_path,
            "allow": self.allow,
            "require": self.require,
            # sheet size is an object, we need to store it also as a dict
            "sheet_size": self.sheet_size.to_dict(),
            # background_color is a object, we need to store it as a hex string
            "background_color": self.background_color.to_hex()
        }
