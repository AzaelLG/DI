import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Registro de Usuarios")
root.geometry("500x500")


def actualizar_edad(valor):
    label_edad_valor.config(text=valor + " años")


def añadir_usuario():
    nombre = entry_nombre.get()
    edad = scale_edad.get()
    genero = var_genero.get()

    if nombre == "":
        messagebox.showwarning("Advertencia", "Introduce un nombre")
        return

    usuario = nombre + " - " + str(edad) + " años - " + genero
    listbox.insert(tk.END, usuario)

    entry_nombre.delete(0, tk.END)
    scale_edad.set(0)


def eliminar_usuario():
    seleccion = listbox.curselection()
    listbox.delete(seleccion)



def salir():
    root.quit()


def guardar_lista():
    messagebox.showinfo("Guardar", "Lista guardada correctamente")


def cargar_lista():
    messagebox.showinfo("Cargar", "Lista cargada correctamente")


# Menú
barra_menu = tk.Menu(root)
root.config(menu=barra_menu)

menu = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Archivo", menu=menu)
menu.add_command(label="Guardar Lista", command=guardar_lista)
menu.add_command(label="Cargar Lista", command=cargar_lista)

frame_datos = tk.Frame(root)
frame_datos.pack(pady=10)

tk.Label(frame_datos, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
entry_nombre = tk.Entry(frame_datos, width=30)
entry_nombre.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_datos, text="Edad:").grid(row=1, column=0, padx=5, pady=5)
scale_edad = tk.Scale(frame_datos, from_=0, to=100, orient=tk.HORIZONTAL, command=actualizar_edad)
scale_edad.grid(row=1, column=1, padx=5, pady=5)
label_edad_valor = tk.Label(frame_datos, text="0 años")
label_edad_valor.grid(row=1, column=2, padx=5, pady=5)

tk.Label(frame_datos, text="Género:").grid(row=2, column=0, padx=5, pady=5)
var_genero = tk.StringVar(value="Masculino")

frame_genero = tk.Frame(frame_datos)
frame_genero.grid(row=2, column=1,)

tk.Radiobutton(frame_genero, text="Masculino", variable=var_genero, value="Masculino").pack(side=tk.LEFT)
tk.Radiobutton(frame_genero, text="Femenino", variable=var_genero, value="Femenino").pack(side=tk.LEFT)
tk.Radiobutton(frame_genero, text="Otro", variable=var_genero, value="Otro").pack(side=tk.LEFT)

tk.Button(frame_datos, text="Añadir", command=añadir_usuario).grid(row=3, column=0,columnspan=3, pady=10)

frame_lista = tk.Frame(root)
frame_lista.pack(pady=10)

tk.Label(frame_lista, text="Usuarios Registrados:").pack()

scrollbar = tk.Scrollbar(frame_lista)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(frame_lista, width=50, height=10, yscrollcommand=scrollbar.set)
listbox.pack(side=tk.LEFT)

scrollbar.config(command=listbox.yview)


frame_botones = tk.Frame(root)
frame_botones.pack(pady=10)

tk.Button(frame_botones, text="Eliminar", command=eliminar_usuario).pack(side=tk.LEFT, padx=5)
tk.Button(frame_botones, text="Salir", command=salir).pack(side=tk.LEFT, padx=5)

root.mainloop()