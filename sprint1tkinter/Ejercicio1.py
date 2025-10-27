import tkinter as tk

root = tk.Tk()
root.title("Ejercicio1")
root.geometry("400x300")

def cambiar_texto():
    etiqueta3.config(text="Este texto a cambiado")

etiqueta1 = tk.Label(root, text="Bienvenido")
etiqueta2 = tk.Label(root, text="Azael López García")
etiqueta3 = tk.Label(root, text="Este texto va cambiar")
boton = tk.Button(root, text="Cambiar texto", command=cambiar_texto)

etiqueta1.pack(pady=10)
etiqueta2.pack(pady=10)
etiqueta3.pack(pady=10)
boton.pack(pady=10)

root.mainloop()

