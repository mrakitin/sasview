"""
 Installation script for SANS models

  - To compile and install:
      python setup.py install
  - To create distribution:
      python setup.py bdist_wininst

"""
import sys, os
from distutils.core import setup, Extension
from distutils import util
from distutils import sysconfig

def get_c_files(path):
    """
        Utility function to return all files 
        to be compiled in a directory
    """
    clist = []
    for file in os.listdir(path):
        if file.endswith(".cc") or file.endswith(".c"):
            clist.append("%s/%s" % (path, file))
    return clist

# The temp directory that the compiled files will be put in
tempdir = "build/temp."+util.get_platform()+'-'+sysconfig.get_python_version()
if os.name=='nt':
    tempdir += "/Release"

# List of sub modules
mod_list = ["iqPy", "geoshapespy", "pointsmodelpy", "analmodelpy"]

# Define package directors, will be extended below
pck_dirs = {"sansModeling":"."}

# List of modules to install, will be extende below
pck_list = ["sansModeling"]

# List of python extensions, will be extended below
exts = []

# List of include dirs, will be extended below
incl_dirs = ["iqPy/libiqPy/tnt"]

# List of files to compile, per module, will be extended below
file_list = {}

# List of dependencies
deps = {}
deps["iqPy"] = []
deps["geoshapespy"] = ["iqPy"]
deps["analmodelpy"] = ["iqPy", "geoshapespy"]
deps["pointsmodelpy"] = ["iqPy", "geoshapespy"]

# List of extra objects to link with, per module, will be extended below 
libs = {}

for module in mod_list:
    pck_dirs["sansModeling.%s" % module] = "%s/%s" % (module, module)
    pck_list.append("sansModeling.%s" % module)

    src_m = "%s/%smodule" % (module, module)
    src_l = "%s/lib%s" % (module, module)

    files = get_c_files(src_m)
    list_lib = get_c_files(src_l)

    libs[module] = []    
    for dep in deps[module]:
        
        for f in get_c_files("%s/lib%s" % (dep, dep)):
            index = f.rindex('.')
            if os.name=='nt':
                fo = f[:index]+'.obj'
            else:
                fo = f[:index]+'.o'
            libs[module].append("%s/%s" %(tempdir,fo))
        
    files.extend(list_lib)
    file_list[module] = files
    
    incl_dirs.append(src_m)
    incl_dirs.append(src_l)
    
for module in mod_list:
    exts.append( Extension("sansModeling.%s.%s" % (module, module),
        sources = file_list[module],
        extra_objects=libs[module],
        include_dirs=incl_dirs) )

setup(
    name="realspacesimulation",
    version = "0.2",
    description = "Python module for SANS simulation",
    author = "University of Tennessee",
    url = "http://danse.us/trac/sans",
    
    package_dir = pck_dirs,
    packages    = pck_list,
    
    ext_modules = exts)


        