from hexClass import *
from tkinter import *
import functools

class EncodingError(Exception):
    pass

def encoder(text: str, canvas: Canvas, size: int) -> list[list[str]]:
    """
    Takes the text input and encodes it into the line lists
    :param text: The text input
    :return: The list of triangles and what lines to draw for them
    """
    # Switched to one deep list as the two deep list was unnecessarily complicated
    alphabet = {"1": ["1", "0", "0", "0", "0", "0"],
                "2": ["0", "1", "0", "0", "0", "0"],
                "3": ["1", "1", "0", "0", "0", "0"],
                "4": ["0", "0", "1", "0", "0", "0"],
                "5": ["1", "0", "1", "0", "0", "0"],
                "6": ["0", "1", "1", "0", "0", "0"],
                "7": ["1", "1", "1", "0", "0", "0"],
                "8": ["0", "0", "0", "1", "0", "0"],
                "9": ["1", "0", "0", "1", "0", "0"],
                "0": ["0", "1", "0", "1", "0", "0"],
                "A_": ["1", "1", "0", "1", "0", "0"],
                "B_": ["0", "0", "1", "1", "0", "0"],
                "C_": ["1", "0", "1", "1", "0", "0"],
                "D_": ["0", "1", "1", "1", "0", "0"],
                "E_": ["1", "1", "1", "1", "0", "0"],
                "F_": ["0", "0", "0", "0", "1", "0"],
                "G_": ["1", "0", "0", "0", "1", "0"],
                "H_": ["0", "1", "0", "0", "1", "0"],
                "I_": ["1", "1", "0", "0", "1", "0"],
                "J_": ["0", "0", "1", "0", "1", "0"],
                "K_": ["1", "0", "1", "0", "1", "0"],
                "L_": ["0", "1", "1", "0", "1", "0"],
                "M_": ["1", "1", "1", "0", "1", "0"],
                "N_": ["0", "0", "0", "1", "1", "0"],
                "O_": ["1", "0", "0", "1", "1", "0"],
                "P_": ["0", "1", "0", "1", "1", "0"],
                "Q_": ["1", "1", "0", "1", "1", "0"],
                "R_": ["0", "0", "1", "1", "1", "0"],
                "S_": ["1", "0", "1", "1", "1", "0"],
                "T_": ["0", "1", "1", "1", "1", "0"],
                "U_": ["1", "1", "1", "1", "1", "0"],
                "V_": ["0", "0", "0", "0", "0", "1"],
                "W_": ["1", "0", "0", "0", "0", "1"],
                "X_": ["0", "1", "0", "0", "0", "1"],
                "Y_": ["1", "1", "0", "0", "0", "1"],
                "Z_": ["0", "0", "1", "0", "0", "1"],
                "_A": ["1", "0", "1", "0", "0", "1"],
                "_B": ["0", "1", "1", "0", "0", "1"],
                "_C": ["1", "1", "1", "0", "0", "1"],
                "_D": ["0", "0", "0", "1", "0", "1"],
                "_E": ["1", "0", "0", "1", "0", "1"],
                "_F": ["0", "1", "0", "1", "0", "1"],
                "_G": ["1", "1", "0", "1", "0", "1"],
                "_H": ["0", "0", "1", "1", "0", "1"],
                "_I": ["1", "0", "1", "1", "0", "1"],
                "_J": ["0", "1", "1", "1", "0", "1"],
                "_K": ["1", "1", "1", "1", "0", "1"],
                "_L": ["0", "0", "0", "0", "1", "1"],
                "_M": ["1", "0", "0", "0", "1", "1"],
                "_N": ["0", "1", "0", "0", "1", "1"],
                "_O": ["1", "1", "0", "0", "1", "1"],
                "_P": ["0", "0", "1", "0", "1", "1"],
                "_Q": ["1", "0", "1", "0", "1", "1"],
                "_R": ["0", "1", "1", "0", "1", "1"],
                "_S": ["1", "1", "1", "0", "1", "1"],
                "_T": ["0", "0", "0", "1", "1", "1"],
                "_U": ["1", "0", "0", "1", "1", "1"],
                "_V": ["0", "1", "0", "1", "1", "1"],
                "_W": ["1", "1", "0", "1", "1", "1"],
                "_X": ["0", "0", "1", "1", "1", "1"],
                "_Y": ["1", "0", "1", "1", "1", "1"],
                "_Z": ["0", "1", "1", "1", "1", "1"],
                ".": [".", ".", ".", ".", ".", "."]}

    # Clear the Canvas of previous hexagrams
    canvas.delete("all")

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
            elif character in "123456890.":
                # If the character is a number or period then we dont need to add a left right indicator or alternate
                # the tracker
                letter = character
            elif character.isalpha():
                # Determine where left right indicator is needed based on left_letter tracker
                letter = character + "_" if left_letter else "_" + character
                # Alternate the left_letter tracker
                left_letter = not left_letter
            else:
                # This must be a special character and is not encoded, stop processing and fail gracefully
                position = text.find(character)
                raise EncodingError(f"Unknown character encountered: {character} at position {str(position)} in input")

            # Get the encoding for each letter, then append the encoding to the new_hex
            encoding = alphabet.get(letter)
            for triangle in range(0,6):
                new_hex[triangle] = new_hex[triangle] + encoding[triangle]

        # add the new hex to the existing ones
        hexes.append(new_hex)

    for hex in hexes:
        Hexagram(hex, canvas_sz=size, canvas=canvas)


################ Start of script ################
# text = input("Enter text to encode: ")
# try:
#     encoded_text = encoder(text)
# except EncodingError as e:
#     print(e)
#     exit()
#
# print(encoded_text)

# Create the parent frame
window = Tk()

window.title("HexWriter")
window.geometry("1000x1050")
window.resizable(False, False)

# Create an encoding frame
encoder_frame = Frame(window)
encoder_frame.pack(padx=10, pady=10, fill='x', expand=True)

# Create a text box for user to enter text
entry_text = StringVar()

entry_label = Label(encoder_frame, text="Enter text to encode:")
entry_label.pack(fill='x', expand=True)

canvas_size = 1000
canvas = Canvas(window, width=canvas_size, height=canvas_size, bg="white")

entry_box = Entry(encoder_frame, textvariable=entry_text)
entry_box.bind('<Return>', functools.partial(encoder, text=entry_text.get(), canvas=canvas, size=canvas_size))
entry_box.pack(fill='x', expand=True)
entry_box.focus_set()

canvas.pack()

# lines = "triangle 1 lines", "triangle 2 lines","triangle 3 lines", ...
# all_lines = ["1111", "1111", "1111", "1111", "1111", "1111"]    # Dummy lines
# encoded_text = [all_lines,]
# new_hex1 = Hexagram(encoded_text[0], canvas_size, canvas)

window.mainloop()
