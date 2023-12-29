# About Hex Writer
Hex Writer is a Python program utilizing Tkinter Canvases to draw out the hexagram representation of messages typed out into the window.

Hexagrams (in the context of this project) are an encoding of the english language used to represent 4 character strings including letters,
numbers, and spaces. The full structure rules are still being worked on for how to represent full sentences that require more than one hexagram
to encode the sentence.

# Work In Progress Features:
1. Drawing Hexes (its the start of the project, of course its WIP)
2. Character to hex encoder

# Known Bugs:
* The encoding process does not know how to handle special characters (.,!#$ etc). This is something that will be addressed in the future. For now it fails gracefully and should reprompt for text.

# Possible Future Features (in no particular order):
* Alphabet display
* Structure rules display
  * requires finalization of structure rules
* "How to encode/decode" tutorial
* Export image
* Handle special characters in encoding (see known bugs)
