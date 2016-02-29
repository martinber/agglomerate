from __future__ import print_function

import argparse
import json
from agglomerate.main import packer
from agglomerate.main.sprite import Sprite
from agglomerate.main.settings import Settings
from agglomerate.main.misc.vector2 import Vector2

import fnmatch
import os
import sys


"""
Commandline interface for the packer.

Allows parameters as arguments, but also can load parameters from a json file
"""


_default_algorithm = "binarytree"
_default_format = "simplejson"
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
                             default=["sheet", "coords"],
            help=("where to save the output sheet and coordinates file, no "
                  "extension means automatic extension, using 'sheet' and "
                  "'coords' by default"))
    # parser_pack.add_argument("-F", "--image-format",
    #         help=("image format to use, using given output extension or 'png' "
    #               "by default"))

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
        sprites, settings = _load_parameters_from_arguments(args)
        packer.pack(sprites, settings)
    elif args.subparser == "from":
        sprites, settings = _load_parameters_from_file(args.path)
        packer.pack(sprites, settings)
    elif args.subparser == "new":
        _create_parameters_file(args.path)


def _load_parameters_from_arguments(args):
    """
    Creates a sprites list and a settings instance from the arguments given to
    the command.

    :param args: args from argparse
    :return: tuple of sprites list and settings instance
    """

    # Match every path given, some can contain wildcards
    matching_paths = []
    for s in args.images:
        matching_paths.extend(_get_matching_files(s))

    if not matching_paths:
        sys.exit("Could not find any image")

    # Print found images
    print("Found images:")
    for p in matching_paths:
        print("    ", p)

    # Create sprites
    sprites = [Sprite(path) for path in matching_paths]


    # Create settings
    settings = Settings(args.algorithm, args.format)
    settings.output_sheet_path = args.output[0]
    settings.output_coordinates_path = args.output[1]
    settings.sheet_size = _parse_size(args.size)

    return (sprites, settings)


def _load_parameters_from_file(path):
    # Read json
    with open(path, "r") as f:
        json_string = f.read()

    root = json.loads(json_string)

    sprites_paths = root["sprites"]
    settings_dict = root["settings"]

    # Process sprites
    # Match every path given, some can contain wildcards
    matching_paths = []
    for s in sprites_paths:
        matching_paths.extend(_get_matching_files(s))

    if not matching_paths:
        sys.exit("Could not find any image")

    # Print found images
    print("Found images:")
    for p in matching_paths:
        print("    ", p)

    # Create sprites
    sprites = [Sprite(path) for path in matching_paths]

    # Process settings
    settings = Settings()
    settings.from_dict(settings_dict)

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
