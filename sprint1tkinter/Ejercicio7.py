import tkinter as tk

root = tk.Tk()
root.title("Dibujar Figuras")

def dibujar_rectangulo():
    x1 = int(entry_x1_rect.get())
    y1 = int(entry_y1_rect.get())
    x2 = int(entry_x2_rect.get())
    y2 = int(entry_y2_rect.get())
    canvas.create_rectangle(x1, y1, x2, y2)

def dibujar_circulo():
    x1 = int(entry_x1_circ.get())
    y1 = int(entry_y1_circ.get())
    x2 = int(entry_x2_circ.get())
    y2 = int(entry_y2_circ.get())
    canvas.create_oval(x1, y1, x2, y2)


tk.Label(root, text="Rectángulo - x1:").pack()
entry_x1_rect = tk.Entry(root)
entry_x1_rect.pack()

tk.Label(root, text="y1:").pack()
entry_y1_rect = tk.Entry(root)
entry_y1_rect.pack()

tk.Label(root, text="x2:").pack()
entry_x2_rect = tk.Entry(root)
entry_x2_rect.pack()

tk.Label(root, text="y2:").pack()
entry_y2_rect = tk.Entry(root)
entry_y2_rect.pack()

tk.Button(root, text="Dibujar Rectángulo", command=dibujar_rectangulo).pack()


tk.Label(root, text="Círculo - x1:").pack()
entry_x1_circ = tk.Entry(root)
entry_x1_circ.pack()

tk.Label(root, text="y1:").pack()
entry_y1_circ = tk.Entry(root)
entry_y1_circ.pack()

tk.Label(root, text="x2:").pack()
entry_x2_circ = tk.Entry(root)
entry_x2_circ.pack()

tk.Label(root, text="y2:").pack()
entry_y2_circ = tk.Entry(root)
entry_y2_circ.pack()

tk.Button(root, text="Dibujar Círculo", command=dibujar_circulo).pack()

# Canvas
canvas = tk.Canvas(root, width=400, height=300, bg="white")
canvas.pack()

root.mainloop()