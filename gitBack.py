import sys, os
import subprocess as sp

def _parseRepos():   #Read repositories.cfg and return a list of tuples containing the local path and remote location
    repos = {}
    with open('{}/gitBackConfig/repositories.cfg'.format(os.environ['USERPROFILE']), 'r') as repoFile:
        for line in repoFile.readlines():
            repos.update({line.split(' ||| ')[0]: line.split(' ||| ')[1]})
    return repos

def _saveRepos(repos):
    with open('{}/gitBackConfig/repositories.cfg'.format(os.environ['USERPROFILE']), 'w') as repoFile:
        for localRepo in list(repos.keys()) #write the key, a ' ||| ', and the value, then a newline

def usage():     #print out usage
    with open('usage.txt', 'r') as file:
        print(file.read())

def list():     #print out the list
    repos = _parseRepos()

def include(newRepo, newRepoBackup = None):  #add a new directory to the list
    repos = _parseRepos()
    repos.update({os.path.expandvars(newRepo): os.path.expandvars(newRepoBackup)})

def exclude(excRepo):  #remove a directory from the list
    pass

def backup():   #Back up all of the listed directories
    p = sp.Popen('git status', stdout = sp.PIPE, stderr = sp.PIPE)
    gitOut, gitErr = sp.communicate()
    
if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '--help':
            usage()
        elif sys.argv[1] == '--list':
            list()
        elif sys.argv[1] == '--include':
            if len(sys.argv) == 3:
                include(sys.argv[2])
            elif len(sys.argv) == 4:
                include(sys.argv[2], sys.argv[3])
        elif sys.argv[1] == '--exclude':
            exclude(sys.argv[1])
    else:
        usage()