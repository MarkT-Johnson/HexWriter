from hexClass import *
from tkinter import *
import re


# TODO Temporary Comment out while I figure out the encoding
# window = Tk()
#
# window.title("HexWriter")
# window.geometry("1000x1000")
#
# canvas_size = 1000
# canvas = Canvas(window, width=canvas_size, height=canvas_size, bg="white")
# canvas.pack()
#
# origin1 = [250, 750]
# origin2 = [500, 500]
#
# # lines = [[trianlge 1 lines], [triangle 2 lines],[triangle 3 lines], ...]
# all_lines = [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]]    # Dummy lines
#
# new_hex1 = Hexagram(all_lines, canvas_size, canvas)
# new_hex2 = Hexagram(all_lines, canvas_size)
#
# window.mainloop()


def encoder(text: str) -> list[int]:
    """
    Takes the text input and encodes it into the line lists
    :param text: The text input
    :return: The list of triangles and what lines to draw for them
    """
    # Switched to one deep list as the two deep list was unnecessarily complicated
    alphabet = {"1": [1, 0, 0, 0, 0, 0],
                "2": [0, 1, 0, 0, 0, 0],
                "3": [1, 1, 0, 0, 0, 0],
                "4": [0, 0, 1, 0, 0, 0],
                "5": [1, 0, 1, 0, 0, 0],
                "6": [0, 1, 1, 0, 0, 0],
                "7": [1, 1, 1, 0, 0, 0],
                "8": [0, 0, 0, 1, 0, 0],
                "9": [1, 0, 0, 1, 0, 0],
                "0": [0, 1, 0, 1, 0, 0],
                "A_": [1, 1, 0, 1, 0, 0],
                "B_": [0, 0, 1, 1, 0, 0],
                "C_": [1, 0, 1, 1, 0, 0],
                "D_": [0, 1, 1, 1, 0, 0],
                "E_": [1, 1, 1, 1, 0, 0],
                "F_": [0, 0, 0, 0, 1, 0],
                "G_": [1, 0, 0, 0, 1, 0],
                "H_": [0, 1, 0, 0, 1, 0],
                "I_": [1, 1, 0, 0, 1, 0],
                "J_": [0, 0, 1, 0, 1, 0],
                "K_": [1, 0, 1, 0, 1, 0],
                "L_": [0, 1, 1, 0, 1, 0],
                "M_": [1, 1, 1, 0, 1, 0],
                "N_": [0, 0, 0, 1, 1, 0],
                "O_": [1, 0, 0, 1, 1, 0],
                "P_": [0, 1, 0, 1, 1, 0],
                "Q_": [1, 1, 0, 1, 1, 0],
                "R_": [0, 0, 1, 1, 1, 0],
                "S_": [1, 0, 1, 1, 1, 0],
                "T_": [0, 1, 1, 1, 1, 0],
                "U_": [1, 1, 1, 1, 1, 0],
                "V_": [0, 0, 0, 0, 0, 1],
                "W_": [1, 0, 0, 0, 0, 1],
                "X_": [0, 1, 0, 0, 0, 1],
                "Y_": [1, 1, 0, 0, 0, 1],
                "Z_": [0, 0, 1, 0, 0, 1],
                "_A": [1, 0, 1, 0, 0, 1],
                "_B": [0, 1, 1, 0, 0, 1],
                "_C": [1, 1, 1, 0, 0, 1],
                "_D": [0, 0, 0, 1, 0, 1],
                "_E": [1, 0, 0, 1, 0, 1],
                "_F": [0, 1, 0, 1, 0, 1],
                "_G": [1, 1, 0, 1, 0, 1],
                "_H": [0, 0, 1, 1, 0, 1],
                "_I": [1, 0, 1, 1, 0, 1],
                "_J": [0, 1, 1, 1, 0, 1],
                "_K": [1, 1, 1, 1, 0, 1],
                "_L": [0, 0, 0, 0, 1, 1],
                "_M": [1, 0, 0, 0, 1, 1],
                "_N": [0, 1, 0, 0, 1, 1],
                "_O": [1, 1, 0, 0, 1, 1],
                "_P": [0, 0, 1, 0, 1, 1],
                "_Q": [1, 0, 1, 0, 1, 1],
                "_R": [0, 1, 1, 0, 1, 1],
                "_S": [1, 1, 1, 0, 1, 1],
                "_T": [0, 0, 0, 1, 1, 1],
                "_U": [1, 0, 0, 1, 1, 1],
                "_V": [0, 1, 0, 1, 1, 1],
                "_W": [1, 1, 0, 1, 1, 1],
                "_X": [0, 0, 1, 1, 1, 1],
                "_Y": [1, 0, 1, 1, 1, 1],
                "_Z": [0, 1, 1, 1, 1, 1]}

    # Convert the text to all upper case. We need to split it into chunks of 4 while replacing spaces with an indicator
    # that a space needs to be placed here instead. chunk_count is used to keep track if we need to start a new chunk
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
            # We have a full chunk, add it to the four_chunk list and reset chunk_count
            four_chunks.append(new_chunk)
            new_chunk = ""
            chunk_count = 0

    # If we have finished processing all characters in the text we need to ensure we capture any stragglers that might
    # not have completed a full chunk
    if new_chunk != "":
        four_chunks.append(new_chunk)

    # At this point we should have chunks of four characters each (except the last one)
    print(four_chunks)

    # Left letter tracks whether our next letter should be a left or right
    left_letter = True
    # hexes holds the encoded hexes as we build it
    hexes = list[list[int]]
    for chunk in four_chunks:
        for character in chunk:
            pass


text = input("Enter text to encode: ")

print(encoder(text))
