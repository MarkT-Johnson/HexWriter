# About Hex Writer
Hex Writer is a Python program utilizing Tkinter Canvases to draw out the hexagram representation of messages typed out into the window.

Hexagrams (in the context of this project) are an encoding of the english language used to represent 4 character strings including letters,
numbers, periods, and spaces. The full structure rules are still being worked on for how to represent full sentences that require more than one hexagram
to encode the sentence.

## How to Run:
* You must have python 3 installed. See https://www.python.org/downloads/ to download.
  * This was developed with python 3.10 and has not been tested on other versions though they will likely work.
* One option for running this script is to download the whole repo and run the main.py script manually.
  * ```python main.py```

* Alternatively, you can also download the HexWriter.exe under the ```dist``` directory if you are on windows.
  * Upon running this executable for the first time, this will likely create a pop up from windows defender indicating this is an unrecognized app. I trust you the reader to
   understand the risks inherent with downloading executables from the internet and make a decision. Read this blog from MalwareBytes if you
   want to learn more: https://www.malwarebytes.com/blog/news/2021/10/what-is-an-exe-file-is-it-the-same-as-an-executable
  * That said, if you do get the pop up from windows defender, this can be bypassed by clicking "More info" under this
  warning. This should then create a new option to "Run anyway" that you can click.
* After the window opens up, simply enter your text you want to encode in the top text bar and click "Draw Hexagram".
  * If you encounter any errors they should populate in the text box below the draw button, or if they are an unrecoverable
   error they will populate in the console that opened alongside the HexWriter window.

## License:
HexWriter by "Drakken_Dude" / Mark Johnson | GitHub: https://github.com/MarkT-Johnson/HexWriter

Distributed under Creative Commons License CC BY-NC-SA 4.0

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
* None known at this time

## Possible Future Features (in no particular order):
* Alphabet display
* Structure rules display
  * requires finalization of structure rules
* "How to encode/decode" tutorial
* Export image

## Bugfixes:
* The number '7' was not being checked for as a valid character. Updated valid characters and encoding behavior to handle '7'
