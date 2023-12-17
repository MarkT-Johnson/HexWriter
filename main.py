from hexClass import *
from tkinter import *

window = Tk()

window.title("HexWriter")
window.geometry("1000x1000")

canvas_size = 1000
canvas = Canvas(window, width=canvas_size, height=canvas_size, bg="white")
canvas.pack()

origin = [canvas_size/2, canvas_size/2]
lines = [[1, 2, 3, 4], [1, 2, 3, 4]]

new_hex = Hexagram(origin, lines, canvas_size, canvas)

window.mainloop()
