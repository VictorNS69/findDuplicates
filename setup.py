#!/usr/bin/env python3

__AUTHOR__ = "Victor Nieves Sanchez"
__COPYRIGHT__ = "Copyright 2018, Victor Nieves Sanchez"
__CREDITS__ = ["Victor Nieves Sanchez", "Tobias Diaz"]
__LICENSE__ = "GPL"
__VERSION__ = "3.0.0"
__PYTHON__= "3.6.4"
__EMAIL__ = "vnievess@gmail.com"


from setuptools import setup

setup(name='Find Duplicates',
	version=__VERSION__,
	description='Search if there are duplicate files of the desired file.',
	author=__AUTHOR__,
	author_email=__EMAIL__,
	url='https://github.com/VictorNS69/findDuplicates',
	license=__LICENSE__,
	classifiers=['Programming Language :: Python :: 3.5'],
	packages=['fileTools'],
	package_dir={'fileTools':'src/'},)

