
import keyword
import re
import sys
import os

from os.path import dirname, join, split, splitext

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import gv

def isidentifier(s):  # to make this work with Python 2.7.
    if s in keyword.kwlist:
        return False
    return re.match(r'^[a-z_][a-z0-9_]*$', s, re.I) is not None

basedir = dirname(__file__)
os_name = os.name

__all__ = []

module = gv.sd['controlName']

# For Debugging
#controlPlugin = __import__(__name__+'.'+module)
#__all__ = module

try:
    controlPlugin = __import__(__name__+'.'+module)
    __all__ = module
except Exception as e:
    print 'Ignoring exception while loading the {} plug-in.'.format(module)
    print e  # Provide feedback for plugin development
