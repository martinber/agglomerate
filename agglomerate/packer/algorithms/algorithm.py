import simple

class Algorithm:
    """
    Base class for all algorithms

    Decides sprites placement and sheet size if isn't specified

    **Necessary class variables**
    supports_rotation
        whether the algorithm supports rotation of sprites
    supports_sheet_size_selection
        wether the algorithm supports deciding the size of the sheet
    """
    supports_rotation = False
    supports_sheet_size_selection = False

    def pack(self, sprites, settings):
        """
        Sets sprites positions accordingly

        :param list sprites: list of sprite objects
        :param settings: settings object
        """

class UnknownAlgorithmException(Exception):
    """
    Raised when trying to get an unknown algorithm
    """
    def __init__(self, algorithm_name):
        self.algorithm_name = algorithm_name
    def __repr__(self):
        return "Unknown algorithm named " + algorithm_name

# Dictionary of registered algorithms
algorithms = {
    "simple": simple.Simple
}

def get_algorithm(name):
    """
    Returns chosen algorithm

    :param str name: algorithm name
    :return: instance or the selected algorithm
    """
    try:
        algorithm = algorithms[name]
    except KeyError:
        raise UnknownAlgorithmException(name)

    return algorithm
