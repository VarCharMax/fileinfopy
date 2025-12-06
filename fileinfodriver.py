"""Framework for getting filetype-specific metadata.
Instantiate appropriate class with filename. Returned object acts like a
dictionary, with key-value pairs for each piece of metadata:
    import mp3fileinfo
    info = mp3fileinfo.MP3FileInfo("C:/temp/01 Born In Chicago.mp3")
    print("\n".join(["%s=%s" % (k, v) for k, v in info.items()]))
Or use listdirectory function to get info on all files in a directory:
    driver = FileInfoDriver()
    for info in driver.listdirectory("C:/temp/", [".mp3"]):
...
Framework can be extended by adding classes for particular file types, e.g.
HTMLFileInfo, MPGFileInfo, DOCFileInfo. Each class is completely responsible for
parsing its files appropriately; see MP3FileInfo for example.

TODO: Make driver agnostic as to file extensions.
      Write at least one more driver, e.g. JPGFileInfo.
"""
import sys
import os
import importlib.util
from types import ModuleType
from string import Template
from fileinfo import FileInfo

class FileInfoDriver:
    """_summary_
    """
    def __import_from_path(self, module_name, file_path) -> ModuleType | None:
        """Import a module given its name and file path."""
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec:
            module = importlib.util.module_from_spec(spec)
            # Add to internal imported modules list.
            sys.modules[module_name.lower()] = module
            spec.loader.exec_module(module) # type: ignore
            return module
        raise ModuleNotFoundError()

    def listdirectory(self, directory, fileextlist) -> list[FileInfo]:
        "get list of dictionaries containing meta info for files of specified extension"
        # Get list of files in directory.
        filelist = [os.path.normcase(f) for f in os.listdir(directory)]
        # Create full path to file, filter by extension.
        filelist = [os.path.join(directory, f) for f in filelist
                    if os.path.splitext(f)[1] in fileextlist]

        def file_ext(path):# -> Any:
            return os.path.splitext(path)[1].upper()[1:]

        def getfileinfoclass(filename) -> type[FileInfo]:
            # e.g. .mp3 -> MP3FileInfo
            subclass = Template('${ext}FileInfo').substitute(ext=file_ext(filename))
            modulename = subclass.lower() # e.g. mp3fileinfo
            # Use cached module if already loaded.
            if modulename in sys.modules:
                module = sys.modules[modulename]
            else:
                try:
                    # Otherwise try to load module from file.
                    module = self.__import_from_path(subclass,
                        os.path.join(os.path.dirname(__file__), f"{modulename}.py"))
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
