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
##     GLOBAL VARIABLES
########################################################################################################################

########################################################################################################################
##     ENVIRONMENT VARIABLES
########################################################################################################################
fileFrmt = {'jpg'  : 'jpg',
            'JPEG' : 'jpg',
            'JPG'  : 'jpg',
            'mp4'  : 'mp4'}
########################################################################################################################
##     IMPORTS
########################################################################################################################

import sys, getopt, logging, argparse, os, datetime, shutil

from PIL import Image

########################################################################################################################
##     FUNCTION DEFINITION
########################################################################################################################
class Photo:
    def __init__(self, path, dest):
        self.photoSource = path
        self.coreDest = dest
        self.cDate = self.getCreationDate()
        self.photoDest = self.buildDestPath()

    def buildDestPath(self):
        #create a destination path
        return self.coreDest + self.cDate + '/'

    def getCreationDate(self):
        #get the date of creation
        return Image.open(self.photoSource)._getexif()[36867].split(' ')[0].replace(':','')

    def createPath(self):
        #create the necessary directory where the file will be copied
        print("class[Photo]|Method[copyFile]: Creating directory " + self.photoDest)
        os.makedirs(self.photoDest, exist_ok=True)

    def copyFile(self):
        #method to copy the file across
        print("class[Photo]|Method[copyFile]: Copying file " + (self.photoSource.split('/')[-1]) + " to " + self.photoDest)
        self.createPath()
        shutil.copy(self.photoSource, self.photoDest)

########################################################################################################################
##     FUNCTION DEFINITION
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
    #print('copyFilesAcross: Creating list of objects for photos')
    #objs = []
    for fl in LOF:
        #get the file format
        fFrmt = fl.split('.')[-1]
        #if mapping exist map, otherwise inform
        if(fFrmt in fileFrmt.keys()):
            fFrmt = fileFrmt[fFrmt]
        else:
            print("Mapping does not exist for " + fFrmt)
        #execute specific class based on type
        if( fFrmt == 'jpg'):
            #objs.append(Photo(fl, dest))
            photo = Photo(fl, dest)
            photo.copyFile()
        elif (fFrmt == 'mp4'):
            print("Not Yet Implemented for " + fFrmt)
        else:
            print("Not yet Implemented for " + fFrmt)


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
