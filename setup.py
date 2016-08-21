# setup.py
from distutils.core import setup
import py2exe
import glob

setup(windows=['run.py'],
      data_files = [("img", glob.glob("img\\*"))])
#setup(console=['run.py'])
