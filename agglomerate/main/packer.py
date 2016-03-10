import agglomerate.main.algorithm
import agglomerate.main.format

import PIL


def pack(params):
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

    :param params: parameters object
    """
    # get an instance of the format named in the settings
    format = agglomerate.main.format.get_format(params.settings.format)

    # check if the chosen output format is compatible with the specified
    # sheet settings
    compatible, __, __ = agglomerate.main.format. \
            check_compatibility(format, params.settings)

    if not compatible:
        raise IncompatibleFormatException(params.settings.format)

    # pack everything recusively!
    _pack_group(params)
    # get all the sprites in the params group and get absolute values of the
    # positions and rotation
    sprites = _get_sprites(params)
    # join together the sprites and save the image
    _generate_sheet(sprites, params.settings)
    # generate the coordinates file string
    coordinates = format.generate(sprites, params.settings)
    # save the coordinates file
    _save_coordinates(coordinates, params.settings)


def _pack_group(group):
    """
    Packs a group of items recursively. Setting values on items.

    Checks compatibility between the algorithm, the format and the settings
    raising exceptions accordingly, but it is recommended to check
    compatibility before calling this function so you can print more
    warnings and more information to the user.

    :param group: group to pack
    """
    # Get an instance of the algorithm and format named in the settings
    a = agglomerate.main.algorithm.get_algorithm(group.settings.algorithm)

    # Check if the chosen algorithm and output format is compatible with
    # the specified settings
    compatible, __, __ = \
            agglomerate.main.algorithm.check_compatibility(a, group.settings)

    if not compatible:
        raise IncompatibleAlgorithmException(settings.algorithm)

    # Check all items and pack the groups
    for i in group.items:
        # check if item.type = "parameters" is not neccesary because only the
        # root can be "parameters"
        if i.type == "group":
            _pack_group(i)

    # Run the algorithm
    a.pack(group.items, group.settings)



def _get_sprites(group):
    """
    Extracts all the sprites from the group and returns a list of sprites
    placed absolutely (not relative to their original groups), also calls this
    function recursively on child groups
    """
    sprites = []

    for i in group.items:
        i.position += group.position
        # TODO see what to do with rotations
        if i.type == "sprite":
            sprites.append(i)
        elif i.type == "group":
            sprites.extend(_get_sprites(i))
        else:
            sys.exit("An item has no type, abort!")

    return sprites


def _generate_sheet(sprites, settings):
    """
    Creates the sheet pasting the sprites in the locations given by the
    algorithm and then saves the image.
    """
    sheet = PIL.Image.new(settings.output_sheet_color_mode,
                          settings.size.to_tuple(),
                          settings.background_color.to_tuple())

    for s in sprites:
        sheet.paste(s.image, s.position.to_tuple(), s.image)
        print("Placed in")
        print(s.position)

    # Now in Python3 this is not needed?
    # if output_sheet_format is an unicode string, pillow has problems
    # if isinstance(settings.output_sheet_format, unicode):
    #     settings.output_sheet_format = \
    #             settings.output_sheet_format.encode("ascii", "ignore")

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
