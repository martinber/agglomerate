from __future__ import print_function

import agglomerate
import agglomerate.packer
import agglomerate.settings
import agglomerate.math
import agglomerate.format
import agglomerate.util

import argparse
import json
import os
import sys


"""
Commandline interface for the packer.

Allows parameters as arguments, but also can load parameters from a json file
"""


_default_algorithm = "binarytree"
_default_format = "simplejson"
_default_output_sheet_path = "sheet"
_default_output_coordinates_path = "coordinates"
_default_size = "auto"


def main():
    print("Welcome to agglomerate!")

    # create parser
    parser = argparse.ArgumentParser(prog="agglomerate",
                                     description="Simple texture packer.")
    subparsers = parser.add_subparsers(dest="subparser", help="prueba")

    # parser for "agglomerate pack ..."
    parser_pack = subparsers.add_parser("pack",
            help="pack from commandline arguments")

    parser_pack.add_argument("-i", "--images", nargs="+",
            help="create from paths to images, can use wildcards")
    parser_pack.add_argument("-a", "--algorithm", default=_default_algorithm,
            help="specify packing algorithm")
    parser_pack.add_argument("-f", "--format", default=_default_format,
            help="specify output format for coordinates file")
    parser_pack.add_argument("-s", "--size", default=_default_size,
            help=("size of the sheet in pixels, no number means auto e.g. "
                  "400x500 or 400x or x100 or auto"))
    parser_pack.add_argument("-o", "--output", nargs=2,
                             default=[_default_output_sheet_path,
                                      _default_output_coordinates_path],
            help=("where to save the output sheet and coordinates file, no "
                  "extension means automatic extension, using 'sheet' and "
                  "'coords' by default. If no extension is given, the"
                  "--image-format extension is appended (png by default)"))
    parser_pack.add_argument("-F", "--image-format", default=None,
            help=("image format to use, using given output extension or 'png' "
                  "by default. Write for example 'png' or '.png'"))
    parser_pack.add_argument("-c", "--background-color", default="#00000000",
            help=("background color to use, must be a RGB or RGBA hex value, "
                  "for example #FFAA9930 or #112233, transparent by default: "
                  "#00000000"))

    # parser for "agglomerate new ..."
    parser_new = subparsers.add_parser("new",
            help=("create parameters file, so you can load them with "
                  "'agglomerate from ...'"))

    parser_new.add_argument("path", default="parameters.json",
            help="path to the file to create, 'parameters.json' by default")

    # parser for "agglomerate from ..."
    parser_from = subparsers.add_parser("from",
            help=("load a parameters file containing settings and sprites to "
                  "pack"))

    parser_from.add_argument("path", default="parameters.json",
            help="path to the file to load, 'parameters.json' by default")

    # parse and work
    args = parser.parse_args()

    if args.subparser == "pack":
        params = _load_parameters_from_arguments(args)
        agglomerate.packer.pack(params)
    elif args.subparser == "from":
        params = _load_parameters_from_file(args.path)
        agglomerate.packer.pack(params)
    elif args.subparser == "new":
        _create_parameters_file(args.path)


def _load_parameters_from_arguments(args):
    """
    Loads the parameters from the commandline arguments.

    :param args: args from argparse
    :return: parameters instance ready for packing
    """

    # sprite paths list
    sprites_paths = args.images

    # parse the items to pack, we don't need groups here
    items = []
    for s in sprites_paths:
        sprites_paths = agglomerate.util.get_matching_paths(i)
        for p in sprites_paths:
            items.append(agglomerate.Sprite(p))

    # create transitory settings
    settings = agglomerate.SheetSettings(args.algorithm, args.format)
    settings.output_sheet_path = args.output[0]
    settings.output_coordinates_path = args.output[1]
    settings.output_sheet_format = args.image_format
    # the _process_parameters method will parse the string into a Color
    settings.background_color = args.background_color
    # the _process_parameters method will parse it later into a Vector2
    settings.size = args.size

    # create the parameters instance
    params = agglomerate.Parameters(items, settings)

    return _process_parameters_settings(params)


def _load_parameters_from_file(path):
    """
    Loads the parameters from a json file.

    :param path: path to parameters file
    :return: parameters instance ready for packing
    """
    # Read json
    with open(path, "r") as f:
        json_string = f.read()

    root = json.loads(json_string)

    params = _parse_group(root, True)

    return _process_parameters_settings(params)

def _process_parameters_settings(params):
    """
    Helper function for _load_parameters_from_X. Finishes building the
    parameters settings.

    params.settings that are processed:
        - background_color: If it is a string we create the Color assuming that
                the string is an hex value
        - size: If it is a string we create the Vector2 using
                _parse_size()
        - output_sheet_format: If given, we strip the dot at the start of the
                string
        - output_sheet_path: We add a extension if none given, the extension
                given is the output_sheet_format, or "png" of none given
        - output_coordinates_path: We add the recommended extension by the
                format if no extension is given
    """
    # the color given by the user is a string, we need to create the Color
    # instance
    if isinstance(params.settings.background_color, str):
        params.settings.background_color = agglomerate.utils. \
                Color.from_hex(params.settings.background_color)

    # the size given by the user is a string, we need to create the Vector2
    if isinstance(params.settings.size, str):
        params.settings.size = _parse_size(params.settings.size)

    if params.settings.output_sheet_format != None:
        # check the given format, the format shouldn't start with a dot
        if params.settings.output_sheet_format[0] == ".":
            params.settings.output_sheet_format = \
                    params.settings.output_sheet_format[1:]

    # if output_sheet_path doesn't have extension
    if os.path.splitext(params.settings.output_sheet_path)[1] == "":
        # if user didn't say what extension to use
        if params.settings.output_sheet_format == None:
            # set image format to png
            params.settings.output_sheet_format = "png"

        # add extension to output_sheet_path
        params.settings.output_sheet_path += \
                "." + params.settings.output_sheet_format

    # if output_coordinates_path doesn't have extension
    if os.path.splitext(params.settings.output_coordinates_path)[1] == "":
        # add the suggested extension by the format
        chosen_format = \
                agglomerate.format.get_format(params.settings.format)

        params.settings.output_coordinates_path += \
                "." + params.chosen_format.suggested_extension

    return params


def _create_parameters_file(path):
    """
    Saves an example parameters json file where the sprites and the settings
    are specified.

    :param str path: path where to save file
    """
    settings = agglomerate.SheetSettings(_default_algorithm, _default_format)

    settings_dict = settings.to_dict()

    sprites = ["example/path/*.png"]

    root = {
        "sprites": sprites,
        "settings": settings_dict
    }

    # create json string indented by 4 spaces
    json_string = json.dumps(root, indent=4)

    with open(path, "w") as f:
        f.write(json_string)


def _parse_size(string):
    """
    Interprets a size string and returns a Vector2.

    String must be for example 100x200, 530x, x200 or auto. No number means
    auto

    :param str string:
    :return: size Vector2
    """
    if string.find("x") < 0:
        if string == "auto":
            return agglomerate.math.Vector2("auto", "auto")
        else:
            print("Invalid size " + string)
            sys.exit()
    else:
        dimensions = string.split("x", 1)
        if len(dimensions) is not 2:
            print("Invalid size " + string)
            sys.exit()
        else:
            x, y = dimensions

            if x == "":
                x = "auto"
            else:
                try:
                    x = int(x)
                except:
                    print("Invalid size " + string)
                    sys.exit()

            if y == "":
                y = "auto"
            else:
                try:
                    y = int(y)
                except:
                    print("Invalid size " + string)
                    sys.exit()

            return agglomerate.math.Vector2(x, y)


def _parse_group(dictionary, is_params):
    """
    Takes a dictionary that represents a group (or a parameters object) and
    returns a group/parameters instance, parsing child groups recursively.

    The structure of a parameters dictionary is as follows::

        parameters (dict)
                ├─ items (list)
        |  ├─ group1 (dict)
        |  |  ├─ items (list)
        |  |  └─ settings (dict)
        |  ├─ group2 (dict)
        |  |  ├─ items (list)
        |  |  └─ settings (dict)
        |  ├─ sprite1 (string)
        |  ├─ sprite2 (string)
        |  └─ ...
        |
                └─ settings

    :param dict dictionary: dictionary that represents the group
    :param bool is_params: True if the group is a parameters group
    :return: Group or Parameters instance
    """
    raw_items = dictionary["items"]
    items = []
    for i in raw_items:
        if isinstance(i, str): # means that i is a sprite path
            sprites_paths = agglomerate.util.get_matching_paths(i)
            for p in sprites_paths:
                items.append(agglomerate.Sprite(p))

        else: # means that i is a dictionary i.e. a group
            items.append(_parse_group(i, False))

    settings_dict = dictionary["settings"]

    if is_params:
        settings = agglomerate.SheetSettings.from_dict(settings_dict)

        return agglomerate.Parameters(items, settings)
    else:
        settings = agglomerate.Settings.from_dict(settings_dict)

        return agglomerate.Group(items, settings)
