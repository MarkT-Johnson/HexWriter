from hexClass import *
from tkinter import *

class EncodingError(Exception):
    pass

def encoder(text: str) -> list[list[str]]:
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
                ".": ["0", "0", "0", "0", "0", "0"]}

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
                # If the character is a number or period then we dont need to add a left right indicator or
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
                raise EncodingError(f"Unknown character encountered: \"{character}\" at position {str(position)} in input")

            # Get the encoding for each letter, then append the encoding to the new_hex
            encoding = alphabet.get(letter)
            for triangle in range(0,6):
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
    message = "This is a default messsage, if you are seeing this then something has gone wrong. Sorry! ¯\_(ツ)_/¯"
    try:
        # Clear the canvas before updating
        canvas.delete("all")
        # Get the text from the entry widget
        text = entry.get()

        # Encode the new text
        encoded_text = encoder(text)
        # Draw the hexagram on the canvas
        hex_num = 1
        if len(encoded_text) <= 7:
            for hex in encoded_text:
                Hexagram(hex, hex_num, canvas_size, canvas)
                hex_num += 1
            message = str(encoded_text)
        else:
            length_err = "Message too long. Limited to 28 letters, numbers, and periods total. Spaces are not counted in this total."
            print(length_err)
            message = length_err

    except EncodingError as e:
        message = f"There was an encoding error, please only use english letters ([a-Z]), numbers ([0-9]), periods (.), " \
                  f"or spaces ( ).\n{e}"

    finally:
        text_output['state'] = "normal"
        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, message)
        text_output['state'] = "disabled"

################ Start of script ################
# Create the parent frame
window = Tk()

window.title("HexWriter")
window.geometry("1000x1050")
window.resizable(False, False)

# Create an encoding frame
# encoder_frame = Frame(window)
# encoder_frame.pack(padx=10, pady=10, fill='x', expand=True)

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
canvas = Canvas(window, width=canvas_size, height=canvas_size, bg="white")

canvas.pack()

window.mainloop()
