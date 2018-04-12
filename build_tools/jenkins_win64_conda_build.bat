:: EXPORT CONDA PATH
set PATH=%PATH%;C:\Users\sasview\Miniconda2\Scripts
set PATH=%PATH%;C:\Users\sasview\Miniconda2

set PYTHON=python.exe
set EASY_INSTALL=easy_install.exe
set PYLINT= pylint.exe
set PYINSTALLER=pyinstaller.exe
set INNO=C:\"Program Files (x86)"\"Inno Setup 5"\ISCC.exe
set GIT_SED=C:\"Program Files"\Git\bin\sed.exe
set SAS_COMPILER=tinycc


:: LIST ALL CONDA ENVS
conda env list

:: CONDA MAKE NEW ENV
cd  %WORKSPACE%
conda env create --force -f %WORKSPACE%\sasview\build_tools\conda\ymls\sasview-env-build_win.yml

:: SETUP CONDA ENV (CONDA IS ALREADY SYSTEM PATH)
call activate sasview

:: REMOVE INSTALLATION ################################################
pip uninstall -y sasview
pip uninstall -y sasmodels
pip uninstall -y tinycc

:: TINYCC build ####################################################
cd %WORKSPACE%
cd tinycc
%PYTHON% setup.py build install

:: SASMODELS build ####################################################
cd %WORKSPACE%
cd sasmodels
%PYTHON% setup.py build

:: SASMODELS doc ######################################################
cd doc
make html

:: SASMODELS build egg ################################################
cd %WORKSPACE%
cd sasmodels
%PYTHON% setup.py install


:: NOW BUILD SASVIEW

:: SASVIEW build egg ################################################
cd %WORKSPACE%
cd sasview
%PYTHON% setup.py build docs install


:: SASVIEW utest ######################################################
cd %WORKSPACE%\sasview\test
%PYTHON% utest_sasview.py


:: SASVIEW INSTALL EGG ################################################
cd %WORKSPACE%
cd sasview
cd dist
echo F | xcopy sasview-*.egg sasview.egg /Y
%EASY_INSTALL% -d %WORKSPACE%\sasview\sasview-install sasview.egg

:: SASVIEW INSTALLER ##################################################
cd %WORKSPACE%
cd sasview
cd installers

:: USING PYINSTALLER
:: %PYINSTALLER% sasview.spec

::# :: USING PY2EXE
%PYTHON% setup_exe.py py2exe

:: READY FOR INNO
%PYTHON% installer_generator.py
%INNO% installer.iss
cd Output
xcopy setupSasView.exe %WORKSPACE%\sasview\dist

:: :: SASVIEW PYLINT #####################################################
:: cd %WORKSPACE%\sasview
:: %PYLINT% --rcfile "build_tools/pylint.rc" -f parseable sasview-install/sasview.egg/sas sasview > test/sasview.txt

:: GO BACK ############################################################
cd %WORKSPACE%


:: REMOVE INSTALLATION ################################################
::pip uninstall -y sasview
::pip uninstall -y sasmodels
::pip uninstall -y tinycc