import os
import fnmatch

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
