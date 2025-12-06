# fileinfopy

Derived from an exercise in Mark Pilgrim's Python book, but re-written to be more efficient and, hopefully, more useful.

I added the ability to load the driver modules dynamically from the parent folder, so that modules don't have to be declared in the driver file, as this seemed to defeat the purpose of making the app extensible.

I'll try to add some additional modules if I can get info on how to parse their meta data. The goal is that you should be able to point it at any folder, and it will attempt to load the correct module for every file type it encounters.
