#!/usr/bin/env python3

__author__ = "Victor Nieves Sanchez"
__copyright__ = "Copyright 2018, Victor Nieves Sanchez"
__credits__ = ["Victor Nieves Sanchez"]
__license__ = "GPL"
__version__ = "2.0.0"
__python__= "3.6.4"
__email__ = "vnievess@gmail.com"

'''this program will print on the screen the duplicate files of the desired file. '''

import argparse
import os
import sys
import hashlib
import glob
from os.path import getsize, basename
import os.path
import logging

_DEB = logging.debug
_ERR = logging.error

class FileInfo(object):
    def __init__(self, filename):
        if not os.path.isfile(filename):
            raise OSError('File not found: %s' % filename)
        self.__fileName = filename

    @property
    def name(self):
        return self.__fileName

    @property
    def path(self):
        return os.path.abspath(self.name)

    @property
    def size(self):
        return os.path.getsize(os.path.abspath(self.name))

    @property
    def md5(self):
        return hashlib.md5(open(self.name, 'rb').read()).hexdigest()

    def __eq__(self, other_file):
        ''' self == other_file '''
        if other_file.size != self.size:
            return False
        if other_file.md5 != self.md5:
            return False
        return True

    def __ne__(self, other_file):
        ''' self != other_file '''
        return not self.__eq__(other_file)

    def __str__(self):
        return self.name


class FileSet(object):
    '''Computes file list to allow quick search'''
    def __init__(self, root_folder, recursive=False):
        self.__root = root_folder
        self.__recursive = recursive
        self._rebuild_file_list_()

    @property
    def root(self):
        return self.__root

    @root.setter
    def root(self, new_root):
        self.__root = new_root
        self._rebuild_file_list_()

    @property
    def files(self):
        return self.__candidates

    def _rebuild_file_list_(self):
        self.__candidates = []
        self._make_candidates_(self.__recursive)

    def _make_candidates_(self, recursive):
        for filename in glob.glob(os.path.join(self.root, '**' if recursive else '*'), recursive=recursive):
            filename = os.path.abspath(filename)
            if os.path.islink(filename):
                continue
            _DEB('Adding file %s' % filename)
            self.__candidates.append(filename)

    def search_by_size(self, size):
        result = list(filter(lambda f: os.path.getsize(f) == size, self.files))
        _DEB('Files with size %s found: %s' % (size, ','.join(result)))
        return result

    def __assert_exists__(self, filename):
        filename = os.path.abspath(filename)
        if filename not in self.files:
            raise ValueError('File %s not in filelist' % filename)
        return filename
    
    def get_fileinfo(self, filename):
        filename = self.__assert_exists__(filename)
        return FileInfo(filename)

    def remove(self, filename):
        filename = self.__assert_exists__(filename)
        self.__candidates.remove(filename)


def parse():
    parser = argparse.ArgumentParser(description='search if there are duplicate files of the desired file.')
    parser.add_argument('file', help='file name')
    parser.add_argument('path', nargs='?', default=os.getcwd(), action="store", help='source path')
    parser.add_argument('-r', '--recursive', default=False, action='store_true', help='search into directories',
                        dest='recursive')
    parser.add_argument('-p', '--pretty-output', default=False, action='store_true', help='show pretty output',
                        dest='pretty_output')
    parser.add_argument('--debug', default=False, action='store_true', help='be verbose',
                        dest='debug')
    parser.add_argument('--version', action='version', version=__version__)
    
    return parser.parse_args()


def show_pretty(duplicates):
    if len(duplicates) > 0:
        print('Duplicates files found:')
        for f in duplicates:
            print('\t%s' % f)


def main():
    userData = parse()
    try:
        target = FileInfo(userData.file)
    except OSError as e:
        _ERR("Error reading file %s: %s" % (userData.file, e))
        sys.exit(1)
        
    files = FileSet(userData.path, userData.recursive)
    try:
        files.remove(target.name)
    except ValueError:
        pass
        
    candidates = [FileInfo(f) for f in files.search_by_size(target.size)]
    equals = list(filter(lambda f: f == target, candidates))

    if userData.pretty_output:
        show_pretty(equals)
    else:
        # Show output
        for f in equals:
            print(str(f))
    sys.exit(0)


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s %(levelname)s %(message)s',
        level=logging.DEBUG if '--debug' in sys.argv else logging.INFO)
    main()
