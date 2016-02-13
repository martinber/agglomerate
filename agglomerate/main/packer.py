# Import all algorithms and formats so they get registered
# We want to import every algorithm, also imports module "algorithm"
from algorithms import *
# We want to import every format, also imports module "format"
from formats import *

def pack(sprites, settings):
    """
    Packs the sprites.

    Saves the result image and the coordinates file according to settings

    :param list sprites: list of sprite objects
    :param settings: settings object
    """
    # Get an instance of the algorithm and format named in the settings
    a = algorithm.get_algorithm(settings.algorithm)
    f = format.get_format(settings.format)

    # Check if the chosen algorithm and output format is compatible with
    # the specified settings
    #algorithm.check_compatibility(a, settings)
    #format.check_compatibility(f, settings)

    # Run the algorithm
    a.pack(sprites, settings)
    # Generate the coordinates file
    print(f.generate(sprites, settings))
