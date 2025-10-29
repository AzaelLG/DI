import tkinter as tk

root = tk.Tk()
root.title("Ejercicio 13")

def dibujar_circulo(event):
    x = event.x
    y = event.y
    canvas.create_oval(x, y, x+10, y+10)

def borrar(event):
    canvas.delete("all")

canvas = tk.Canvas(root, width=500, height=400)
canvas.pack()

canvas.bind("<Button-1>", dibujar_circulo)
root.bind("c", borrar)

root.mainloop()