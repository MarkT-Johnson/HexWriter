# About Hex Writer
Hex Writer is a Python program utilizing Tkinter Canvases to draw out the hexagram representation of messages typed out into the window.

Hexagrams (in the context of this project) are an encoding of the english language used to represent 4 character strings including letters,
numbers, and spaces. The full structure rules are still being worked on for how to represent full sentences that require more than one hexagram
to encode the sentence.

## Features:
* Drawing Hexes (only one hex)
* Text to hex encoder (not displayed in window)

## Work In Progress Features:
1. Dynamic origin determination
   * Current limitation on the one hex only requirement
   * Need to figure out how to determine the new angle for the bearing method to use
2. Draw more than one hex (requires Dynamic Origin Determination)

## Known Bugs:
* None known so far

## Possible Future Features (in no particular order):
* Alphabet display
* Structure rules display
  * requires finalization of structure rules
* "How to encode/decode" tutorial
* Export image
* Handle special characters in encoding (see known bugs)
* Show text encoding in window
