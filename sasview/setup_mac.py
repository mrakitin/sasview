"""
This is a setup.py script partly generated by py2applet

Usage:
    python setup.py py2app


NOTES:
   12/01/2011: When seeing an error related to pytz.zoneinfo not being found, change the following line in py2app/recipes/matplotlib.py
               mf.import_hook('pytz.tzinfo', m, ['UTC'])
   12/05/2011: Needs macholib >= 1.4.3 and py2app >= 0.6.4 to create a 64-bit app
"""
from setuptools import setup
import periodictable.xsf
import sas.sascalc.dataloader.readers
import os
import string
import local_config
import pytz
import sys
import platform
#Extending recursion limit
sys.setrecursionlimit(10000)

from distutils.util import get_platform
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
platform = '%s-%s'%(get_platform(),sys.version[:3])
build_path = os.path.join(root, 'build','lib.'+platform)
sys.path.insert(0, build_path)
print "BUILDING PATH INSIDE", build_path
ICON = local_config.SetupIconFile_mac
EXTENSIONS_LIST = []
DATA_FILES = []
RESOURCES_FILES = []

#Periodictable data file
DATA_FILES = periodictable.data_files()
#invariant and calculator help doc
import sas.sasgui.perspectives.fitting as fitting
DATA_FILES += fitting.data_files()
import sas.sasgui.perspectives.calculator as calculator
DATA_FILES += calculator.data_files()
import sas.sasgui.perspectives.invariant as invariant
DATA_FILES += invariant.data_files()
import sasmodels as models
DATA_FILES += models.data_files()
import sas.sasgui.guiframe as guiframe
DATA_FILES += guiframe.data_files()

#CANSAxml reader data files
RESOURCES_FILES.append(os.path.join(sas.sascalc.dataloader.readers.get_data_path(),'defaults.json'))

DATA_FILES.append('logging.ini')

# Locate libxml2 library
lib_locs = ['/usr/local/lib', '/usr/lib']
libxml_path = None
for item in lib_locs:
    libxml_path_test = '%s/libxml2.2.dylib' % item
    if os.path.isfile(libxml_path_test):
        libxml_path = libxml_path_test
if libxml_path == None:
    raise RuntimeError, "Could not find libxml2 on the system"

APP = ['sasview.py']
DATA_FILES += ['images','test','media', 'custom_config.py', 'local_config.py']
if os.path.isfile("BUILD_NUMBER"):
    DATA_FILES.append("BUILD_NUMBER")

# See if the documentation has been built, and if so include it.
doc_path = os.path.join(build_path, "doc")
print doc_path
if os.path.exists(doc_path):
    for dirpath, dirnames, filenames in os.walk(doc_path):
        for filename in filenames:
            sub_dir = os.path.join("doc", os.path.relpath(dirpath, doc_path))
            DATA_FILES.append((sub_dir, [os.path.join(dirpath, filename)]))
else:
    raise Exception("You must first build the documentation before creating an installer.")

# locate file extensions
def find_extension():
    """
    Describe the extensions that can be read by the current application
    """
    try:
        list = []
        EXCEPTION_LIST = ['*', '.', '']
        from sas.sascalc.dataloader.loader import Loader
        wild_cards = Loader().get_wildcards()
        for item in wild_cards:
            #['All (*.*)|*.*']
            file_type, ext = string.split(item, "|*.", 1)
            if ext.strip() not in EXCEPTION_LIST and ext.strip() not in list:
                list.append(ext)
    except:
        pass
    try:
        file_type, ext = string.split(local_config.APPLICATION_WLIST, "|*.", 1)
        if ext.strip() not in EXCEPTION_LIST and ext.strip() not in list:
            list.append(ext)
    except:
        pass
    try:
        for item in local_config.PLUGINS_WLIST:
            file_type, ext = string.split(item, "|*.", 1)
            if ext.strip() not in EXCEPTION_LIST and ext.strip() not in list:
                list.append(ext)
    except:
        pass

    return list

EXTENSIONS_LIST = find_extension()


plist = dict(CFBundleDocumentTypes=[dict(CFBundleTypeExtensions=EXTENSIONS_LIST,
                                         CFBundleTypeIconFile=ICON,
                                   CFBundleTypeName="sasview file",
                                   CFBundleTypeRole="Shell" )],)

#Get version - NB nasty hack. Need to find correct way to give path to installed sasview (AJJ)
#h5py has been added to packages. It requires hdf5 to be installed separetly
#
import __init__ as sasviewver

VERSION = sasviewver.__version__
APPNAME = "SasView "+VERSION
DMGNAME = "SasView-"+VERSION+"-MacOSX"

APP = ['sasview.py']
DATA_FILES += ['images','test','media']

EXCLUDES = ['PyQt4', 'sip', 'QtGui']

OPTIONS = {'argv_emulation': True,
           'packages': ['lxml','numpy', 'scipy', 'pytz', 'encodings',
                        'encodings','matplotlib', 'periodictable',
                        'reportlab','sasmodels',"pyopencl", "h5py"
                        ],
           'iconfile': ICON,
           'frameworks':[libxml_path],
           'resources': RESOURCES_FILES,
           'plist':plist,
           'excludes' : EXCLUDES,
           }
setup(
    name=APPNAME,
    app=APP,
    data_files=DATA_FILES,
    include_package_data= True,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

#Build dmg
DMG="dist/%s.dmg"%DMGNAME
if os.path.exists(DMG): os.unlink(DMG)
os.system('cd dist && ../../build_tools/dmgpack.sh "%s" "%s.app"'%(DMGNAME,APPNAME))
os.system('chmod a+r "%s"'%DMG)
