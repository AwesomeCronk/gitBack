This is meant to be a simple backup systyem for Windows that loops over all the directories listed in its config file and automatically runs git add, git commit, and git push to update remote repositories to match each local one.

WARNING! Multiple branches may break this system!
WARNING! There are no chacks for validity on ANYTHING! gitBack kinda relies on you to make sure you give it valid paths for everything.