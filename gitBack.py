import sys, os
import subprocess as sp

#Notes for next time:

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

def _git(command):  #Wrapper for subprocess to facilitate one-line git commands.
    git = sp.Popen('git {}'.format(command), stdout = sp.PIPE, stderr = sp.PIPE)
    return git.communicate()

def usage():     #print out usage
    with open('usage.txt', 'r') as file:
        print(file.read())

def listRepos():     #print out the list
    print('Repositories to be watched:', end = '\n\n')
    repos = _loadRepos()
    #print('debug repos={}'.format(repos))
    for localRepo in repos.keys():
        print(localRepo)
        print(repos[localRepo], end = '\n\n')

def includeRepo(newRepo, newRepoBackup):  #add a new directory to the list
    repos = _loadRepos()
    repos.update({os.path.expandvars(newRepo): os.path.expandvars(newRepoBackup)})
    _saveRepos(repos)

def excludeRepo(excRepo):  #remove a directory from the list
    repos = _loadRepos()
    try:
        del(repos[os.path.expandvars(excRepo)])
        _saveRepos(repos)
    except KeyError:
        print('Local repository not found.')

def backup():   #Back up all of the listed directories
    repos = _loadRepos()
    for localRepo in repos.keys():
        print('cd to {}'.format(localRepo))

        gitResults = _git('status')
        if gitResults != (b'On branch master\nnothing to commit, working tree clean\n', b''):
            print('Changes needing committed.')

            print('git add .')
            print('git commit -m "gitBack autocommit on <date> at <time>"')
        print('git push {} master'.format(repos[localRepo]))
    
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
        elif sys.argv[1] == 'backup':
            backup()
    else:
        usage()