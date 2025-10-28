import tkinter as tk

root = tk.Tk()
root.geometry("400x300")
root.title("Ejercicio 4")


def mostrar_seleccion():
    selecciones = []
    if var_check1.get():
        selecciones.append("Leer")
    if var_check2.get():
        selecciones.append("Música")
    if var_check3.get():
        selecciones.append("Deportes")

    if selecciones:
        etiqueta.config(text="Has seleccionado: " + ", ".join(selecciones))
    else:
        etiqueta.config(text="No has seleccionado ninguna afición")


etiqueta = tk.Label(root, text="Escoge tus hobbies:")
etiqueta.pack(pady=10)

var_check1 = tk.IntVar()
var_check2 = tk.IntVar()
var_check3 = tk.IntVar()

check1 = tk.Checkbutton(root, text="Leer", variable=var_check1, command=mostrar_seleccion)
check1.pack(pady=10)

check2 = tk.Checkbutton(root, text="Música", variable=var_check2, command=mostrar_seleccion)
check2.pack(pady=10)

check3 = tk.Checkbutton(root, text="Deportes", variable=var_check3, command=mostrar_seleccion)
check3.pack(pady=10)

root.mainloop()


root.mainloop()