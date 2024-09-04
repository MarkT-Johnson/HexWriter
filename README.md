# About Hex Writer
Hex Writer is a Python program utilizing Tkinter Canvases to draw out the hexagram representation of messages typed out into the window.

Hexagrams (in the context of this project) are an encoding of the english language used to represent 4 character strings including letters,
numbers, periods, and spaces. The full structure rules are still being worked on for how to represent full sentences that require more than one hexagram
to encode the sentence.

## License:
HexWriter by "Drakken_Dude" / Mark Johnson | GitHub: https://github.com/MarkT-Johnson/HexWriter
Distributed under Creative Commons CC BY-NC-SA 4.0 License
https://creativecommons.org/licenses/by-nc-sa/4.0/

Feel free to adapt/build on this as you wish!

## Features:
* Drawing Hexes (1-7 hexes)
* Text to hex encoder (not displayed in window)
* Show text encoding in window
* GUI input for text

## Work In Progress Features:
1. Dynamic origin determination (7+ hexes)
   * Need programmatic way to determine location of hexes outside of layers 1-2
2. Draw more than 7 hex (requires Dynamic Origin Determination (7+ hexes))

## Known Bugs:
* None known so far

## Possible Future Features (in no particular order):
* Alphabet display
* Structure rules display
  * requires finalization of structure rules
* "How to encode/decode" tutorial
* Export image

## Bugfixes:
* The number '7' was not being checked for as a valid character. Updated valid characters and encoding behavior to handle '7'
