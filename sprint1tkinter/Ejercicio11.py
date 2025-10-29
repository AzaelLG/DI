import tkinter as tk

root = tk.Tk()
root.title("Ejercicio11")
root.geometry("400x300")

def actualizar(valor):
    etiqueta.config(text="Valor: " + valor)

etiqueta = tk.Label(root, text="Valor: 0")
etiqueta.pack(pady=20)

scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=actualizar)
scale.pack(pady=20)

root.mainloop()