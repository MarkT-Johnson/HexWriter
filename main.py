from hexClass import Hexagram
import tkinter as tk
from alphabet import *
import ast

"""
HexWriter by "Drakken_Dude" / Mark Johnson | GitHub: https://github.com/MarkT-Johnson/HexWriter
Distributed under Creative Commons License CC BY-NC-SA 4.0
https://creativecommons.org/licenses/by-nc-sa/4.0/

Feel free to adapt/build on this as you wish!
"""


class EncodingError(Exception):
    pass


def decoder(lines: list[list[str]]) -> str:
    """
    Takes the numerical encoding and returns the text input that would have generated it.
    :param lines: The numerical encoding.
    :return: The text that could have generated this numerical encoding.
    """
    dirty_message = ""
    message = ""

    # Start by breaking the list of hexes into individual hexes
    # [['1111', '1000', '1101', '0001', '1010', '0101'], [...,...,...,...,...,...],...]
    for hex in lines:
        # Check the hex has the right number of triangles
        if len(hex) == 6:
            # ['1111', '1000', '1101', '0001', '1010', '0101']
            # Now we need to combine the characters in the same positions into the same list
            for loop in range(4):
                # loop determines where in each triangle we are pulling the parts of the letter from
                character_enc = ""
                for triangle in hex:
                    if len(triangle) == 4:
                        # Build the character from each triangle
                        character_enc = character_enc + triangle[loop]
                    else:
                        # This triangle does not contain 4 lines, raise an encoding/decoding error
                        raise EncodingError(f"Triangle {str(triangle)} in hex {str(hex)} does not represent 4 lines. "
                                            f"This is a malformed hex encoding")
                # Decode the letter and append to the message
                character_dec = alphabet_dec.get(character_enc)
                # If the decoded character is a period, append another period to make cleanup easier
                character_dec = character_dec if character_dec != "." else character_dec + "."

                dirty_message = dirty_message + character_dec
        else:
            # Hex does not have all triangles or has too many. Raise an error
            raise EncodingError(f" Hex {str(hex)} does not represent 6 triangles. This is a malformed hex encoding")

    # Now that we have the decoded message, we need to clean up the message by removing underscores and adding spaces
    # We assume we are starting with left preference as is used for encoding.
    left_letter = True
    index = 0
    end = index + 2
    while end <= len(dirty_message):
        # Get the first/next two characters to figure out if its left or right tracked
        character = dirty_message[index:end]

        if (character[0] == "_" and left_letter) or (character[0].isalpha() and not left_letter):
            # We have a break in the pattern, insert a space with the character
            character = " " + character.strip("_")
            # Do not alternate the left_letter tracker as we now expect the same preference
        elif character[0] == ".":
            # We have double periods. Keep one and do not alternate tracker
            character = "."
        elif (character[0].isalpha() and left_letter) or (character[0] == "_" and not left_letter):
            # The pattern agrees, alternate the tracker and strip _
            character = character.strip("_")
            left_letter = not left_letter
        else:
            # This should theoretically not occur but placing a catchall just in case
            raise EncodingError("There was an issue while decoding your message. Cleanup of decoded message failed")

        # Move the range down and append the character to the message
        index = end
        end = index + 2
        message = message + character

    return message.strip(".")


def encoder(text: str) -> list[list[str]]:
    """
    Takes the text input and encodes it into the line lists
    :param text: The text input
    :return: The list of triangles and what lines to draw for them
    """

    # Convert the text to all upper case. We need to split it into chunks of 4 while ignoring spaces.
    # chunk_count is used to keep track if we need to start a new chunk.
    text = text.upper()
    four_chunks = []
    new_chunk = ""
    chunk_count = 0
    for character in text:
        if character == " ":
            # If it's a space, subtract one from chunk_count
            chunk_count -= 1
        new_chunk += character
        chunk_count += 1

        if chunk_count == 4:
            # We have a full chunk, add it to the four_chunk list and reset chunk_count and new_chunk
            four_chunks.append(new_chunk)
            new_chunk = ""
            chunk_count = 0

    # If we have finished processing all characters in the text we need to ensure we capture any stragglers that might
    # not have completed a full chunk
    if new_chunk != "":
        # If last chunk is not a perfect set of 4 append a period to pad it
        while chunk_count < 4:
            new_chunk = new_chunk + "."
            chunk_count += 1
        four_chunks.append(new_chunk)

    # Left letter tracks whether our next letter should be a left or right
    left_letter = True
    # hexes holds the encoded hexes as we build it
    hexes = []
    for chunk in four_chunks:
        new_hex = ["", "", "", "", "", ""]
        for character in chunk:
            if character == " ":
                # If the character is a space then we alternate the left_letter tracker to break the pattern and stop
                # processing this character
                left_letter = not left_letter
                continue
            elif character in "1234567890.":
                # If the character is a number or period then we don't need to add a left right indicator or
                # alternate the tracker
                letter = character
            elif character.isalpha():
                # Determine where left right indicator is needed based on left_letter tracker
                letter = character + "_" if left_letter else "_" + character
                # Alternate the left_letter tracker
                left_letter = not left_letter
            else:
                # This must be a special character and is not encoded, stop processing and fail gracefully
                position = text.find(character) + 1
                raise EncodingError(f"Unknown character encountered: \"{character}\" at position {str(position)} in "
                                    f"input. Please only use english alphabet, periods, numbers, or spaces")

            # Get the encoding for each letter, then append the encoding to the new_hex
            encoding = alphabet_enc.get(letter)
            for triangle in range(0, 6):
                new_hex[triangle] = new_hex[triangle] + encoding[triangle]

        # add the new hex to the existing ones
        hexes.append(new_hex)

    return hexes


# Function to handle the Enter key press when user is finished typing
def on_enter_key(event):
    # Used because the binding of entry to the return key requires a function that can take in an event.
    # But since we don't need the event really, we can simply point it to a function that discards it on calling the
    # draw_hexagram function.
    draw_hexagram()


def draw_hexagram():
    # Encodes the user's message and draws the new hexagram
    message = "This is a default message, if you are seeing this then something has gone wrong. Sorry! ¯\\_(ツ)_/¯"
    try:
        # Clear the canvas before updating
        canvas.delete("all")
        # Get the text from the entry widget
        text = entry.get()
        if text[0] == "[":
            # The user is likely using the decoding function, we need to convert the text to a list[list[str]]
            encoded_text = ast.literal_eval(text)
            message = decoder(encoded_text)
        else:
            # This is likely new text, encode it as normal
            encoded_text = encoder(text)

        # Draw the hexagram on the canvas
        hex_num = 1
        if len(encoded_text) <= 7:
            for hexagon in encoded_text:
                Hexagram(hexagon, hex_num, canvas_size, canvas)
                hex_num += 1
            if text[0] != "[":
                message = str(encoded_text)
        else:
            length_err = "Message too long. Limited to 28 letters, numbers, and periods total. Spaces are not " \
                         "counted in this total."
            print(length_err)
            message = length_err

    except EncodingError as e:
        message = f"There was an encoding/decoding error:\n{e}"

    finally:
        text_output['state'] = "normal"
        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, message)
        text_output['state'] = "disabled"


################ Start of script ################
# Create the parent frame
window = tk.Tk()

window.title("HexWriter")
window.geometry("1000x1050")
window.resizable(False, False)

# Create a text box for user to enter text
entry = tk.Entry(window, width=50)
entry.bind("<Return>", on_enter_key)
entry.pack(pady=10)

# Create a button to update the canvas
button = tk.Button(window, text="Draw Hexagram", command=draw_hexagram)
button.pack(pady=10)

# Create a text box for communicating to the user.
text_output = tk.Text(window, width=300, height=3)
text_output.insert(tk.END, "Your message will also appear as a numerical encoded message here that you can save for "
                           "drawing again or decoding in the future.")
text_output.pack(pady=10)
text_output['state'] = "disabled"

# Create a canvas for drawing on
canvas_size = 1000
canvas = tk.Canvas(window, width=canvas_size, height=canvas_size, bg="white")

canvas.pack()

window.mainloop()
