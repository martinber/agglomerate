from __future__ import print_function

import argparse
import json
from agglomerate.main import packer
from agglomerate.main.sprite import Sprite
from agglomerate.main.settings import Settings
from agglomerate.main.misc.vector2 import Vector2
from agglomerate.main.misc.color import Color
from agglomerate.main.formats import format

import fnmatch
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
        sprites_paths, settings = _load_parameters_from_arguments(args)
        sprites, settings = _process_parameters(sprites_paths, settings)
        packer.pack(sprites, settings)
    elif args.subparser == "from":
        sprites_paths, settings = _load_parameters_from_file(args.path)
        sprites, settings = _process_parameters(sprites_paths, settings)
        packer.pack(sprites, settings)
    elif args.subparser == "new":
        _create_parameters_file(args.path)


def _load_parameters_from_arguments(args):
    """
    Creates a sprites paths list and a transitory settings instance from the
    arguments given to the command, later these should be processed by the
    _process_parameters method.

    :param args: args from argparse
    :return: tuple of sprites paths list and transitory settings instance
    """

    # Sprite paths list
    sprite_paths = args.images

    # Create transitory settings
    settings = Settings(args.algorithm, args.format)
    settings.output_sheet_path = args.output[0]
    settings.output_coordinates_path = args.output[1]
    settings.output_sheet_format = args.image_format
    # the _process_parameters method will parse the string into a Color
    settings.background_color = args.background_color
    # the _process_parameters method will parse it later into a Vector2
    settings.sheet_size = args.size

    return (sprite_paths, settings)


def _load_parameters_from_file(path):
    """
    Creates a sprites paths list and a transitory settings instance from the
    file given, later these should be processed by the _process_parameters
    method.

    :param path: path to parameters file
    :return: tuple of sprites paths list and transitory settings instance
    """
    # Read json
    with open(path, "r") as f:
        json_string = f.read()

    root = json.loads(json_string)

    sprites_paths = root["sprites"]
    settings_dict = root["settings"]

    # create transitory settings
    settings = Settings.from_dict(settings_dict)

    return (sprites_paths, settings)


def _process_parameters(sprites_paths, settings):
    """
    Creates the sprites list and check the transitory settings given, returns
    the sprites list and the settings ready for packing

    :param list sprites_paths: a list of path strings, can contain wildcards
    :param settings: transitory settings instance
    :return: tuple containing the sprites list and the settings instance
    """
    # Match every path given, some can contain wildcards
    matching_paths = []
    for s in sprites_paths:
        matching_paths.extend(_get_matching_files(s))

    if not matching_paths:
        sys.exit("Could not find any image")

    # print found images
    print("Found images:")
    for p in matching_paths:
        print("    ", p)

    # create sprites
    sprites = [Sprite(path) for path in matching_paths]


    # Check settings

    # the color given by the user is a string, we need to create the Color
    # instance
    if isinstance(settings.background_color, basestring):
        settings.background_color = Color.from_hex(settings.background_color)

    # the size given by the user is a string, we need to create the Vector2
    if isinstance(settings.sheet_size, basestring):
        settings.sheet_size = _parse_size(settings.sheet_size)

    if settings.output_sheet_format != None:
        # check the given format, the format shouldn't start with a dot
        if settings.output_sheet_format[0] == ".":
            settings.output_sheet_format = settings.output_sheet_format[1:]

    print(settings.output_sheet_path)
    # if output_sheet_path doesn't have extension
    if os.path.splitext(settings.output_sheet_path)[1] == "":
        # if user didn't say what extension to use
        if settings.output_sheet_format == None:
            # set image format to png
            settings.output_sheet_format = "png"

        # add extension to output_sheet_path
        settings.output_sheet_path += "." + settings.output_sheet_format

    # if output_coordinates_path doesn't have extension
    if os.path.splitext(settings.output_coordinates_path)[1] == "":
        # add the suggested extension by the format
        settings.output_coordinates_path += "." + \
                format.get_format(settings.format).suggested_extension


    return (sprites, settings)


def _create_parameters_file(path):
    """
    Saves an example json file where the sprites and the settings are
    specified.

    The json file consists of a root object that contains a sprites array of
    strings and a settings object

    :param str path: path where to save file
    """
    settings = Settings(_default_algorithm, _default_format)
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


def _get_matching_files(path):
    """
    Returns a list of paths that are matched by the given string. e.g. *.png

    Used to support unix style wildcards, e.g. file_*, sprites/*.png or ./f.png

    Adds ./ at the beggining of the path if given path doesn't have directory

    :param str path:
    :return: list of matching file paths
    :rtype: list of str
    """
    directory = os.path.dirname(path)
    if directory == "":
        directory = "./"
    pattern = os.path.basename(path)
    # Files in given directory
    available_files = os.listdir(directory)
    # Files matched
    files = []

    for f in available_files:
        if fnmatch.fnmatch(f, pattern):
            files.append(os.path.join(directory, f))

    return files


def _parse_size(string):
    """
    Interpret given size string:

    String must be for example 100x200, 530x, x200 or auto. No number means
    auto

    :param str string:
    :return: sheet size
    :rtype: classes.Vector2
    """
    if string.find("x") < 0:
        if string == "auto":
            return Vector2("auto", "auto")
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

            return Vector2(x, y)
