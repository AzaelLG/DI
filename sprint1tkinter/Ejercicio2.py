import tkinter as tk

root = tk.Tk()
root.title("Ejercicio 2")
root.geometry("400x300")

def aparecer_texto():
    etiqueta1.config(text="Mensaje")

etiqueta1 = tk.Label(root, text="Mostrar mensaje")
boton = tk.Button(root, command=aparecer_texto,text="Cambiar texto")
boton2 = tk.Button(root,command=root.quit,text="Boton cerrar")
etiqueta1.pack(pady=10)
boton.pack(pady=10)
boton2.pack(pady=10)
root.mainloop()
