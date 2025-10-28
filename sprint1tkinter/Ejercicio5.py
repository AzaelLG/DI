import tkinter as tk

from django.conf.locale import bg

root = tk.Tk()
root.geometry("400x300")
root.title("Ejercicio 5")

def mostrar_seleccion():
    seleccion = var_radio.get()
    if seleccion == "Rojo":
        root.config(bg="red")
    elif seleccion == "Verde":
        root.config(bg="green")
    else:
        root.config(bg="blue")
var_radio = tk.StringVar()
var_radio.set(0)

radio1 = tk.Radiobutton(root,text="Rojo", variable=var_radio, value="Rojo", command=mostrar_seleccion)
radio1.pack(pady=10)
radio2 = tk.Radiobutton(root,text="Verde", variable=var_radio, value="Verde", command=mostrar_seleccion)
radio2.pack(pady=10)
radio3 = tk.Radiobutton(root,text="Azul", variable=var_radio, value="Azul", command=mostrar_seleccion)
radio3.pack(pady=10)

root.mainloop()

