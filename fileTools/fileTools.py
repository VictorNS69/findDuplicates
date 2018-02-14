

__AUTHOR__ = "Victor Nieves Sanchez"
__COPYRIGHT__ = "Copyright 2018, Victor Nieves Sanchez"
__CREDITS__ = ["Victor Nieves Sanchez", "Tobias Diaz"]
__LICENSE__ = "GPL"
__VERSION__ = "3.0.0"
__PYTHON__= "3.6.4"
__EMAIL__ = "vnievess@gmail.com"


import hashlib
import os.path
import os
import glob
import logging
from os.path import getsize

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
        self.__rebuild_file_list__()

    @property
    def root(self):
        return self.__root

    @root.setter
    def root(self, new_root):
        self.__root = new_root
        self.__rebuild_file_list__()

    @property
    def files(self):
        return self.__candidates

    def __rebuild_file_list__(self):
        self.__candidates = []
        self.__make_candidates__(self.__recursive)

    def __make_candidates__(self, recursive):
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


