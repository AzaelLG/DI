import tkinter as tk

root = tk.Tk()
root.title("Ejercicio 8")

def mostrar():
    nombre = entrada_nombre.get()
    apellido = entrada_apellido.get()
    etiqueta_resultado.config(text=nombre + " " + apellido)

def borrar():
    entrada_nombre.delete(0, tk.END)
    entrada_apellido.delete(0, tk.END)
    etiqueta_resultado.config(text="")


frame1 = tk.Frame(root, bg="lightblue")
frame1.pack(pady=10)

tk.Label(frame1, text="Nombre:", bg="lightblue").grid(row=0, column=0, padx=5, pady=5)
entrada_nombre = tk.Entry(frame1)
entrada_nombre.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame1, text="Apellido:", bg="lightblue").grid(row=1, column=0, padx=5, pady=5)
entrada_apellido = tk.Entry(frame1)
entrada_apellido.grid(row=1, column=1, padx=5, pady=5)


frame2 = tk.Frame(root, bg="lightgray")
frame2.pack(pady=10)

etiqueta_resultado = tk.Label(frame2, text="", bg="white", width=30)
etiqueta_resultado.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

tk.Button(frame2, text="Mostrar", command=mostrar).grid(row=1, column=0, padx=5, pady=5)
tk.Button(frame2, text="Borrar", command=borrar).grid(row=1, column=1, padx=5, pady=5)

root.mainloop()
