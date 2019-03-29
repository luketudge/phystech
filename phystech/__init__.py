"""
This is the init file for the phystech module.
In here we can put any commands that should be run when phystech is imported.
Variables defined here will be available under the module's namespace.
"""

from glob import glob
from os import path

# Path to the example data file.
# Might be useful for tests.
EXAMPLEFILES = glob(path.join(path.dirname(path.abspath(__file__)), 'data', '*.h5'))

# Example datasets in the files.
EXAMPLEDATA = ['eVEnerg:io1200000cff','A2980:23303chan1']

