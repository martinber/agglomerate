import argparse
from main import packer
from main.sprite import Sprite
from main.settings import Settings

def main():
    print("Welcome to agglomerate!")

    parser = argparse.ArgumentParser(description="Simple texture packer.")
    parser.add_argument("-a", "--algorithm", default="simple",
                        help="specify packing algorithm")
    parser.add_argument("-f", "--format", default="simplejson",
                        help="specify output format for coordinates file")
    args = parser.parse_args();

    settings = Settings(args.algorithm, args.format)
    settings.output_sheet_path = "sheet.png"
    settings.output_coordinates_path = "coordinates.json"

    sprites = [Sprite("ball1.png")]

    packer.pack(sprites, settings)
