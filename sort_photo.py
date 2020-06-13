###############################################################################
##
##  Script Name: sort_photo.py
##       Author: Unknown
##         Year: 2019
##        Month: October
##  Description: Script which sorts photos by date
##
###############################################################################

###############################################################################
##  ENVIRONMENT VARIABLES
###############################################################################



###############################################################################
##  IMPORTS
###############################################################################

import sys, getopt

###############################################################################
##  FUNCTION DEFINITION
###############################################################################


class log:
    #class to manage log file and printing to screen
    def __init__(self, logFilePath):
        self.logFilePath=logFilePath

    def logTime(self):
        return datetime.datetime.now().strftime("%Y.%m.%dD%H.%M.%S.%f")

    def lvl(self, level):
        if (level == 0):
            prefix = "[*INFO]|"
        elif (level == 1):
            prefix = "[ERROR]|"
        else:
            prefix = "[DEBUG]|"
        return prefix + getTimestamp() + "| " + message

def getAvailableSpace():
    #function to get the available space on target device 
    print('getAvailableSpace: Executed ...')
    
def getNecessarySpace():
    #function to get the necessary space on target device 
    print('getNecessarySpace: Executed ...')
    
def compareSpace():
    #function to compare the necessary and avaialble space
    print('compareSpace: Executed ...')
    
def getPhotoDate():
    #function to get the date when the photo was taken 
    print('getPhotoDate: Executed ...')
    
def createDateFolder():
    #function to check if folder for given date exists in target location and 
    #creates it if not 
    print('createDateFolder: Executed ...')

def getCmdLineArguments():
    # function to create a dictionary of arguments passed from the cmdline
    dictVal = {}  # Creating an empty dictionary
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "hd:f:t:l:",["SORTPHOTO_FROM=", "SORTPHOTO_TO=", "SORTPHOTO_LOG="])
    except getopt.GetoptError:
        print('getCmdLineArguments: Failed to get command line arguments ...')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(
                "\nHelp Message:\nsort_photo.py --SORTPHOTO_FROM [path] --SORTPHOTO_TO [path] --SORTPHOTO_LOG [path]\n")
            sys.exit()
        elif opt in ("-f", "--SORTPHOTO_FROM"):
            dictVal['SORTPHOTO_FROM'] = arg
        elif opt in ("-t", "--SORTPHOTO_TO"):
            dictVal['SORTPHOTO_TO'] = arg
        elif opt in ("-l", "--SORTPHOTO_LOG"):
            dictVal['SORTPHOTO_LOG'] = arg
    return dictVal

def main ():
    dictVal = getCmdLineArguments()

###############################################################################
##  MAIN
###############################################################################
if __name__ == "__main__":
    main()
