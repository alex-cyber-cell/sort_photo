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
#Tags for exif - https://pillow.readthedocs.io/en/stable/_modules/PIL/TiffTags.html?highlight=datetime
#Tags definition for exif - https://www.awaresystems.be/imaging/tiff/tifftags/datetime.html

########################################################################################################################
##     GLOBAL VARIABLES
########################################################################################################################
fileFrmt = {'jpg'  : 'jpg',
            'JPEG' : 'jpg',
            'JPG'  : 'jpg',
            'mp4'  : 'mp4'}

########################################################################################################################
##     ENVIRONMENT VARIABLES
########################################################################################################################

########################################################################################################################
##     IMPORTS
########################################################################################################################

import sys, getopt, logging, argparse, os, datetime, shutil, pymediainfo

from PIL import Image

########################################################################################################################
##     CLASS DEFINITION
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
        #36867 - DateTimeOriginal : The date and time when the original image data was generated
        #36868 - DateTimeDigitized : The date and time when the image was stored as digital data
        #306 - DateTime : the date and time of iamge creation. In this standard it is the date and time the file was changed
        #If 36867 and 36868 are missing use 306
        exifData = Image.open(self.photoSource)._getexif()
        if(36867 in exifData.keys()):
            tag = 36867
        elif(36868 in exifData.keys()):
            tag = 36868
        elif(306 in exifData.keys()):
            tag = 306
        else:
            tag = None

        return exifData[tag].split(' ')[0].replace(':','')

    def createPath(self):
        #create the necessary directory where the file will be copied
        print("class[Photo]|Method[copyFile]: Creating directory " + self.photoDest)
        os.makedirs(self.photoDest, exist_ok=True)

    def copyFile(self):
        #method to copy the file across
        print("class[Photo]|Method[copyFile]: Copying file " + (self.photoSource.split('/')[-1]) + " to " + self.photoDest)
        self.createPath()
        shutil.copy(self.photoSource, self.photoDest)

class Mov:
    def __init__(self, path, dest):
        self.movSource = path
        self.coreDest = dest
        self.cDate = self.getCreationDate()
        self.movDest = self.buildDestPath()

    def buildDestPath(self):
        #create a destination path
        return self.coreDest + self.cDate + '/'

    def getCreationDate(self):
        #get the date of creation using pymediainfo
        return pymediainfo.MediaInfo.parse(self.movSource).tracks[0].encoded_date.split(' ')[1].replace('-','')

    def createPath(self):
        #create the necessary directory where the file will be copied
        print("class[Mov]|Method[copyFile]: Creating directory " + self.movDest)
        os.makedirs(self.movDest, exist_ok=True)

    def copyFile(self):
        #method to copy the file across
        print("class[Mov]|Method[copyFile]: Copying file " + (self.movSource.split('/')[-1]) + " to " + self.movDest)
        self.createPath()
        shutil.copy(self.movSource, self.movDest)

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
            photoObj = Photo(fl, dest)
            photoObj.copyFile()
        elif (fFrmt == 'mp4'):
            #print("Not Yet Implemented for " + fFrmt)
            movObj = Mov(fl, dest)
            movObj.copyFile()
        else:
            print("No handler for format " + fFrmt + ". Copying in extension named folder ...")
            dst = dest + fFrmt + '/'
            os.makedirs(dst, exist_ok=True)
            shutil.copy(fl,dst)


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
