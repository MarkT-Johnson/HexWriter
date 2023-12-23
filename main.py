from hexClass import *
from tkinter import *

window = Tk()

window.title("HexWriter")
window.geometry("1000x1000")

canvas_size = 1000
canvas = Canvas(window, width=canvas_size, height=canvas_size, bg="white")
canvas.pack()

origin1 = [250, 750]
origin2 = [500, 500]

# lines = [[primary inner lines], [secondary inner lines],[primary outer lines], [secondary outer lines]]
all_lines = [[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]]    # Dummy lines

new_hex1 = Hexagram(all_lines, canvas_size, canvas)
new_hex2 = Hexagram(all_lines, canvas_size)

window.mainloop()
