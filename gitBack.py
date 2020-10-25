import sys, os
import subprocess as sp

#Notes for next time:
# os.path.expandvars is not working.

#Local and remote repos are separated in repositories.cfg by ' ||| '. This makes it easier to read manually and debug issues with the config file.
def _parseRepos():   #Read repositories.cfg and return a dictionary containing the local and remote repositories. Local repos are keys.
    repos = {}
    with open('{}/gitBackConfig/repositories.cfg'.format(os.environ['APPDATA']), 'r') as repoFile:
        for line in repoFile.readlines():
            repos.update({line.split(' ||| ')[0]: line.split(' ||| ')[1]})
    return repos

def _saveRepos(repos):  #Write the 
    with open('{}/gitBackConfig/repositories.cfg'.format(os.environ['APPDATA']), 'w') as repoFile:
        for localRepo in list(repos.keys()):
            repoFile.writelines('{} ||| {}'.format(localRepo, repos[localRepo]))

def usage():     #print out usage
    with open('usage.txt', 'r') as file:
        print(file.read())

def listRepos():     #print out the list
    print('Repositories to be watched:\n')
    repos = _parseRepos()
    print('debug repos={}'.format(repos))
    for localRepo in repos.keys():
        print(localRepo)
        print(repos[localRepo], end = '\n\n')

def includeRepo(newRepo, newRepoBackup):  #add a new directory to the list
    repos = _parseRepos()
    repos.update({os.path.expandvars(newRepo): os.path.expandvars(newRepoBackup)})
    _saveRepos(repos)

def excludeRepo(excRepo):  #remove a directory from the list
    pass

def backup():   #Back up all of the listed directories
    p = sp.Popen('git status', stdout = sp.PIPE, stderr = sp.PIPE)
    gitOut, gitErr = sp.communicate()
    
if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'help':
            usage()
        elif sys.argv[1] == 'list':
            listRepos()
        elif sys.argv[1] == 'include':
            includeRepo(sys.argv[2], sys.argv[3])
        elif sys.argv[1] == 'exclude':
            excludeRepo(sys.argv[2])
    else:
        usage()