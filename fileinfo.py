"""_summary_

    Returns:
        _type_: _description_
"""
class FileInfo(dict):
    """Initialize this parent class key ["name"] with filename value."""
    def __init__(self, filename=None):
        """This implementation does not override the parent dict __init__, which expects a k,v pair.
            We just redefine the init here for our own purposes."""
        self["name"] = filename

def stripnulls(data):
    "strip whitespace and nulls"
    return data.replace("\00", " ").strip()
