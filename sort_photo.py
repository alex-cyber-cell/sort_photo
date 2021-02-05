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
fileFrmt = {'jpg'  : 'Photo',
            'JPEG' : 'Photo',
            'JPG'  : 'Photo',
            'mp4'  : 'Mov'}

########################################################################################################################
##     ENVIRONMENT VARIABLES
########################################################################################################################

########################################################################################################################
##     IMPORTS
########################################################################################################################

import sys, getopt, logging, argparse, os, datetime, shutil, pymediainfo
import pandas as pd
from multiprocessing import Process, current_process

from PIL import Image

########################################################################################################################
##     CLASS DEFINITION
########################################################################################################################
class Photo:
    def __init__(self, path, dest):
        self.itemSource = path
        self.coreDest = dest
        self.cDate = self.getCreationDate()
        self.itemDest = self.buildDestPath()

    def buildDestPath(self):
        #create a destination path
        return self.coreDest + self.cDate + '/'

    def getCreationDate(self):
        #get the date of creation
        #36867 - DateTimeOriginal : The date and time when the original image data was generated
        #36868 - DateTimeDigitized : The date and time when the image was stored as digital data
        #306 - DateTime : the date and time of iamge creation. In this standard it is the date and time the file was changed
        #If 36867 and 36868 are missing use 306
        exifData = Image.open(self.itemSource)._getexif()
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
        print("class[Photo]|Method[copyFile]: Creating directory " + self.itemDest)
        os.makedirs(self.itemDest, exist_ok=True)

    def copyFile(self):
        #method to copy the file across
        print("class[Photo]|Method[copyFile]: Copying file " + (self.itemSource.split('/')[-1]) + " to " + self.itemDest)
        self.createPath()
        shutil.copy(self.itemSource, self.itemDest)

class Mov:
    def __init__(self, path, dest):
        self.itemSource = path
        self.coreDest = dest
        self.cDate = self.getCreationDate()
        self.itemDest = self.buildDestPath()

    def buildDestPath(self):
        #create a destination path
        return self.coreDest + self.cDate + '/'

    def getCreationDate(self):
        #get the date of creation using pymediainfo
        return pymediainfo.MediaInfo.parse(self.itemSource).tracks[0].encoded_date.split(' ')[1].replace('-','')

    def createPath(self):
        #create the necessary directory where the file will be copied
        print("class[Mov]|Method[copyFile]: Creating directory " + self.itemDest)
        os.makedirs(self.itemDest, exist_ok=True)

    def copyFile(self):
        #method to copy the file across
        print("class[Mov]|Method[copyFile]: Copying file " + (self.itemSource.split('/')[-1]) + " to " + self.itemDest)
        self.createPath()
        shutil.copy(self.itemSource, self.itemDest)

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

def createDF(LOF, dest):
    print('Creating dataframe of files to be copied ...')
    dfCols = ['date', 'source', 'destination']
    print('Creating empty dataframe ...')
    FDF = pd.DataFrame(columns = dfCols)
    print('Populating dataframe ...')
    for f in LOF:
        inst = getattr(sys.modules[__name__],fileFrmt[f.split('.')[-1]])(f, dest)
        FDF.loc[len(FDF)] = [inst.getCreationDate(), f, inst.buildDestPath()]
    print('Sorting data frame by date ...')
    FDF = FDF.sort_values(by=['date'])
    return FDF

def copyFilesAcross(lst):
    #keep only the date provided as parameter
    df = lst[0]
    dt = lst[1]
    for d in dt:
        subDf = df[df.date == d]
        print("Processing date " + d + ' for PID: ', os.getpid())
        for index,row in subDf.iterrows():
            try:
                #print('Making directory ' + row['destination'])
                os.makedirs(row['destination'], exist_ok=True)
                shutil.copy(row['source'], row['destination'])
            except OSError as e:
                print('Failed to copy file ' + row['source'] + ' with error {0}'.format(e) )
            except:
                print("Unexpected error: ", sys.exc_info()[0])

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

########################################################################################################################
##  MAIN
########################################################################################################################
if __name__ == "__main__":
    #get command line arguments
    cmdlineArgs = getCmdLineArguments()
    #get all the files in folder
    listOfFiles = getFiles(cmdlineArgs.sourceDirectory)
    #create dataframe of files which needs to be copied
    filesDF = createDF(listOfFiles, cmdlineArgs.destDirectory)
    processes = []
    lstOfDates = list(set(filesDF['date'].to_list()))
    lstOfDates.sort()
    splitListOfDatesForProc = [(lstOfDates[i:i+3]) for i in range(0, len(lstOfDates), 3)]
    for dt in splitListOfDatesForProc:
        p = Process(target=copyFilesAcross, args=([filesDF, dt],))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()


