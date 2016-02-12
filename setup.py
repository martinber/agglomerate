from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), "r", "utf-8") as f:
    _long_description = f.read()

# Get the version from VERSION file
with open(path.join(here, 'VERSION'), "r", "utf-8") as f:
    _version = f.read()

setup(
    name = 'sample',
    version = _version,

    description = 'A simple sprite packer',
    long_description = _long_description,

    #url='https://github.com/martinber/agglomerate',
    author = 'Martin Bernardi',
    author_email = 'martinbernardi@openmailbox.org',
    license = 'MIT',

    classifiers = [
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Graphics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],

    keywords = 'development sprite image game',

    packages = find_packages(),
    install_requires = ['pillow'],

    entry_points = {
        'console_scripts': [
            'agglomerate=agglomerate.scripts.agglomerate:main',
        ],
    },

	# Set files in MANIFEST.in to be installed (required at runtime)
	include_package_data=True

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    #extras_require={
    #    'dev': ['check-manifest'],
    #    'test': ['coverage'],
    #},

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    #package_data={
    #    'agglomerate': ['package_data.dat'],
    #},

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    #data_files=[('my_data', ['data/data_file'])],
)
