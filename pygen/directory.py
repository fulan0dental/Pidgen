# -*- coding: utf-8 -*-


"""
Directory parsing
"""

import os
from .element import PyGenElement
from .file import PyGenFileParser
from . import debug


class PyGenDirectoryParser(PyGenElement):
    """
    Class for parsing a directory of protocol definition files.
    """

    def __init__(self, dirpath, **kwargs):

        if "path" not in kwargs:
            kwargs["path"] = dirpath

        PyGenElement.__init__(self, **kwargs)

        self._files = []
        self._dirs = []

        self.parse()

    def parse(self):
        """ Parse the current directory.
        - Look for any subdirectories
        - Look for any protocol files (.yaml)
        - Note: .yaml files prefixed with _ character are treated differently.
        """

        debug.debug("Parsing directory:", self.path)

        listing = os.listdir(self.path)

        files = []
        dirs = []

        for item in listing:
            path = os.path.join(self.path, item)

            if os.path.isdir(path):
                dirs.append(item)

            if os.path.isfile(path) and item.endswith(".yaml"):
                files.append(item)

        # Parse any files first
        self.parseFiles(files)

        # Then parse any sub-directories
        self.parseSubDirs(dirs)

    def parseFiles(self, files):

        if len(files) == 0:
            debug.info("No protocol files found in directory '{d}'".format(d=self.path))

        # Parse all protocol files
        for f in files:

            if f.startswith("_"):
                # TODO - Special files which augment the protocol generation
                continue

            self._files.append(PyGenFileParser(os.path.join(self.path, f), settings=self.settings))

    def parseSubDirs(self, dirs):
        for d in dirs:

            self._dirs.append(PyGenDirectoryParser(os.path.join(self.path, d), settings=self.settings))

