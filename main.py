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

lines = [[1, 2, 3, 4], [1, 2, 3, 4]]    # Dummy time

new_hex1 = Hexagram(origin1, lines, canvas_size, canvas)
new_hex2 = Hexagram(origin2, lines, canvas_size)

window.mainloop()
