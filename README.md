PyKit
=====
PyKit is an automation library for Windows, supporting 32 and 64-bit applications. It currently supports controlling the cursor, searching for and setting pixels on the screen and detouring/hooking functions in foreign processes to local Python code.


Dependencies
------------
 - [WinAppDbg](http://winappdbg.sourceforge.net/) 1.5


Examples
--------
 - recettear.py

    Implements a hotkey controlled (F1, F2) "vacuum hack" for the game "Recettear: An Item Shop's Tale" version 1.105, teleporting all mobs to your location with a slight offset. F2 toggles the hack and F1 sets the vacuum position.

    - Dependencies:
        - [pywin32](http://sourceforge.net/projects/pywin32/)
        - [pyHook](http://sourceforge.net/projects/pyhook/)
    - Screenshots:
        - [#1](http://i.imgur.com/LPcPjNY.gif)
        - [#2](http://s13.postimg.org/4sninp2fp/screenshot2_gif.gif)
