import tkinter

import customtkinter as ctk


class AddUserView:
    def __init__(self, master, avatar_names):
        self.window = ctk.CTkToplevel(master)
        self.window.title("Añadir Nuevo Usuario")
        self.window.geometry("350x400")
        self.window.grab_set()  # ¡Esto la hace modal!

        self.frame = ctk.CTkFrame(self.window)
        self.frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Widgets del formulario
        ctk.CTkLabel(self.frame, text="Nombre:").pack(pady=(10, 0))
        self.nombre_entry = ctk.CTkEntry(self.frame)
        self.nombre_entry.pack(fill="x", padx=10)

        ctk.CTkLabel(self.frame, text="Edad:").pack(pady=(10, 0))
        self.edad_entry = ctk.CTkEntry(self.frame)
        self.edad_entry.pack(fill="x", padx=10)

        ctk.CTkLabel(self.frame, text="Género:").pack(pady=(10, 0))
        self.genero_var = ctk.StringVar(value="No especificado")
        self.genero_optionmenu = ctk.CTkOptionMenu(self.frame,
                                                   values=["Masculino", "Femenino", "No especificado"],
                                                   variable=self.genero_var)
        self.genero_optionmenu.pack(fill="x", padx=10)

        ctk.CTkLabel(self.frame, text="Avatar:").pack(pady=(10, 0))
        self.avatar_var = ctk.StringVar(value=avatar_names[0] if avatar_names else "")
        self.avatar_optionmenu = ctk.CTkOptionMenu(self.frame,
                                                   values=avatar_names,
                                                   variable=self.avatar_var)
        self.avatar_optionmenu.pack(fill="x", padx=10)

        # El botón de guardar será configurado por el controlador
        self.guardar_button = ctk.CTkButton(self.frame, text="Guardar")
        self.guardar_button.pack(pady=20)

    def get_data(self):
        """Recoge los datos del formulario y los devuelve como diccionario."""
        return {
            "nombre": self.nombre_entry.get(),
            "edad": self.edad_entry.get(),
            "genero": self.genero_var.get(),
            "avatar": self.avatar_var.get()
        }

class MainView:
    def __init__(self, master):
        self.master = master
        self.frame = ctk.CTkFrame(master)
        self.frame.pack(fill="both", expand=True)

        # Configuración de grid: 2 columnas, pesos 1 y 3.
        self.frame.grid_columnconfigure(0, weight=1)  # Columna lista
        self.frame.grid_columnconfigure(1, weight=3)  # Columna detalles
        self.frame.grid_rowconfigure(0, weight=1) # Fila principal

        self._crear_widgets_lista()
        self._crear_widgets_detalles()
        self.crear_menu_bar()

    def _crear_widgets_lista(self):
        """Crea el frame para la lista de usuarios a la izquierda."""
        self.lista_frame = ctk.CTkFrame(self.frame)
        self.lista_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.lista_frame, text="Usuarios",
                     font=ctk.CTkFont(weight="bold")).pack(pady=5)

        # Frame desplazable para la lista de botones
        self.lista_usuarios_scrollable = ctk.CTkScrollableFrame(self.lista_frame)
        self.lista_usuarios_scrollable.pack(fill="both", expand=True, padx=5, pady=5)

    def _crear_widgets_detalles(self):
        """Crea el frame y etiquetas para los detalles del usuario a la derecha."""
        self.detalles_frame = ctk.CTkFrame(self.frame)
        self.detalles_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.detalles_frame, text="Detalles del Usuario",
                     font=ctk.CTkFont(weight="bold", size=16)).pack(pady=10)

        # Widgets de visualización (serán actualizados por el controlador)
        self.nombre_label = ctk.CTkLabel(self.detalles_frame, text="Nombre: ")
        self.nombre_label.pack(pady=5)
        self.edad_label = ctk.CTkLabel(self.detalles_frame, text="Edad: ")
        self.edad_label.pack(pady=5)
        self.genero_label = ctk.CTkLabel(self.detalles_frame, text="Género: ")
        self.genero_label.pack(pady=5)

        # Etiqueta para el avatar
        self.avatar_label = ctk.CTkLabel(self.detalles_frame, text="", width=150, height=150)
        self.avatar_label.pack(pady=20)
        self.avatar_label.configure(image=None) # Inicializar sin imagen

    def actualizar_lista_usuarios(self, usuarios, on_seleccionar_callback):
        """
        Recibe la lista de usuarios y el callback del controlador.
        Dibuja los botones para cada usuario.
        """
        # Eliminar widgets anteriores
        for widget in self.lista_usuarios_scrollable.winfo_children():
            widget.destroy()

        # Crear un botón por usuario
        for i, usuario in enumerate(usuarios):
            btn = ctk.CTkButton(
                self.lista_usuarios_scrollable,
                text=usuario.nombre,
                # Usar lambda para pasar el índice al callback del controlador
                command=lambda idx=i: on_seleccionar_callback(idx)
            )
            btn.pack(fill="x", padx=5, pady=2)

    def mostrar_detalles_usuario(self, usuario, avatar_image):
        """Actualiza las etiquetas con los datos del usuario seleccionado."""
        if usuario:
            self.nombre_label.configure(text=f"Nombre: {usuario.nombre}")
            self.edad_label.configure(text=f"Edad: {usuario.edad}")
            self.genero_label.configure(text=f"Género: {usuario.genero}")

            # Actualizar imagen (si existe)
            if avatar_image:
                self.avatar_label.configure(image=avatar_image, text="")
            else:
                self.avatar_label.configure(image=None, text="Sin Avatar")
        else:
            # Limpiar detalles si no hay usuario (ej. lista vacía)
            self.nombre_label.configure(text="Nombre:")
            self.edad_label.configure(text="Edad:")
            self.genero_label.configure(text="Género:")
            self.avatar_label.configure(image=None, text="")

    def _crear_widgets_lista(self):
        """Crea el frame para la lista de usuarios y el botón de añadir."""
        # ... (Frame y Label igual)

        # Botón para abrir la ventana modal
        self.add_button = ctk.CTkButton(self.lista_frame, text="➕ Añadir Usuario")
        self.add_button.pack(fill="x", padx=5, pady=(5, 10))

    def _crear_menu_bar(self):
        """Crea la barra de menú, exponiendo los menús al controlador."""
        self.menubar = tkinter.Menu(self.master)
        self.master.config(menu=self.menubar)

        # Menú Archivo
        self.menu_archivo = tkinter.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Archivo", menu=self.menu_archivo)


