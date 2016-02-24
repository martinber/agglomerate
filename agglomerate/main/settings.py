from agglomerate.main.classes import Vector2


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
        dictionay containing required settings
    sheet_size
        Vector2 that contains size of the generated sprite sheet image,
        (width, height), values can be "auto"

    **Allowed dictionary**
    - rotation: True if the user allows the rotation of sprites
    - cropping: True if the user allows cropping of sprites

    **Required dictionary**
    - square_sheet_size: True if a squared sheet is required
    - power_of_two_sheet_size: True if power-of-two dimensions are required
    - padding: Padding to appli to sprites, can be False or an integer
    """
    def __init__(self, algorithm, format):
        """
        Creates a settings object

        Sets remaining options to default values

        **Default values**
        - output_sheet_path: None
        - output_coordinates_path: None
        - allow_rotation: False
        - padding: 0
        - require_square_output: False
        - require_power_of_two_output: False
        - output_sheet_size: both x and y set to auto
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
