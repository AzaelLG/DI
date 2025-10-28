import tkinter as tk

root = tk.Tk()
root.geometry("400x300")
root.title("Ejercicio 6")

def mostrar_seleccion():
    seleccion = listbox.curselection()
    elemento = listbox.get(seleccion)
    etiqueta.config(text="Tu fruta favorita es: "+elemento)

opciones= ["Manzana","Banana","Naranja"]

listbox = tk.Listbox(root,selectmode=tk.SINGLE)
for opcion in opciones:
    listbox.insert(tk.END,opcion)
listbox.pack(pady=10)

boton = tk.Button(root, text="Escoger opcion", command=mostrar_seleccion)
boton.pack(pady=10)

etiqueta = tk.Label(root, text="Escoge tu fruta:")
etiqueta.pack(pady=10)

root.mainloop()