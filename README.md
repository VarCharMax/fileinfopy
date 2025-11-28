# fileinfopy

Derived from an exercise in Mark Pilgrim's Python book, but re-written to be more efficient and, hopefully, more useful.

I wanted to be able to load the driver modules dynamically from the parent folder. To facilitate this, I added a dictionary to cache already-loaded modules.

I'll try to add some additional moddules if I can get info on how to parse their meta data. The goal is that you should be able to point it at any folder, and it will attempt to load the correct module for every file type it encounters.
