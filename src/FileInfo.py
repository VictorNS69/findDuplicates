

__AUTHOR__ = "Victor Nieves Sanchez"
__COPYRIGHT__ = "Copyright 2018, Victor Nieves Sanchez"
__CREDITS__ = ["Victor Nieves Sanchez", "Tobias Diaz"]
__LICENSE__ = "GPL"
__VERSION__ = "3.0.0"
__PYTHON__= "3.6.4"
__EMAIL__ = "vnievess@gmail.com"


import hashlib
import os.path

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


