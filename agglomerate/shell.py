import argparse
from main import packer
from main.sprite import Sprite
from main.settings import Settings

def main():
    print("Hola")

    parser = argparse.ArgumentParser(description="Simple texture packer.")

    parser.add_argument("-a", "--algorithm", default="simple",
                        help="specify packing algorithm")
    parser.add_argument("-f", "--format", default="simplejson",
                        help="specify output format for coordinates file")

    args = parser.parse_args();

    print(args.algorithm)

    settings = Settings(args.algorithm, args.format)
    sprites = [Sprite("ball1.png")]

    packer.pack(sprites, settings)
