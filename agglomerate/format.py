import abc
import importlib


class Format:
    """
    Base class for all coordinates file output formats.

    Creates a string defining sprites placement, has a "supports" dictionary
    and a suggested extension.

    **Supports dictionary**
    - rotation: whether the format supports rotation of sprites
    - cropping: True if the format supports sprite cropping
    """
    supports = {
                "rotation": False,
                "cropping": False,
               }
    suggested_extension = "txt"

    @abc.abstractmethod
    def generate(self, sprites, settings):
        """
        Creates a string defining sprites placement

        :param list sprites: list of Sprite objects
        :param settings: SheetSettings object
        :return: string to be saved to a file
        """


# -----------------------------------------------------------------------------
# Registration of formats
# -----------------------------------------------------------------------------


class UnknownFormatException(Exception):
    """
    Raised when trying to get an unknown format
    """
    def __init__(self, format_name):
        self.format_name = format_name

    def __repr__(self):
        return "Unknown format named " + format_name


def get_format(name):
    """
    Returns an instance of the chosen format.

    :param str name: format name
    :return: instance of the selected format
    """
    module = importlib.import_module("agglomerate.formats." + name)
    return module.format_class()


# -----------------------------------------------------------------------------
# Compatibility Checking
# -----------------------------------------------------------------------------


class IncompatibilityReason:
    """
    Enumeration on causes of incompatibilites between formats and settings

    - ROTATION_REQUIRED: settings allow rotation of sprites but format does
      not define rotated sprites
    """
    (ROTATION_ALLOWED,
    CROPPING_ALLOWED) = range(2)


class WarningReason:
    """
    Enumeration on causes of incompatibilites warnings between formats and
    settings
    """
    pass


def check_compatibility(format, settings):
    """
    Check if the given format is compatible with the given settings

    This is because some formats don't support rotating sprites

    :param format: format instance
    :param settings: settings object
    :return: tuple containing a boolean, a list of incompatibilities reasons
    and a list of warnings reasons
    """
    compatible = True
    incompatibilities = [None]
    warnings = [None]

    if settings.allow["rotation"] and not format.supports["rotation"]:
        compatible = False
        incompatibilities.append(IncompatibilityReason.ROTATION_ALLOWED)

    if settings.allow["cropping"] and not format.supports["cropping"]:
        compatible = False
        incompatibilities.append(IncompatibilityReason.CROPPING_ALLOWED)

    return (compatible, incompatibilities, warnings)
