import os
import fnmatch
import PIL


def get_matching_paths(path):
    """
    Returns a list of paths that were matched by the given path. e.g. *.png

    Supports unix style wildcards, e.g. file_*, sprites/*.png or ./f.png

    Adds ./ at the beggining of the path if given path doesn't have
    directory

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


class Color:
    """
    Represents a RGBA color

    Has "r", "g", "b", and "a" fields.
    """
    def __init__(self, r=255, g=255, b=255, a=255):
        """
        Creates a color instance from RGBA values.

        Values are 255 by default, and should be integers between 0 and 255
        """
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    @classmethod
    def from_hex(cls, hex_value):
        """
        Creates a color instance from a hex RGB or RGBA string value.

        For example #AABBCC, #AABBCCDD, AABBCC or AABBCCDD
        """
        if hex_value[0] == "#":
            # means that the code starts with #, so we delete it
            hex_value = hex_value[1:]

        # we will put the values here
        values_list = []

        # string must be 6 or 8 chars long
        if len(hex_value) == 6 or len(hex_value) == 8:
            # take two letters at a time until we finish the string, once per
            # value
            while len(hex_value) > 0:
                # get first value
                v = hex_value[:2]

                # convert hex value to int and append to the list
                values_list.append(int(v, 16))

                # remove processed value from the code string
                hex_value = hex_value[2:]

            # unpack the list
            if len(values_list) == 3:
                r, g, b = values_list
                return Color(r, g, b)
            else:
                r, g, b, a = values_list
                return Color(r, g, b, a)


    def to_hex(self):
        """
        Returns a hex value RGBA string in lowercase, like #aabbccdd
        """
        values = [self.r, self.g, self.b, self.a]
        # we will concatenate the strings present in this list later
        string_list = ["#"]

        # convert values to hex one by one and add them to de list
        for v in self.values:
            # slice the string because hex() returns string starting with "0x"
            hex_value = hex(v)[2:]
            # if the value is less than 16, the hex_value has only one digit,
            # so we need to make sure that hex_value is 2 digits long adding a
            # 0 at the beggining
            if len(hex_value) == 1:
                hex_value = "0" + hex_value

            # add to string_list
            string_list.append(hex_value)

        return "".join(string_list)


    def to_tuple(self):
        """
        Returns a tuple (r, g, b, a) with the values in decimal format
        (from 0 to 255)
        """
        return (self.r, self.g, self.b, self.a)


    def __repr__(self):
        return "({}, {}, {}, {})".format(self.r, self.g, self.b, self.a)
