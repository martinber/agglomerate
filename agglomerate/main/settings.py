from classes import Vector2

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
    allow_rotation
        whether to allow sprite rotation
    padding
        padding applied to sprites
    require_square_output
        whether a square sprite sheet is necessary
    require_power_of_two_output
        whether a power of two sized sprite sheet is necessary
    output_sheet_size
        named tuple that contains size of the generated sprite sheet image,
        (width, height), values can be "auto"
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
        self.allow_rotation = False
        self.padding = 0
        self.require_square_output = False
        self.require_power_of_two_output = False
        self.output_sheet_size = Vector2("auto", "auto")
