echo "Building gitBack.exe ..."
pyinstaller --onefile gitBack.py #Build with PyInstaller
mv dist/gitBack.exe ./ #Move the .exe to the current directory
rmdir dist #Delete the dist directory
rmdir -recurse -Force build #Recursively delete the contents of the build directory.
#rmdir build #Delete the build directory
del gitBack.spec #Delete the .spec file
echo Done

echo "Building install.exe ..."
pyinstaller --onefile install.py #Build with PyInstaller
mv dist/install.exe ./ #move the .exe to the current directory
rmdir dist #Delete the dist directory
rmdir -recurse -Force build #Recursively delete the contents of the build directory.
#rmdir build #Delete the build directory
del install.spec #Delete the .spec file
echo Done