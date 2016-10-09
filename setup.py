# setup.py
import glob
import platform

if platform.system() == 'Darwin':
    from setuptools import setup
    print 'In mac env'
    APP = ['run.py']
    DATA_FILES = [("img", glob.glob("img\\*"))]
    OPTIONS = {'argv_emulation': True}

    setup(
        app=APP,
        data_files=DATA_FILES,
        options={'py2app': OPTIONS},
        setup_requires=['py2app'],
    )
else:
    from distutils.core import setup
    setup(windows=['run.py'],
          data_files = [("img", glob.glob("img\\*"))])
