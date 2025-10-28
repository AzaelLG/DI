import tkinter as tk
root = tk.Tk()
root.geometry("400x300")
root.title("Ejercicio 7")

canvas = tk.Canvas(root, width=400, height=300, bg="white")
canvas.pack(pady=20)

canvas.create_oval(150,150,250,250,fill="black")
canvas.create_rectangle(50,50,250,150,fill="blue")

root.mainloop()