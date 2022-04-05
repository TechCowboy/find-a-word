# find-a-word

Python example of using a user created module, importing it
and interacting with it with text and graphical user interfaces

If you use this code, please credit this repository

word list:

    The 'all words' list was downloaded from
    https://www.sketchengine.eu/english-word-list/#tab-id
    
    english-word-list-nouns.csv

    The file format is a bit odd for a csv.  It uses ';' as a separator
    and the word list doesn't start until line 5.  The word is in the
    second column.
    
    The program grabs all the words and rejects words that have punctuation
    in them (e.g., U.S., etc.) and any word less than 3 characters


user module:

  User modules require, at minimum, a blank __init__.py file and
  a the directory for the sources added to the LIB path 

  __init__.py - blank file

  faw.py      - contains a class for creating a find-a-word grid and the
                solution within it


GUIs:

  faw_gui.py  - Text based user interface.  No user interaction

  faw_gui2.py - Graphical user interface.  User clicks on first 
                character of a word to highlight it in the grid
                and on the word list


