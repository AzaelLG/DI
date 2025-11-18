import customtkinter as ctk

import tkinter  # Necesario para tkinter.Menu y BooleanVar


# --- VENTANA MODAL PARA AÑADIR USUARIO (AddUserView) ---
class AddUserView:
    def __init__(self, master, avatar_names):
        self.window = ctk.CTkToplevel(master)
        self.window.title("Añadir Nuevo Usuario")
        self.window.geometry("350x400")
        self.window.grab_set()
        self.window.resizable(False, False)

        self.frame = ctk.CTkFrame(self.window)
        self.frame.pack(padx=20, pady=20, fill="both", expand=True)

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
                                                   values=["avatar1.png","avatar2.png"],
                                                   variable=self.avatar_var)
        self.avatar_optionmenu.pack(fill="x", padx=10)

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


# --- VENTANA MODAL PARA EDITAR USUARIO (EditUserView) ---
class EditUserView:
    def __init__(self, master, avatar_names):
        self.window = ctk.CTkToplevel(master)
        self.window.title("Editar Usuario")
        self.window.geometry("350x400")
        self.window.grab_set()
        self.window.resizable(False, False)

        self.frame = ctk.CTkFrame(self.window)
        self.frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(self.frame, text="Nombre:").pack(pady=(10, 0))
        self.nombre_entry = ctk.CTkEntry(self.frame)
        self.nombre_entry.pack(fill="x", padx=10)

        ctk.CTkLabel(self.frame, text="Edad:").pack(pady=(10, 0))
        self.edad_entry = ctk.CTkEntry(self.frame)
        self.edad_entry.pack(fill="x", padx=10)

        ctk.CTkLabel(self.frame, text="Género:").pack(pady=(10, 0))
        self.genero_var = ctk.StringVar()
        self.genero_optionmenu = ctk.CTkOptionMenu(self.frame,
                                                   values=["Masculino", "Femenino", "No especificado"],
                                                   variable=self.genero_var)
        self.genero_optionmenu.pack(fill="x", padx=10)

        ctk.CTkLabel(self.frame, text="Avatar:").pack(pady=(10, 0))
        self.avatar_var = ctk.StringVar()
        self.avatar_optionmenu = ctk.CTkOptionMenu(self.frame,
                                                   values=["avatar1.png","avatar2.png"],
                                                   variable=self.avatar_var)
        self.avatar_optionmenu.pack(fill="x", padx=10)

        self.guardar_button = ctk.CTkButton(self.frame, text="Guardar Cambios")
        self.guardar_button.pack(pady=20)

    def set_data(self, usuario):
        """Pre-carga los datos del usuario a editar."""
        self.nombre_entry.insert(0, usuario.nombre)
        self.edad_entry.insert(0, str(usuario.edad))
        self.genero_var.set(usuario.genero)
        self.avatar_var.set(usuario.avatar)

    def get_data(self):
        """Recoge los datos del formulario y los devuelve como diccionario."""
        return {
            "nombre": self.nombre_entry.get(),
            "edad": self.edad_entry.get(),
            "genero": self.genero_var.get(),
            "avatar": self.avatar_var.get()
        }


# --- VISTA PRINCIPAL (MainView) ---
class MainView:
    def __init__(self, master):
        self.master = master
        self.frame = ctk.CTkFrame(master)
        self.frame.pack(fill="both", expand=True)

        # Configuración de grid
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=3)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=0)

        self._crear_widgets_lista()
        self._crear_widgets_detalles()
        self._crear_menu_bar()
        self._crear_barra_estado()

        # --- Creación de Widgets ---

    def _crear_widgets_lista(self):
        """Crea el frame para la lista de usuarios y el botón de añadir."""
        self.lista_frame = ctk.CTkFrame(self.frame)
        self.lista_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.lista_frame, text="Usuarios",
                     font=ctk.CTkFont(weight="bold")).pack(pady=5)

        self.add_button = ctk.CTkButton(self.lista_frame, text="➕ Añadir Usuario")
        self.add_button.pack(fill="x", padx=5, pady=(5, 10))

        # Widgets de Búsqueda/Filtro
        self.busqueda_var = ctk.StringVar()
        self.busqueda_entry = ctk.CTkEntry(self.lista_frame, placeholder_text="Buscar por nombre",
                                           textvariable=self.busqueda_var)
        self.busqueda_entry.pack(fill="x", padx=5, pady=5)

        self.genero_filtro_var = ctk.StringVar(value="Todos")
        self.genero_filtro_menu = ctk.CTkOptionMenu(self.lista_frame,
                                                    values=["Todos", "Masculino", "Femenino", "No especificado"],
                                                    variable=self.genero_filtro_var)
        self.genero_filtro_menu.pack(fill="x", padx=5, pady=5)

        self.lista_usuarios_scrollable = ctk.CTkScrollableFrame(self.lista_frame)
        self.lista_usuarios_scrollable.pack(fill="both", expand=True, padx=5, pady=5)

    def _crear_widgets_detalles(self):
        """Crea el frame, etiquetas y botones para los detalles del usuario a la derecha."""
        self.detalles_frame = ctk.CTkFrame(self.frame)
        self.detalles_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.detalles_frame, text="Detalles del Usuario",
                     font=ctk.CTkFont(weight="bold", size=16)).pack(pady=10)

        self.nombre_label = ctk.CTkLabel(self.detalles_frame, text="Nombre: ")
        self.nombre_label.pack(pady=5)
        self.edad_label = ctk.CTkLabel(self.detalles_frame, text="Edad: ")
        self.edad_label.pack(pady=5)
        self.genero_label = ctk.CTkLabel(self.detalles_frame, text="Género: ")
        self.genero_label.pack(pady=5)

        self.avatar_label = ctk.CTkLabel(self.detalles_frame, text="", width=150, height=150)
        self.avatar_label.pack(pady=20)

        self.edit_button = ctk.CTkButton(self.detalles_frame, text="✏️ Editar", state="disabled")
        self.edit_button.pack(pady=(10, 5))
        self.delete_button = ctk.CTkButton(self.detalles_frame, text="🗑️ Eliminar", fg_color="red", state="disabled")
        self.delete_button.pack(pady=(0, 10))

    def _crear_menu_bar(self):
        """Crea la barra de menú."""
        self.menubar = tkinter.Menu(self.master)
        self.master.config(menu=self.menubar)

        self.menu_archivo = tkinter.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Archivo", menu=self.menu_archivo)

        # Menú Opciones (NUEVO para el Checkbutton de auto-guardado)
        self.menu_opciones = tkinter.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Opciones", menu=self.menu_opciones)

    def _crear_barra_estado(self):
        """Crea la barra de estado en la parte inferior."""
        self.estado_label = ctk.CTkLabel(self.frame, text="Estado: Listo", anchor="w",
                                         fg_color="transparent", text_color="gray")
        self.estado_label.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 5))

    # --- Métodos de Actualización ---
    def set_estado(self, mensaje):
        """Actualiza el mensaje de la barra de estado."""
        self.estado_label.configure(text=f"Estado: {mensaje}")

    def actualizar_lista_usuarios(self, usuarios, on_seleccionar_callback, on_doble_clic_callback):
        """
        Dibuja los botones y configura el doble clic para edición.
        """
        for widget in self.lista_usuarios_scrollable.winfo_children():
            widget.destroy()

        for i, usuario in enumerate(usuarios):
            btn = ctk.CTkButton(
                self.lista_usuarios_scrollable,
                text=usuario.nombre,
                command=lambda idx=i: on_seleccionar_callback(idx)
            )
            btn.pack(fill="x", padx=5, pady=2)
            btn.bind("<Double-Button-1>", lambda event, u=usuario: on_doble_clic_callback(u.nombre))

    def mostrar_detalles_usuario(self, usuario, avatar_image):
        """Actualiza las etiquetas con los datos del usuario seleccionado."""
        if usuario:
            self.nombre_label.configure(text=f"Nombre: {usuario.nombre}")
            self.edad_label.configure(text=f"Edad: {usuario.edad}")
            self.genero_label.configure(text=f"Género: {usuario.genero}")

            if avatar_image:
                self.avatar_label.configure(image=avatar_image, text="")
            else:
                self.avatar_label.configure(image=None, text="Sin Avatar")

            self.edit_button.configure(state="normal")
            self.delete_button.configure(state="normal")
        else:
            self.nombre_label.configure(text="Nombre:")
            self.edad_label.configure(text="Edad:")
            self.genero_label.configure(text="Género:")
            self.avatar_label.configure(image=None, text="")

            self.edit_button.configure(state="disabled")
            self.delete_button.configure(state="disabled")