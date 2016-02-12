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
    output_width
        width of the generated sprite sheet image, can be "auto"
    output_height
        height of the generated sprite sheet image, can be "auto"
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
        - output_width: auto
        - output_height: auto
        """
        self.algorithm = algorithm
        self.format = format
        output_sheet_path: None
        output_coordinates_path: None
        allow_rotation: False
        padding: 0
        require_square_output: False
        require_power_of_two_output: False
        output_width: auto
        output_height: auto
