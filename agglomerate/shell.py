from __future__ import print_function

import argparse
from main import packer
from main.sprite import Sprite
from main.settings import Settings
from main.classes import Vector2

import fnmatch
import os
import sys

def main():
    print("Welcome to agglomerate!")

    parser = argparse.ArgumentParser(description="Simple texture packer.")
    parser.add_argument("sprites_paths", nargs="+",
                        help="paths to sprites, can use wildcards")
    parser.add_argument("-a", "--algorithm", default="simple",
                        help="specify packing algorithm")
    parser.add_argument("-f", "--format", default="simplejson",
                        help="specify output format for coordinates file")
    parser.add_argument("-s", "--size", default="auto",
                        help=("size of the sheet in pixels, no number means "
                              "auto e.g. 400x500 or 400x or x100 or auto"))
    args = parser.parse_args();

    # Create settings
    settings = Settings(args.algorithm, args.format)
    settings.output_sheet_path = "sheet.png"
    settings.output_coordinates_path = "coordinates.json"
    settings.output_sheet_size = _parse_size(args.size)

    # Match every path given, some can contain wildcards
    matching_paths = []
    for s in args.sprites_paths:
        matching_paths.extend(_get_matching_files(s))

    # Print found images
    if not matching_paths:
        sys.exit("Could not find any image")

    print("Found images:")
    for p in matching_paths:
        print("    ", p)

    # Create sprites
    sprites = [Sprite(path) for path in matching_paths]

    packer.pack(sprites, settings)

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
