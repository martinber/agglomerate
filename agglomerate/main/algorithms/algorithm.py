import abc

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

    @abc.abstractmethod
    def pack(self, sprites, settings):
        """
        Sets sprites positions accordingly, also modifies settings if neccesary

        :param list sprites: list of sprite objects
        :param settings: settings object
        """

# -----------------------------------------------------------------------------
# Registration of algorithms
# -----------------------------------------------------------------------------

class UnknownAlgorithmException(Exception):
    """
    Raised when trying to get an unknown algorithm
    """
    def __init__(self, algorithm_name):
        self.algorithm_name = algorithm_name
    def __repr__(self):
        return "Unknown algorithm named " + algorithm_name

# Dictionary of registered algorithms
algorithms = {}

def register_algorithm(name, algorithm):
    """
    Register an algorithm for get_algorithm function

    :param str name: the name
    :param class algorithm: the algorithm
    """
    algorithms[name] = algorithm

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

    return algorithm()

# -----------------------------------------------------------------------------
# Compatibility checking
# -----------------------------------------------------------------------------

class IncompatibilityReason:
    """
    Enumeration on causes of incompatibilites between algorithms and settings

    - AUTO_SIZE_REQUIRED: settings specify an automatic sheet size but
      algorithm doesn't support size resolving
    """
    AUTO_SIZE_REQUIRED = range(1)

class WarningReason:
    """
    Enumeration on causes of incompatibilites warnings between algorithms and
    settings

    - ROTATION_REQUIRED: settings allow rotation of sprites but algorithm does
      not support rotation
    """
    ROTATION_REQUIRED = range(1)

def check_compatibility(alg, settings):
    """
    Check if the given algorithm is compatible with the given settings

    This is because some algorithms don't support rotating sprites or defining
    neccesary sheet size

    :param alg: algorithm instance
    :param settings: settings object
    :return: tuple containing a boolean, a list of incompatibilities reasons
    and a list of warnings reasons
    """
    compatible = True
    incompatibilities = [None]
    warnings = [None]

    w, h = settings.output_sheet_size
    requires_sheet_size_selection = (w == "auto" or h == "auto")

    if requires_sheet_size_selection and not alg.supports_sheet_size_selection:
        compatible = False
        incompatibilities.append(IncompatibilityReason.AUTO_SIZE_REQUIRED)

    if settings.allow_rotation and not alg.supports_rotation:
        warnings.append(WarningReason.ROTATION_REQUIRED)

    return (compatible, incompatibilities, warnings)

# -----------------------------------------------------------------------------
# Exceptions for algorithm implementations
# -----------------------------------------------------------------------------

class AlgorithmOutOfSpaceException(Exception):
    """
    Thrown when the algorithm runs out of space in the sheet
    """
    pass

class AlgorithmUnexpectedException(Exception):
    """
    Raised when the algorithm has an unexpected error
    """
    pass
