import os, shutil

#check if %APPDATA%\gitBackConfig exists
#if not, create it and repositories.cfg
configDir = os.path.expandvars('%APPDATA%\\gitBackConfig')
installDir = os.path.expandvars('%LOCALAPPDATA%\\Programs\\gitBack')
downloadDir = os.path.dirname(os.path.realpath(__file__))
configFiles = ['usage.txt']
installFiles = ['LICENSE', 'README.md']

if not os.path.exists(configDir):
    print('Creating config directory.')
    os.mkdir(configDir)

#Check if %LOCALAPPDATA%\Programs\gitBack exists
#if so, delete it
if os.path.exists(installDir):
    shutil.rmtree(installDir)

#Create installDir
os.mkdir(installDir)

#clone the whole repository to installDir
for file in configFiles:
    fullFile = os.path.join(configDir, file)
    print(shutil.copyfile(fullFile, configDir))

for file in installFiles:
    fullFile = os.path.join(installDir, file)
    print(shutil.copyfile(fullFile, installDir))