"""_summary_
"""

from fileinfo import FileInfo, stripnulls

class MP3FileInfo(FileInfo):
    "store ID3v1.0 MP3 tags"
    tagDataMap = {"title"   : (  3,  33, stripnulls),
                  "artist"  : ( 33,  63, stripnulls),
                  "album"   : ( 63,  93, stripnulls),
                  "year"    : ( 93,  97, stripnulls),
                  "comment" : ( 97, 126, stripnulls),
                  "genre"   : (127, 128, ord)}

    def __parse(self, filename):
        "parse ID3v1.0 tags from MP3 file"
        self.clear()
        try:
            with open(filename, "rb", 0) as fsock:
                fsock.seek(-128, 2)
                tagdata = fsock.read(128)

                if tagdata[:3].decode() == 'TAG':  # utf-8
                    # Dictionary with string key, tuple value of (start, end, parsefunc).
                    for tag, (start, end, parsefunc) in self.tagDataMap.items():
                        # Call back to __setitem__ to add key-value pair to dictionary.
                        self[tag] = parsefunc(tagdata[start:end].decode())
        except IOError:
            pass

    def __setitem__(self, key, item):
        """Called after parent dictionary is initialised with first key ["name"].
            Then goes on to parse additional metadata.
        Args:
            key (_type_): _description_
            item (_type_): _description_
        """
        if key == "name" and item:
            self.__parse(item)
        FileInfo.__setitem__(self, key, item)
