#!/usr/bin/env python3

__author__ = "Victor Nieves Sanchez"
__copyright__ = "Copyright 2018, Victor Nieves Sanchez"
__credits__ = ["Victor Nieves Sanchez"]
__license__ = "GPL"
__version__ = "2.0.1"
__python__= "3.6.4"
__email__ = "vnievess@gmail.com"


'''this program will print on the screen the duplicate files of the desired file. '''

import argparse
import os
import sys
import hashlib
import glob


class TargetFile(object):

    def __init__(self, fileName):
        self.fileName = fileName
        self.filePath = os.path.abspath(fileName)
        self.fileSize = os.path.getsize(os.path.abspath(fileName))
        self.fileMd5 = hashlib.md5(open(self.filePath, 'rb').read()).hexdigest()

def parse():
    parser = argparse.ArgumentParser(description='search if there are duplicate files of the desired file.')
    parser.add_argument('file', help='file name')
    parser.add_argument('path', nargs='?', default=os.getcwd(), action="store", help='source path')
    parser.add_argument('-r', '--recursive', default=False, action='store_true', help='search into directories',
                        dest='recursive')
    return parser.parse_args()

'''Recursive'''
def candidatesR (targetFile, path):
    print ("RECURSIVE SEARCH")
    candidates = []
    for fileName in glob.glob(path +'/**', recursive =True):
        if targetFile.fileSize == os.path.getsize (fileName) and\
                        targetFile.fileMd5 == hashlib.md5(open(fileName, 'rb').read()).hexdigest() and\
                        targetFile.filePath != os.path.abspath(fileName) and not os.path.islink(fileName):
            candidates.append(os.path.abspath(fileName))
    return candidates

'''Non-recursive'''
def candidatesNoR(targetFile, path):
    candidates = []
    print ("NON-RECURSIVE SEARCH")
    for fileName in glob.glob(path+'/*', recursive=False):
        if targetFile.fileSize == os.path.getsize(fileName) and \
                        targetFile.fileMd5 == hashlib.md5(open(fileName, 'rb').read()).hexdigest() and\
                        targetFile.filePath != os.path.abspath(fileName) and not os.path.islink(fileName):
            candidates.append(os.path.abspath(fileName))
    return candidates

def checkName (targetFile, fileList):
    if len(fileList) == 0:
        print ("No duplicated files.")
    else:
        for fileName in fileList:
            if targetFile.fileName == os.path.basename(fileName):
                print ("Duplicated file (SAME NAME) in: " + os.path.abspath(fileName))
            else:
                print ("Duplicated file (DIFFERENT NAME) in: " + os.path.abspath(fileName))

def main():
    userData = parse()
    try:
        tf = TargetFile(userData.file)
    except:
        print("ERROR: ", sys.exc_info()[0])
        sys.exit(1)
    files = []
    if userData.recursive:
        files = candidatesR(tf, userData.path)
    elif not userData.recursive:
        files = candidatesNoR(tf, userData.path)

    checkName(tf, files)
    sys.exit(0)


if __name__ == "__main__":
    main()
