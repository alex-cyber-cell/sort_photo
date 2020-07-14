########################################################################################################################
##
##  Script Name: sort_photo.py
##       Author: Unknown
##         Year: 2020
##        Month: October
##  Description: Script which sorts photos by date
##
########################################################################################################################

########################################################################################################################
##     USEFUL LINKS
########################################################################################################################
#Logging - https://www.toptal.com/python/in-depth-python-logging

########################################################################################################################
##  ENVIRONMENT VARIABLES
########################################################################################################################


########################################################################################################################
##  IMPORTS
########################################################################################################################

import sys, getopt, logging, argparse, os, datetime

from PIL import Image

########################################################################################################################
##  FUNCTION DEFINITION
########################################################################################################################
class Photo:
    def __init__(self, path):
        print('classPhoto: (init) Executed ...')
        self.photoPath = path
        self.cDate = self.getCreationDate()

    def getCreationDate(self):
        return Image.open(self.photoPath)._getexif()[36867].split(' ')[0].replace(':','')

########################################################################################################################
##  FUNCTION DEFINITION
########################################################################################################################
def getAvailableSpace():
    #function to get the available space on target device 
    print('getAvailableSpace: Executed ...')
    
def getNecessarySpace():
    #function to get the necessary space on target device 
    print('getNecessarySpace: Executed ...')
    
def compareSpace():
    #function to compare the necessary and avaialble space
    print('compareSpace: Executed ...')
    
def createDateFolder():
    #function to check if folder for given date exists in target location and 
    #creates it if not 
    print('createDateFolder: Executed ...')

def getFiles(src):
    #function to generate a list of files that we need to sort
    print('getFiles: Executed ...')
    print('getFiles: Creating empty list ...')
    LOF = []
    print('getFiles: Concatenating files ...')
    for root, subdirs, files in os.walk(src):
        for fl in files:
            LOF.append('/'.join([root,fl]))
    return LOF

def copyFilesAcross(LOF,dest):
    print('copyFilesAcross: Executed ...')
    print('copyFilesAcross: Creating list of objects for photos')
    objs = []
    for fl in LOF:
        if(fl.split('.')[-1] == 'jpg'):
            objs.append(Photo(fl))
        else:
            print('copyFilesAcross: Not implemented for extension: ' + fl.split('.')[-1])


def getCmdLineArguments():
    #function to get command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-sourceDir',
                        '--sourceDirectory',
                        required=True,
                        help='The directory where all the photos are')
    parser.add_argument('-destDir',
                        '--destDirectory',
                        required=True,
                        help='Directory where files should be sorted')
    parser.add_argument('-logDir',
                        '--logDirectory',
                        help="""Directory where the log file should be dumped.
                                If empty this will be set to home dir""")
    args = parser.parse_args()
    if(args.logDirectory==None):
        print('Log Directory has not been provided. Setting to script directory')
        args.logDirectory = os.path.dirname(sys.argv[0]) + '/'
        #Adding the log directory
        args.logDirectory = args.logDirectory + 'log/'
        os.makedirs(args.logDirectory, exist_ok=True)
        print('Log folder is now set to ' + args.logDirectory)
    return args

def main ():
    #get command line arguments
    cmdlineArgs = getCmdLineArguments()
    #get all the files in folder
    listOfFiles = getFiles(cmdlineArgs.sourceDirectory)
    #get meta of photo and copy across
    copyFilesAcross(listOfFiles,cmdlineArgs.destDirectory)

########################################################################################################################
##  MAIN
########################################################################################################################
if __name__ == "__main__":
    main()
