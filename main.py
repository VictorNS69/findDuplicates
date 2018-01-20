#!/usr/bin/env python

__author__ = "Victor Nieves Sanchez"
__copyright__ = "Copyright 2018, Victor Nieves Sanchez"
__credits__ = ["Victor Nieves Sanchez"]
__license__ = "GPL"
__version__ = "2.0.0"
__python__= "3.6.4"
__maintainer__ = "Victor Nieves Sanchez"
__email__ = "vnievess@gmail.com"
__status__ = "Production"

'''this program will print on the screen the duplicate files of the desired file. '''

import argparse
import os
import sys
import hashlib
import glob
from os import listdir
from os.path import isfile, join, getsize, basename


class TargetFile(object):
    fileName = ""
    filePath = ""
    fileSize = 0
    fileMd5 = ""

    def __init__(self, file):
        self.fileName = file
        self.filePath = os.path.abspath(file)
        self.fileSize = os.path.getsize(self.filePath)
        self.fileMd5 = hashlib.md5(open(self.filePath, 'rb').read()).hexdigest()

def parse():
    parser = argparse.ArgumentParser(description='search if there are duplicate files of the desired file.')
    parser.add_argument('file', nargs='+', help='file Name')
    parser.add_argument('path', nargs='?', default=os.getcwd(), help='source path')
    #parser.add_argument('path', default=os.getcwd(), help='Search into directories', action='store_true')
    parser.add_argument('-r', '--recursive', default=False, action='store_true', help='search into directories',
                        dest='recursive')
    return parser.parse_args()

'''Recursive'''
def candidatesR (targetFile):
    print ("RECURSIVE SEARCH")
    candidates = []
    allFiles = glob.glob('**/*', recursive =True)
    for file in allFiles:
        if targetFile.fileSize == os.path.getsize (file) and\
                        targetFile.fileMd5 == hashlib.md5(open(file, 'rb').read()).hexdigest():
            candidates.append(os.path.abspath(file))
    candidates.remove(targetFile.filePath)
    return candidates

'''Non-recursive'''
def candidatesNoR(targetFile):
    candidates = []
    print ("NON-RECURSIVE SEARCH")
    allFiles = glob.glob('*', recursive=False)
    for file in allFiles:
        if targetFile.fileSize == os.path.getsize(file) and \
                        targetFile.fileMd5 == hashlib.md5(open(file, 'rb').read()).hexdigest():
            candidates.append(os.path.abspath(file))
    candidates.remove(targetFile.filePath)
    return candidates

def checkName (targetFile, fileList):
    if len(fileList) == 0:
        print ("No duplicated files.")
    else:
        for file in fileList:
            if targetFile.fileName == os.path.basename(file):
                print ("Duplicated file (SAME NAME) in: " + os.path.abspath(file))
            else:
                print ("Duplicated file (DIFFERENT NAME) in: " + os.path.abspath(file))

def main():
    userData = parse()
    target = str(", ".join(userData.file))
    try: 
        tf = TargetFile(target)
    except: 
        print("ERROR: This file does not exist.", sys.exc_info()[0])
        sys.exit(1)
    files = []
    if userData.recursive:
        files = candidatesR(tf)
    elif not userData.recursive:
        files = candidatesNoR(tf)

    checkName(tf, files)
    sys.exit(0)


if __name__ == "__main__":
    main()
