import abc
import importlib


class Algorithm:
    """
    Base class for all algorithms

    Decides items placement and sheet size if isn't specified. Has a
    "supports" dictionary

    **Supports dictionary**
    - rotation: whether the algorithm supports rotation of sprites
    - cropping: True if the algorithm supports sprite cropping
    - padding: True if the algorithm supports sprite padding

    - auto_size: whether the algorithm supports deciding the size of the
                       sheet
    - auto_square_size: if the algorithm supports defining a squared
                              sheet, ignored if auto_size is False
    - auto_power_of_two_size: if the algorithm supports defining a
                                    power-of-two sized sheet, ignored if
                                    auto_size is False
    """
    supports = {
                "rotation": False,
                "cropping": False,
                "padding": False,

                "auto_size": False,
                "auto_square_size": False,
                "auto_power_of_two_size": False
               }

    @abc.abstractmethod
    def pack(self, sprites, settings):
        """
        Sets items positions accordingly, also modifies settings if neccesary
        (for example setting the size). Can accept a Settings instance or a
        SheetSettings instance.

        :param list sprites: list of sprite objects
        :param settings: settings object
        """


# -----------------------------------------------------------------------------
# Retrieval of algorithms
# -----------------------------------------------------------------------------


class UnknownAlgorithmException(Exception):
    """
    Raised when trying to get an unknown algorithm
    """
    def __init__(self, algorithm_name):
        self.algorithm_name = algorithm_name

    def __repr__(self):
        return "Unknown algorithm named " + algorithm_name


def get_algorithm(name):
    """
    Returns an instance of the chosen algorithm.

    :param str name: algorithm name
    :return: instance of the selected algorithm
    """
    module = importlib.import_module("agglomerate.main.algorithms." + name)
    return module.algorithm_class()


# -----------------------------------------------------------------------------
# Compatibility checking
# -----------------------------------------------------------------------------


class IncompatibilityReason:
    """
    Enumeration on causes of incompatibilites between algorithms and settings

    - AUTO_SIZE_REQUIRED: settings specify an automatic sheet size but
      algorithm doesn't support size resolving
    """
    (AUTO_SHEET_SIZE_REQUIRED,
     AUTO_SQUARE_SHEET_SIZE_REQUIRED,
     AUTO_POWER_OF_TWO_SHEET_SIZE_REQUIRED) = range(3)


class WarningReason:
    """
    Enumeration on causes of incompatibilites warnings between algorithms and
    settings

    - ROTATION_REQUIRED: settings allow rotation of sprites but algorithm does
      not support rotation
    """
    (ROTATION_ALLOWED,
    CROPPING_ALLOWED) = range(2)


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

    w, h = settings.size.to_tuple()
    requires_size_selection = (w == "auto" or h == "auto")

    if requires_size_selection and not \
            alg.supports["auto_size"]:

        compatible = False
        incompatibilities.append(IncompatibilityReason.AUTO_SHEET_SIZE_REQUIRED)

        if settings.require["auto_square_size"] and not \
                alg.supports["auto_square_size"]:
            compatible = False
            incompatibilities.append(IncompatibilityReason.
                    AUTO_SQUARE_SHEET_SIZE_REQUIRED)

        if settings.require["auto_power_of_two_size"] and not \
                alg.supports["auto_power_of_two_size"]:
            compatible = False
            incompatibilities.append(IncompatibilityReason.
                    AUTO_POWER_OF_TWO_SHEET_SIZE_REQUIRED)

    if settings.allow["rotation"] and not alg.supports["rotation"]:
        warnings.append(WarningReason.ROTATION_ALLOWED)

    if settings.allow["cropping"] and not alg.supports["cropping"]:
        warnings.append(WarningReason.CROPPING_ALLOWED)

    # padding will be false or a number
    if settings.require["padding"] != False and not alg.supports["padding"]:
        incompatibilities.append(IncompatibilityReason.PADDING_REQUIRED)

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
