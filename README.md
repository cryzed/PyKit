PyKit
=====

PyKit is an automation library for Windows, supporting 32 and 64-bit applications. It currently supports controlling the cursor and detouring/hooking functions in foreign processes to local Python code.


Dependencies
------------
 - [WinAppDbg](http://winappdbg.sourceforge.net/) 1.5


Examples
--------
 - recettear.py
    - Implements a hotkey controlled (F1, F2) "vacuum hack", teleporting all mobs on the display to your location with a slight offset.
    - Dependencies:
        - [pywin32](http://sourceforge.net/projects/pywin32/)
        - [pyHook](http://sourceforge.net/projects/pyhook/)
