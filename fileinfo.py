"""_summary_

Returns:
    _type_: _description_
"""


class FileInfo(dict[str, str]):
    """Initialize this parent class key ["name"] with filename value."""

    def __init__(self, filename: str) -> None:
        """This implementation does not override the parent dict __init__, which expects a k,v pair.
        We just redefine the init here for our own purposes."""
        self["name"] = filename


def stripnulls(data: bytes) -> str:
    "strip whitespace and nulls"
    return data.decode().replace("\00", " ").strip()
