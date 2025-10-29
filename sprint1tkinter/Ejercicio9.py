import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Ejercicio9")
root.geometry("400x300")

def abrir():
    messagebox.showinfo("Abrir", "Función Abrir seleccionada")

def salir():
    root.quit()

def acerca_de():
    messagebox.showinfo("Acerca de", "Aplicación creada con Tkinter")


barra_menu = tk.Menu(root)
root.config(menu=barra_menu)


menu_archivo = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Archivo", menu=menu_archivo)
menu_archivo.add_command(label="Abrir", command=abrir)
menu_archivo.add_command(label="Salir", command=salir)


menu_ayuda = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)
menu_ayuda.add_command(label="Acerca de", command=acerca_de)

root.mainloop()