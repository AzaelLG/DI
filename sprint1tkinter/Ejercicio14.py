import tkinter as tk
from tkinter import messagebox

class RegistroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ejercicio 14")

        barramenu = tk.Menu(self.root)
        self.root.config(menu=barramenu)

        menu = tk.Menu(barramenu, tearoff=0)
        barramenu.add_cascade(label="Archivo", menu=menu)
        menu.add_command(label="Guardar Lista", command=self.guardar_lista)
        menu.add_command(label="Cargar Lista", command=self.cargar_lista)

        frame_datos = tk.Frame(root)
        frame_datos.pack(pady=10)

        tk.Label(frame_datos, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nombre = tk.Entry(frame_datos, width=30)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_datos, text="Edad:").grid(row=1, column=0, padx=5, pady=5)
        self.scale_edad = tk.Scale(frame_datos, from_=0, to=100, orient=tk.HORIZONTAL, command=self.actualizar_edad)
        self.scale_edad.grid(row=1, column=1, padx=5, pady=5)
        self.label_edad_valor = tk.Label(frame_datos, text="0 años")
        self.label_edad_valor.grid(row=1, column=2, padx=5, pady=5)

        tk.Label(frame_datos, text="Género:").grid(row=2, column=0, padx=5, pady=5)
        self.var_genero = tk.StringVar(value="Masculino")

        frame_genero = tk.Frame(frame_datos)
        frame_genero.grid(row=2, column=1)

        tk.Radiobutton(frame_genero, text="Masculino", variable=self.var_genero, value="Masculino").pack(side=tk.LEFT)
        tk.Radiobutton(frame_genero, text="Femenino", variable=self.var_genero, value="Femenino").pack(side=tk.LEFT)
        tk.Radiobutton(frame_genero, text="Otro", variable=self.var_genero, value="Otro").pack(side=tk.LEFT)

        tk.Button(frame_datos, text="Añadir", command=self.añadir_usuario).grid(row=3, column=0, columnspan=3, pady=10)

        frame_lista = tk.Frame(root)
        frame_lista.pack(pady=10)

        tk.Label(frame_lista, text="Usuarios Registrados:").pack()

        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(frame_lista, width=50, height=10, yscrollcommand=scrollbar.set)  # ← Añade self.
        self.listbox.pack(side=tk.LEFT)

        scrollbar.config(command=self.listbox.yview)

        frame_botones = tk.Frame(root)
        frame_botones.pack(pady=10)

        tk.Button(frame_botones, text="Eliminar", command=self.eliminar_usuario).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="Salir", command=self.salir).pack(side=tk.LEFT, padx=5)

    def añadir_usuario(self):
        nombre = self.entry_nombre.get()
        edad = self.scale_edad.get()
        genero = self.var_genero.get()

        if nombre == "":
            messagebox.showwarning("Advertencia", "Introduce un nombre")
            return

        usuario = nombre + " - " + str(edad) + " años - " + genero
        self.listbox.insert(tk.END, usuario)

        self.entry_nombre.delete(0, tk.END)
        self.scale_edad.set(0)

    def eliminar_usuario(self):
        seleccion = self.listbox.curselection()
        if seleccion:
            self.listbox.delete(seleccion)

    def salir(self):
        self.root.quit()

    def actualizar_edad(self, valor):
        self.label_edad_valor.config(text=valor + " años")

    def guardar_lista(self):
        messagebox.showinfo("Guardar", "Lista guardada correctamente")

    def cargar_lista(self):
        messagebox.showinfo("Cargar", "Lista cargada correctamente")

root = tk.Tk()
app = RegistroApp(root)
root.mainloop()