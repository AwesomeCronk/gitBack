import sys, os, datetime, ctypes
import subprocess as sp

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

today, now = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S").split()
_version = '1.5.1'
_termWidth = os.get_terminal_size()[0]
_driveLetters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
                 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                 'Y', 'Z']

#Local and remote repos are separated in repositories.cfg by ' ||| '. This makes it easier to read manually and debug issues with the config file.
def _loadRepos():   #Read repositories.cfg and return a dictionary containing the local and remote repositories. Local repos are keys.
    repos = {}
    with open('{}/gitBackConfig/repositories.cfg'.format(os.environ['APPDATA']), 'r') as repoFile:
        for line in repoFile.readlines():
            #print(line.__repr__(), end = '\n\n')
            repos.update({line[0:-1].split(' ||| ')[0]: line[0:-1].split(' ||| ')[1]})  #Use line[0:-1] to pull the \n off the end of line.
    return repos

def _saveRepos(repos):  #Write to repositories.cfg to save the repos dictionary.
    with open('{}/gitBackConfig/repositories.cfg'.format(os.environ['APPDATA']), 'w') as repoFile:
        for localRepo in list(repos.keys()):
            repoFile.write('{} ||| {}\n'.format(localRepo, repos[localRepo]))

def _parsePath(pathIn):
    #This should do the following:
    #|-Replace all instances of `/` with `\\`
    #|-Check if given path is a valid directory
    #| `-If it is not, cancel the operation and inform the user
    #`-Identify if the path is relative or absolute
    #  |-If it is relative, check for the specified path in the working directory
    #  | |-If found, return full path
    #  | `-If not found, ask user if they want to continue anyway
    #  `-If path is absolute, check if it exists
    #    |-If it exists, return it
    #    `-If it does not exist, ask the user if they want to continue anyway.

    #Return this tuple: (bool isValid, str result)

    #Environment variables should be parsed by the shell.
    #Replace all instances of `/` with `\\`
    pathOut = pathIn.replace('/', '\\')

    isAbsolute = os.path.isabs(pathOut)
    if not isAbsolute:
        pathOut = os.getcwd() + '\\' + pathOut
    pathOut = pathOut[0].upper() + pathOut[1:]
#    exists = os.path.exists(pathOut)
#    if not exists:
#        return False, 'target does not exist'
    isFile = os.path.isfile(pathOut)
    if isFile:
        return False, 'target is file'
    isDirectory = os.path.isdir(pathOut)
    if not isDirectory:
        return False, 'target is not directory'
    
    return True, pathOut

def _git(command):  #Wrapper for subprocess to facilitate one-line git commands.
    git = sp.Popen('git {}'.format(command), stdout = sp.PIPE, stderr = sp.PIPE)
    return git.communicate()

def usage():     #print out usage
    with open('{}/gitBack/usage.txt'.format(os.environ['LOCALAPPDATA'], 'r')) as file:
        print(file.read())

def listRepos():     #print out the list
    print('Repository watch list:', end = '\n\n')
    repos = _loadRepos()
    #print('debug repos={}'.format(repos))
    for localRepo in repos.keys():
        print(localRepo)
        print(repos[localRepo], end = '\n\n')

def includeRepo(newRepo, remote):  #add a new directory to the list
    isValid, result = _parsePath(newRepo)
    if not isValid:
        print('Failed to add local repository to watch list. Reason: {}'.format(result))
        return
    repos = _loadRepos()
    repos.update({result: remote})
    print('Local repository added to watch list.')
    _saveRepos(repos)

def excludeRepo(excRepo):  #remove a directory from the list
    repos = _loadRepos()
    isValid, result = _parsePath(excRepo)
    if not isValid:
        print('Failed to remove repository from watch list. Reason: {}'.format(result))
    try:
        del(repos[result])
        _saveRepos(repos)
        print('Local repository removed from watch list.')
    except KeyError:
        print('Local repository not found in watch list.')

def backup():   #Back up all of the listed directories
    repos = _loadRepos()
    for localRepo in repos.keys():
        remoteRepo = repos[localRepo]
        print('=' * _termWidth)
        print('Checking directory {}'.format(localRepo))
        os.chdir(localRepo)

        gitResults = _git('status')
        print(gitResults[0].decode('utf-8'))
        print(gitResults[1].decode('utf-8'))
        if not b'nothing to commit, working tree clean' in gitResults[0]:   #Check for uncommitted changes
            print('Changes needing committed. Committing now.')
            _git('add .')
            gitResults = _git('commit -m "gitBack autocommit on {} at {}"'.format(today, now))
            print(gitResults[0].decode('utf-8'))
            print(gitResults[1].decode('utf-8'))
        else:
            print('No changes needing committed.\n')
            
        #Check if local is ahead, behind, or diverged
        _git('fetch')
        mb = _git('merge-base master {}/master'.format(remoteRepo))[0]
        rpLocal = _git('rev-parse master')[0]
        rpRemote = _git('rev-parse {}/master'.format(remoteRepo))[0]

        print('merge-base:       {}\nrev-parse local:  {}\nrev-parse remote: {}'.format(mb[0:-1].decode('UTF-8'), rpLocal[0:-1].decode('UTF-8'), rpRemote[0:-1].decode('UTF-8')))

        if mb == rpLocal == rpRemote:
            status = 'up-to-date'
        elif mb == rpLocal != rpRemote:
            status = 'behind'
        elif mb == rpRemote != rpLocal:
            status = 'ahead'
        elif mb != rpRemote != rpLocal:
            status = 'diverged'
        else:
            status = 'unknown'

        if status == 'ahead':
            print('Local repository is ahead of remote. Pushing to remote.')   #Push the current state to the remote repository
            gitResults = _git('push {} master'.format(remoteRepo))
            print(gitResults[0].decode('utf-8'))
            print(gitResults[1].decode('utf-8'))
            print('\n')
        elif status == 'up-to-date':
            print('Local repository is up-to-date with remote.')
        elif status == 'behind':
            print('Local repository is behind remote. Consider using git pull to update your local.')
        elif status == 'diverged':
            print('Local repository and remote have diverged. gitBack cannot fix this.')
        else:
            print('Unable to determine status of remote repository.')
    
def version():
    print('Using gitBack version {}.'.format(_version))

if __name__ == '__main__':
    try:
        tempRepoFile = open('{}/gitBackConfig/repositories.cfg'.format(os.environ['APPDATA']), 'r')
        tempRepoFile.close()
    except OSError:
        print('%APPDATA%\\gitBackConfig\\repositories.cfg not found. Creating a blank one.')
        tempRepoFile = open('{}/gitBackConfig/repositories.cfg'.format(os.environ['APPDATA']), 'w')
        tempRepoFile.write('')
        tempRepoFile.close()

    if len(sys.argv) > 1:
        if sys.argv[1] == 'help':
            usage()
        elif sys.argv[1] == 'list':
            listRepos()
        elif sys.argv[1] == 'include':
            includeRepo(sys.argv[2], sys.argv[3])
        elif sys.argv[1] == 'exclude':
            excludeRepo(sys.argv[2])
        elif sys.argv[1] == 'backup':
            backup()
        elif sys.argv[1] == 'version':
            version()
        elif sys.argv[1] == 'checkpath':
            print(_parsePath(sys.argv[2]))
    else:
        usage()