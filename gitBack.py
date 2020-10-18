import sys
import subprocess as sp

def usage():     #print out usage
    with open('usage.txt', 'r') as file:
        print(file.read())

def list():     #print out the list
    pass

def include(newDir, newDirBackup = None):  #add a new directory to the list
    pass

def exclude(excDir):  #remove a directory from the list
    pass

def backup():   #Back up all of the listed directories
    p = sp.Popen('git status', stdout = sp.PIPE, stderr = sp.PIPE)
    gitOut, gitErr = sp.communicate()
    
if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '--list':
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