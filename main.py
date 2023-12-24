from hexClass import *
from tkinter import *


#TODO Temporary Comment out while I figure out the encoding
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

text = input("Enter text to encode: ")

def encoder(input: str) -> list[list[int]]:
    """
    Takes the text input and encodes it into the line lists
    :param input: The text input
    :return: The list of triangles and what lines to draw for them
    """
    #"": [[],[],[],[],[],[]]
    alphabet = {"1": [[1],[],[],[],[],[]],
                "2": [[],[1],[],[],[],[]],
                "3": [[1],[1],[],[],[],[]],
                "4": [[],[],[1],[],[],[]],
                "5": [[1],[],[1],[],[],[]],
                "6": [[],[1],[1],[],[],[]],
                "7": [[1],[1],[1],[],[],[]],
                "8": [[],[],[],[1],[],[]],
                "9": [[1],[],[],[1],[],[]],
                "0": [[],[1],[],[1],[],[]],
                "A_": [[1],[1],[],[1],[],[]],
                "B_": [[],[],[1],[1],[],[]],
                "C_": [[1],[],[1],[1],[],[]],
                "D_": [[],[1],[1],[1],[],[]],
                "E_": [[1],[1],[1],[1],[],[]],
                "F_": [[],[],[],[],[1],[]],
                "G_": [[1],[],[],[],[1],[]],
                "H_": [[],[1],[],[],[1],[]],
                "I_": [[1],[1],[],[],[1],[]],
                "J_": [[],[],[1],[],[1],[]],
                "K_": [[1],[],[1],[],[1],[]],
                "L_": [[],[1],[1],[],[1],[]],
                "M_": [[1],[1],[1],[],[1],[]],
                "N_": [[],[],[],[1],[1],[]],
                "O_": [[1],[],[],[1],[1],[]],
                "P_": [[],[1],[],[1],[1],[]],
                "Q_": [[1],[1],[],[1],[1],[]],
                "R_": [[],[],[1],[1],[1],[]],
                "S_": [[1],[],[1],[1],[1],[]],
                "T_": [[],[1],[1],[1],[1],[]],
                "U_": [[1],[1],[1],[1],[1],[]],
                "V_": [[],[],[],[],[],[1]],
                "W_": [[1],[],[],[],[],[1]],
                "X_": [[],[1],[],[],[],[1]]}
