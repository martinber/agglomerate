# We want to import every algorithm, also imports module "algorithm"
#from agglomerate.main.algorithms import *
# We want to import every format, also imports module "format"
#from agglomerate.main.formats import *
import agglomerate.main.algorithms.algorithm
import agglomerate.main.algorithms.binarytree
import agglomerate.main.algorithms.inline
import agglomerate.main.formats.format
import agglomerate.main.formats.simplejson


import PIL


def pack(sprites, settings):
    """
    Packs the sprites.

    Saves the result image and the coordinates file according to settings.

    Checks compatibility between the algorithm, the format and the settings
    raising exceptions accordingly, but it is recommended to check
    compatibility before calling this function so you can print more
    warnings and more information to the user.

    In the settings given, output_sheet_path must have extension. But if
    output_coordinates_path doesn't have extension, the packer will use
    a default one based on the format chosen

    :param list sprites: list of sprite objects
    :param settings: settings object
    """
    # Get an instance of the algorithm and format named in the settings
    a = agglomerate.main.algorithms.algorithm.get_algorithm(settings.algorithm)
    f = agglomerate.main.formats.format.get_format(settings.format)

    # Check if the chosen algorithm and output format is compatible with
    # the specified settings
    compatible, __, __ = agglomerate.main.algorithms.algorithm.check_compatibility(a, settings)
    if not compatible:
        raise IncompatibleAlgorithmException(settings.algorithm)

    compatible, __, __ = agglomerate.main.formats.format.check_compatibility(f, settings)
    if not compatible:
        raise IncompatibleFormatException(settings.format)

    # Run the algorithm
    a.pack(sprites, settings)
    # Join together the sprites and save the image
    _generate_sheet(sprites, settings)
    # Generate the coordinates file string
    coordinates = f.generate(sprites, settings)
    # Save the coordinates file
    _save_coordinates(coordinates, settings)


def _generate_sheet(sprites, settings):
    """
    Creates the sheet pasting the sprites in the locations given by the
    algorithm and then saves the image.
    """
    sheet = PIL.Image.new(settings.output_sheet_color_mode,
                          settings.sheet_size.to_tuple(),
                          settings.background_color.to_tuple())

    for s in sprites:
        sheet.paste(s.image, s.position.to_tuple(), s.image)
        print("Placed in")
        print(s.position)

    # if output_sheet_format is an unicode string, pillow has problems
    if isinstance(settings.output_sheet_format, unicode):
        settings.output_sheet_format = \
                settings.output_sheet_format.encode("ascii", "ignore")

    sheet.save(settings.output_sheet_path, settings.output_sheet_format)


def _save_coordinates(coordinates, settings):
    """
    Saves the generated string into a file.

    The output file is defined in the settings, if the path given doesn't have
    extension, the format's default extension will be used
    """
    with open(settings.output_coordinates_path, "w") as f:
        f.write(coordinates)


# -----------------------------------------------------------------------------
# Exceptions
# -----------------------------------------------------------------------------


class IncompatibleAlgorithmException(Exception):
    """
    Raised when the selected algorithm and settings are incompatible

    :param str algorithm_name:
    :param str reason: why the algorithm is incompatible, optional
    """
    def __init__(self, algorithm_name, reason=""):
        self.algorithm_name = algorithm_name

        # Set the message by calling parent's constructor
        message = "Format {} is incompatible with the given settings, {}" \
            .format(format_name, reason)
        super(IncompatibleAlgorithmException, self).__init__(message)


class IncompatibleFormatException(Exception):
    """
    Raised when the selected format and settings are incompatible

    :param str algorithm_name:
    :param str reason: why the algorithm is incompatible, optional
    """
    def __init__(self, format_name, reason):
        self.format_name = format_name

        # Set the message by calling parent's constructor
        message = "Format {} is incompatible with the given settings, {}" \
            .format(format_name, reason)
        super(IncompatibleAlgorithmException, self).__init__(message)
