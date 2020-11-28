if ("gitBack" -in $args)
{
    Write-Output "Building gitBack.exe..."
    Remove-Item gitBack.exe -ErrorAction Ignore #Delete the original .exe if it exists
    pyinstaller --onefile gitBack.py #Build with PyInstaller
    Move-Item dist/gitBack.exe ./ #Move the .exe to the current directory
    Remove-Item -Recurse -Force dist #Delete the dist directory
    Remove-Item -Recurse -Force build #Recursively delete the contents of the build directory
    #Remove-Item build #Delete the build directory
    Remove-Item gitBack.spec #Delete the .spec file
    Write-Output "Done building gitBack.exe."
}

if ("install" -in $args)
{
    Write-Output "Building install.exe..."
    Remove-Item install.exe -ErrorAction Ignore
    pyinstaller --onefile install.py #Build with PyInstaller
    Move-Item dist/install.exe ./ #move the .exe to the current directory
    Remove-Item -Recurse -Force dist #Delete the dist directory
    Remove-Item -Recurse -Force build #Recursively delete the contents of the build directory
    #Remove-Item build #Delete the build directory
    Remove-Item install.spec #Delete the .spec file
    Write-Output "Done building install.exe."
}