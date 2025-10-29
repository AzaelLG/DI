import tkinter as tk

root = tk.Tk()
root.title("Ejercicio10")
root.geometry("500x400")


scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


texto = tk.Text(root, yscrollcommand=scrollbar.set)
texto.pack(side=tk.LEFT, fill=tk.Y)


scrollbar.config(command=texto.yview)


texto_largo = """Introducción a Python

Python es un lenguaje de programación de alto nivel, interpretado y de propósito general. 
Fue creado por Guido van Rossum y lanzado por primera vez en 1991.

Python se caracteriza por su sintaxis clara y legible, lo que lo convierte en un excelente 
lenguaje tanto para principiantes como para programadores experimentados.

Capítulo 2: Tkinter

Tkinter es la biblioteca estándar de Python para crear interfaces gráficas de usuario (GUI). 
Es una interfaz de Python para el toolkit Tk, que originalmente fue desarrollado para el 
lenguaje Tcl.

Con Tkinter puedes crear ventanas, botones, campos de texto, menús y muchos otros elementos 
de interfaz gráfica de manera relativamente sencilla.

Capítulo 3: Widgets básicos

Los widgets son los componentes básicos de una interfaz gráfica. En Tkinter tenemos:

- Label: para mostrar texto o imágenes
- Button: botones clickeables
- Entry: campos de entrada de una línea
- Text: campos de texto multilínea
- Frame: contenedores para organizar otros widgets
- Canvas: para dibujar formas y gráficos

Capítulo 4: Gestores de geometría

Tkinter ofrece tres gestores principales para posicionar widgets:

1. pack(): apila los widgets de forma automática
2. grid(): organiza los widgets en una cuadrícula
3. place(): permite posicionamiento absoluto

Cada uno tiene sus ventajas y se usa en diferentes situaciones.

Capítulo 5: Eventos y comandos

Los eventos son acciones del usuario como clicks, pulsaciones de teclas, etc.
En Tkinter, conectamos funciones a estos eventos mediante el parámetro command
o usando el método bind().

Esto permite que nuestra aplicación responda a las acciones del usuario de forma
interactiva y dinámica.

Fin del documento."""

texto.insert(tk.END, texto_largo)

root.mainloop()