"""Framework for getting filetype-specific metadata.
Instantiate appropriate class with filename. Returned object acts like a
dictionary, with key-value pairs for each piece of metadata.
import fileinfo
info = fileinfo.MP3FileInfo("/music/ap/mahadeva.mp3")
print("\n".join(["%s=%s" % (k, v) for k, v in info.items()]))
Or use listdirectory function to get info on all files in a directory.
for info in fileinfo.listdirectory("/music/ap/", [".mp3"]):
...
Framework can be extended by adding classes for particular file types, e.g.
HTMLFileInfo, MPGFileInfo, DOCFileInfo. Each class is completely responsible for
parsing its files appropriately; see MP3FileInfo for example.

TODO: Make driver agnostic as to file extensions.
"""
import os
import sys
import importlib.util
from fileinfo import FileInfo

class FileInfoDriver:
    """_summary_
    """
    def __init__(self):
        self.moduledict = {}

    def __getmodule__(self, name):
        """_summary_

        Args:
            name (_type_): _description_

        Returns:
            _type_: _description_
        """
        return self.moduledict.get(name) or None
    def __savemodule__(self, name, module):
        """_summary_

        Args:
            name (_type_): _description_
            module (_type_): _description_
        """
        self.moduledict[name] = module

    def __import_from_path__(self, module_name, file_path):
        """Import a module given its name and file path."""
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module

    def listdirectory(self, directory, fileextlist):
        "get list of dictionaries containing meta info for files of specified extension"
        # Get list of files in directory.
        filelist = [os.path.normcase(f) for f in os.listdir(directory)]
        # Create full path to file, filter by extension.
        filelist = [os.path.join(directory, f) for f in filelist
                    if os.path.splitext(f)[1] in fileextlist]

        def getfileinfoclass(filename):
            "get file info class according to filename extension"
            subclass = f"{os.path.splitext(filename)[1].upper()[1:]}FileInfo" # e.g. .mp3 -> MP3FileInfo
            modulename = subclass.lower() # e.g. mp3fileinfo
            # Use cached module if already loaded.
            modtmp = self.__getmodule__(modulename)
            if modtmp:
                module = modtmp
            else:
                try:
                    # Otherwise try to load module from file.
                    module = self.__import_from_path__(subclass,
                        os.path.join(os.path.dirname(__file__), f"{modulename}.py"))
                    self.__savemodule__(modulename, module)
                except ModuleNotFoundError:
                    return FileInfo

            return hasattr(module, subclass) and getattr(module, subclass) or FileInfo

        # Get custom dictionary object for specific file type,
        # Initialise parent dictionary with ["name"]=<filename>,
        # Parse file meta data into child dictionary and return list of dictionaries.
        return [getfileinfoclass(f)(f) for f in filelist]

if __name__ == "__main__":
    # info is subclassed FileInfo dictionary containing file metadata.
    driver = FileInfoDriver()
    for info in driver.listdirectory("C:/temp/", [".mp3"]):
        print("\n".join([f"{k}={v}" for (k, v) in info.items()]))
        print()
