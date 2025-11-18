import customtkinter as ctk
from model.usuario_model import GestorUsuarios, Usuario
from view.main_view import MainView, AddUserView, EditUserView
from pathlib import Path
from PIL import Image  # ¡Importante! Requiere 'pip install Pillow'
import tkinter.messagebox as messagebox
import tkinter
import threading  # Necesario para hilos (Fase 5)
import time  # Necesario para la pausa del hilo (Fase 5)


class AppController:
    def __init__(self, master):
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.salir_app)

        self.model = GestorUsuarios()
        self.view = MainView(master)

        # Inicialización de rutas y avatares
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.ASSETS_PATH = self.BASE_DIR / "assetss"
        self.avatar_images = {}

        # Carga dinámica de nombres de archivos
        self.avatar_files = ["avatar1.png", "avatar2.png"]

        self.usuario_seleccionado_indice = -1

        # Variables de control de hilos (Fase 5)
        self.auto_guardado_activo = False
        self.auto_guardado_thread = None
        self.auto_guardado_stop_event = threading.Event()

        # Conexión de widgets
        self.view.add_button.configure(command=self.abrir_ventana_añadir)
        self._configurar_menu_commands()
        self._configurar_auto_guardado()

        self.view.edit_button.configure(command=self.abrir_ventana_editar)
        self.view.delete_button.configure(command=self.eliminar_usuario)

        self.view.busqueda_var.trace_add("write", self.manejar_filtro)
        self.view.genero_filtro_var.trace_add("write", self.manejar_filtro)

        self.cargar_usuarios()
        self.refrescar_lista_usuarios()
        self.view.set_estado(f"App iniciada. {len(self.model.listar())} usuarios cargados.")

    # --- Configuración UI / Menú ---
    def _configurar_menu_commands(self):
        """Conecta los comandos del menú Archivo a los métodos del controlador."""
        self.view.menu_archivo.add_command(label="Cargar", command=self.cargar_usuarios)
        self.view.menu_archivo.add_command(label="Guardar", command=self.guardar_usuarios)
        self.view.menu_archivo.add_separator()
        self.view.menu_archivo.add_command(label="Salir", command=self.salir_app)

    def _configurar_auto_guardado(self):
        """Crea el control del auto-guardado en el menú."""
        self.auto_guardado_var = tkinter.BooleanVar()
        self.view.menu_opciones.add_checkbutton(
            label="Auto-Guardado (cada 10s)",
            variable=self.auto_guardado_var,
            command=self.toggle_auto_guardado
        )

    # --- Lógica de Hilos (Fase 5) ---
    def toggle_auto_guardado(self):
        """Activa o desactiva la función de auto-guardado."""
        if self.auto_guardado_var.get():
            self.auto_guardado_activo = True
            self.auto_guardado_stop_event.clear()
            self.auto_guardado_thread = threading.Thread(target=self._hilo_auto_guardado, daemon=True)
            self.auto_guardado_thread.start()
            self.view.set_estado("Auto-Guardado: ACTIVADO")
        else:
            self.auto_guardado_activo = False
            self.auto_guardado_stop_event.set()
            self.view.set_estado("Auto-Guardado: DESACTIVADO")

    def _hilo_auto_guardado(self):
        """Función que se ejecuta en el hilo secundario."""
        while not self.auto_guardado_stop_event.is_set():
            self.auto_guardado_stop_event.wait(10)
            if self.auto_guardado_stop_event.is_set():
                break

            try:
                self.model.guardar_csv()
                # Actualiza la UI de forma segura
                self.master.after(0, lambda: self.view.set_estado("Auto-Guardado: CSV guardado automáticamente."))
            except Exception as e:
                # Reporte de error en el hilo principal
                self.master.after(0, lambda: self.view.set_estado(f"Auto-Guardado: ERROR ({e})"))

    def salir_app(self):
        """Maneja el cierre de la aplicación, deteniendo el hilo si está activo."""
        if self.auto_guardado_thread and self.auto_guardado_thread.is_alive():
            self.view.set_estado("Deteniendo auto-guardado...")
            self.auto_guardado_stop_event.set()
            self.auto_guardado_thread.join(1)

        self.master.destroy()

    # --- Lógica de Avatares ---
    def _load_avatar(self, path, key):
        """Carga y almacena la referencia de una imagen si no está en caché."""
        if not path.is_file():
            path = self.ASSETS_PATH / "avatar1.png"
            if not path.is_file(): return None
            key = "avatar1.png"

        if key not in self.avatar_images:
            try:
                img = Image.open(path)
                self.avatar_images[key] = ctk.CTkImage(light_image=img, dark_image=img, size=(150, 150))
            except Exception as e:
                # Esto es importante si las imágenes no cargan (por ej. falta Pillow)
                self.view.set_estado(f"Error al cargar avatar {key}: {e}")
                return None

        return self.avatar_images[key]

    # --- Lógica de Filtro y Selección ---
    def manejar_filtro(self, *args):
        self.refrescar_lista_usuarios()

    def refrescar_lista_usuarios(self):
        nombre_filtro = self.view.busqueda_var.get()
        genero_filtro = self.view.genero_filtro_var.get()

        usuarios_filtrados = self.model.filtrar(nombre_filtro, genero_filtro)

        self.view.actualizar_lista_usuarios(
            usuarios_filtrados,
            self.seleccionar_usuario_filtrado,
            self.doble_clic_usuario
        )

        if not usuarios_filtrados or self.model.get_usuario(self.usuario_seleccionado_indice) not in usuarios_filtrados:
            self.view.mostrar_detalles_usuario(None, None)
            self.usuario_seleccionado_indice = -1

    def seleccionar_usuario_filtrado(self, indice_filtrado):
        nombre_filtro = self.view.busqueda_var.get()
        genero_filtro = self.view.genero_filtro_var.get()
        usuarios_filtrados = self.model.filtrar(nombre_filtro, genero_filtro)

        if 0 <= indice_filtrado < len(usuarios_filtrados):
            usuario_filtrado = usuarios_filtrados[indice_filtrado]
            self.usuario_seleccionado_indice = self.model.get_indice_by_name(usuario_filtrado.nombre)

            avatar_path = self.ASSETS_PATH / usuario_filtrado.avatar
            avatar_image = self._load_avatar(avatar_path, usuario_filtrado.avatar)

            self.view.mostrar_detalles_usuario(usuario_filtrado, avatar_image)
            self.view.set_estado(f"Usuario {usuario_filtrado.nombre} seleccionado.")

    def doble_clic_usuario(self, nombre_usuario):
        idx = self.model.get_indice_by_name(nombre_usuario)
        if idx != -1:
            self.usuario_seleccionado_indice = idx
            self.abrir_ventana_editar()

    # --- Lógica de Alta (Add) ---
    def abrir_ventana_añadir(self):
        add_view = AddUserView(self.master, self.avatar_files)  # Pasa la lista de avatares
        add_view.guardar_button.configure(command=lambda: self.añadir_usuario(add_view))
        self.view.set_estado("Abriendo ventana de alta de usuario.")

    def añadir_usuario(self, add_view):
        data = add_view.get_data()
        if not data["nombre"] or not data["edad"]:
            messagebox.showerror("Error de Validación", "El nombre y la edad no pueden estar vacíos.")
            return
        try:
            edad = int(data["edad"])
        except ValueError:
            messagebox.showerror("Error de Validación", "La edad debe ser un número entero válido.")
            return

        nuevo_usuario = Usuario(nombre=data["nombre"], edad=edad, genero=data["genero"], avatar=data["avatar"])
        self.model.agregar(nuevo_usuario)
        self.refrescar_lista_usuarios()
        add_view.window.destroy()

        self.view.set_estado(f"Usuario '{nuevo_usuario.nombre}' añadido. Total: {len(self.model.listar())}")
        idx_filtrado = self.model.filtrar().index(nuevo_usuario)
        self.seleccionar_usuario_filtrado(idx_filtrado)

    # --- Lógica de Edición y Eliminación (Edit/Delete) ---
    def abrir_ventana_editar(self):
        if self.usuario_seleccionado_indice == -1: return
        usuario = self.model.get_usuario(self.usuario_seleccionado_indice)
        if not usuario: return

        edit_view = EditUserView(self.master, self.avatar_files)  # Pasa la lista de avatares
        edit_view.set_data(usuario)

        indice_a_editar = self.usuario_seleccionado_indice
        edit_view.guardar_button.configure(
            command=lambda: self.editar_usuario_confirmar(edit_view, indice_a_editar)
        )
        self.view.set_estado(f"Abriendo edición para {usuario.nombre}.")

    def editar_usuario_confirmar(self, edit_view, indice_real):
        data = edit_view.get_data()
        try:
            data['edad'] = int(data['edad'])
        except ValueError:
            messagebox.showerror("Error de Validación", "La edad debe ser un número entero válido.")
            return

        self.model.actualizar(indice_real, data)
        edit_view.window.destroy()
        self.refrescar_lista_usuarios()

        usuario_actualizado = self.model.get_usuario(indice_real)
        if usuario_actualizado:
            usuarios_filtrados = self.model.filtrar(self.view.busqueda_var.get(), self.view.genero_filtro_var.get())
            try:
                indice_filtrado = usuarios_filtrados.index(usuario_actualizado)
                self.seleccionar_usuario_filtrado(indice_filtrado)
            except ValueError:
                self.view.mostrar_detalles_usuario(None, None)
                self.usuario_seleccionado_indice = -1

        self.view.set_estado(f"Usuario '{data['nombre']}' editado correctamente.")

    def eliminar_usuario(self):
        if self.usuario_seleccionado_indice == -1: return
        usuario_a_eliminar = self.model.get_usuario(self.usuario_seleccionado_indice)

        if messagebox.askyesno("Confirmar Eliminación",
                               f"¿Estás seguro de que quieres eliminar a {usuario_a_eliminar.nombre}?"):
            self.model.eliminar(self.usuario_seleccionado_indice)
            self.usuario_seleccionado_indice = -1
            self.refrescar_lista_usuarios()
            self.view.set_estado(f"Usuario {usuario_a_eliminar.nombre} eliminado. Total: {len(self.model.listar())}")
        else:
            self.view.set_estado("Eliminación cancelada.")

    # --- Lógica de Persistencia (CSV) ---
    def guardar_usuarios(self):
        try:
            count = self.model.guardar_csv()
            messagebox.showinfo("Guardado OK", f"Se han guardado {count} usuarios correctamente.")
            self.view.set_estado(f"Guardado OK. {count} usuarios guardados en CSV.")
        except Exception as e:
            messagebox.showerror("Error de Guardado", f"Ocurrió un error al guardar el archivo: {e}")
            self.view.set_estado(f"Error de Guardado: {e}")

    def cargar_usuarios(self):
        try:
            count = self.model.cargar_csv()
            messagebox.showinfo("Carga OK", f"Se han cargado {count} usuarios desde el archivo.")
            self.refrescar_lista_usuarios()
            self.view.set_estado(f"Carga OK. {count} usuarios cargados desde CSV.")
        except Exception as e:
            messagebox.showerror("Error de Carga", f"Ocurrió un error al cargar el archivo: {e}")
            self.view.set_estado(f"Error de Carga: {e}")