This is meant to be a simple backup systyem for Windows that loops over all the directories listed in its config file and automatically runs git add, git commit, and git push to update remote repositories to match each local one.

A few warnings: Multiple branches may break this system! There are no checks for validity on ANYTHING! gitBack kinda relies on you to make sure you give it valid paths for everything. Multiple instances of the same local repo will break the config file! This program was written to work on my system, with no regards to how other people have their systems set up. It may break things on your system.

gitBack version: 1.3.0
installer version: 1.0.1

### Installation instructions (non git users):
1. Make sure you have [Git](https://git-scm.com) installed and on your path.
2. Click the green button that says 'Code'.
3. Navigate to the zip folder that downloaded and unzip its contents to another folder.
4. Open that folder and run `install.exe`.
5. Add `%USERPROFILE%\AppData\Local\Programs\gitBack` to your path.

### Installation instructions (git users):
1. Clone `https://github.com/AwesomeCronk/gitBack` to any folder on your computer.
2. Navigate to the clones repository and execute `install.exe`.
3. Add `%USERPROFILE%\AppData\Local\Programs\gitBack` to your path.

### Instructions for building from source:
1. Modify `install.py` and/or `gitBack.py` as desired.
2. Execute `build.ps1` with the arguments `gitBack` and/or `install` to build the desired script.
3. Execute `install.exe`.
3. Make sure `%USERPROFILE%\AppData\Local\Programs\gitBack` is on your path.

### Uninstallation/removal instructions:
1. Delete `%APPDATA%\gitBackConfig` and its contents.
2. Delete `%LOCALAPPDATA\Programs\gitBack` and its contents.

gitBack is licensed under the MIT license with no warranty of any kind.