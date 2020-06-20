# mysetup.py
from distutils.core import setup
import py2exe
import sys
import glob

# this allows to run it with a simple double click.
sys.argv.append('py2exe')

py2exe_options = {
    "includes": ["sip"],
    "dll_excludes": ["MSVCP90.dll", ],
    "compressed": 1,
    "optimize": 2,
    "ascii": 0,
    "bundle_files": 3,
}

setup(
    name='ShanbayHelper',
    version='1.0',
    windows=['human_recognition_tool_v3.py', ],
    zipfile=None,
    options={'py2exe': py2exe_options},
    data_files = [("imageformats", glob.glob("C:\Python27\Lib\site-packages\PyQt4\plugins\imageformats\*.dll"))]
)


