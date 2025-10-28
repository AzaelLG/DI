import tkinter as tk




def obtener_texto():
    texto = entrada.get()
    etiqueta1.configure(text="Bienvenido "+ texto)

root = tk.Tk()
root.title("Ejercicio 3")
root.geometry("400x300")

etiqueta = tk.Label(root, text="Introduce tu nombre:")
etiqueta.pack(pady=10)

entrada = tk.Entry(root,width=40)
entrada.pack(pady=10)

boton = tk.Button(root,command=obtener_texto,text="Registrar nombre")
boton.pack(pady=10)

etiqueta1 = tk.Label(root, text="")
etiqueta1.pack(pady=10)

root.mainloop()

