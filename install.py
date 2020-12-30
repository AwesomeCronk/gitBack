import os, shutil, sys

configDir = os.path.expandvars('%APPDATA%\\gitBackConfig')
installDir = os.path.expandvars('%LOCALAPPDATA%\\Programs\\gitBack')
downloadDir = os.path.dirname(os.path.realpath(__file__))
configFiles = ['usage.txt']
installFiles = ['LICENSE', 'README.md', 'gitBack.exe']

_version = '1.0.1'

def version():
    print('Using gitBack installer version {}.'.format(_version))

if len(sys.argv) > 1:
    if sys.argv[1] == 'version':
        version()
else:
    #If not, create it
    if not os.path.exists(configDir):
        print('Creating config directory.')
        os.mkdir(configDir)

    #Check if %LOCALAPPDATA%\Programs\gitBack exists
    #if so, delete it
    if os.path.exists(installDir):
        print('Removing install directory.')
        shutil.rmtree(installDir)

    #Create installDir
    print('Creating install directory.')
    os.mkdir(installDir)

    #copy the necessary files to installDir
    for file in configFiles:
        print('Copying {} to {} ... '.format(file, configDir), end = '')
        shutil.copy(file, configDir)
        print('Done.')

    for file in installFiles:
        print('Copying {} to {} ... '.format(file, installDir), end = '')
        shutil.copy(file, installDir)
        print('Done.')