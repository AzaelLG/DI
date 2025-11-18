import customtkinter as ctk
from model.usuario_model import GestorUsuarios, Usuario
from view.main_view import MainView, AddUserView, EditUserView
from pathlib import Path
from PIL import Image
import tkinter.messagebox as messagebox
import tkinter


class AppController:
    def __init__(self, master):
        self.master = master
        self.model = GestorUsuarios()
        self.view = MainView(master)

        # Inicializar rutas de archivo
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.ASSETS_PATH = self.BASE_DIR / "assets"
        self.avatar_images = {}
        self.avatar_files = [f.name for f in self.ASSETS_PATH.glob('*.png') if f.is_file()]
        if not self.avatar_files:
            self.avatar_files = ["default.png"]

            # Estado: Índice del usuario actualmente seleccionado en la lista NO FILTRADA del Modelo
        self.usuario_seleccionado_indice = -1

        # Conexión de botones y menús
        self.view.add_button.configure(command=self.abrir_ventana_añadir)
        self._configurar_menu_commands()

        # Conexión de edición/eliminación (¡NUEVO!)
        self.view.edit_button.configure(command=self.abrir_ventana_editar)
        self.view.delete_button.configure(command=self.eliminar_usuario)

        # Conexión de búsqueda/filtro con trace_add (¡NUEVO!)
        self.view.busqueda_var.trace_add("write", self.manejar_filtro)
        self.view.genero_filtro_var.trace_add("write", self.manejar_filtro)

        # Carga inicial y refresco de UI
        self.cargar_usuarios()
        self.refrescar_lista_usuarios()
        self.view.set_estado(f"App iniciada. {len(self.model.listar())} usuarios cargados.")

    # --- Configuración UI ---
    def _configurar_menu_commands(self):
        """Conecta los comandos del menú Archivo a los métodos del controlador."""
        self.view.menu_archivo.add_command(label="Cargar", command=self.cargar_usuarios)
        self.view.menu_archivo.add_command(label="Guardar", command=self.guardar_usuarios)
        self.view.menu_archivo.add_separator()
        self.view.menu_archivo.add_command(label="Salir", command=self.master.quit)

    def _load_avatar(self, path, key):
        """Carga y almacena la referencia de una imagen si no está en caché."""
        if not path.is_file():
            # Devuelve un avatar por defecto si no se encuentra
            path = self.ASSETS_PATH / "default.png"
            if not path.is_file(): return None
            key = "default.png"

        if key not in self.avatar_images:
            try:
                img = Image.open(path)
                self.avatar_images[key] = ctk.CTkImage(light_image=img, dark_image=img, size=(150, 150))
            except Exception as e:
                print(f"Error al cargar imagen {path}: {e}")
                return None

        return self.avatar_images[key]

    # --- Manejo de la Lista (Refresco/Filtro) ---
    def manejar_filtro(self, *args):
        """Llamado por trace_add cuando cambia el texto de búsqueda o el filtro de género."""
        self.refrescar_lista_usuarios()

    def refrescar_lista_usuarios(self):
        """
        Pide la lista FILTRADA al Modelo, la pasa a la Vista y actualiza el estado.
        """
        nombre_filtro = self.view.busqueda_var.get()
        genero_filtro = self.view.genero_filtro_var.get()

        # Obtener la lista de usuarios FILTRADOS
        usuarios_filtrados = self.model.filtrar(nombre_filtro, genero_filtro)

        # Pasar la lista filtrada y los callbacks a la Vista
        self.view.actualizar_lista_usuarios(
            usuarios_filtrados,
            self.seleccionar_usuario_filtrado,  # Callback para el click
            self.doble_clic_usuario  # Callback para el doble clic
        )

        # Si la lista filtrada no tiene el usuario seleccionado, o está vacía, se deselecciona
        if not usuarios_filtrados or self.model.get_usuario(self.usuario_seleccionado_indice) not in usuarios_filtrados:
            self.view.mostrar_detalles_usuario(None, None)
            self.usuario_seleccionado_indice = -1

    def seleccionar_usuario_filtrado(self, indice_filtrado):
        """
        Callback del click. Recibe el índice en la lista FILTRADA.
        Busca el usuario y establece el índice REAL para edición/eliminación.
        """
        nombre_filtro = self.view.busqueda_var.get()
        genero_filtro = self.view.genero_filtro_var.get()
        usuarios_filtrados = self.model.filtrar(nombre_filtro, genero_filtro)

        if 0 <= indice_filtrado < len(usuarios_filtrados):
            usuario_filtrado = usuarios_filtrados[indice_filtrado]

            # Buscar el índice REAL en la lista del modelo para futuras operaciones
            self.usuario_seleccionado_indice = self.model.get_indice_by_name(usuario_filtrado.nombre)

            avatar_path = self.ASSETS_PATH / usuario_filtrado.avatar
            avatar_image = self._load_avatar(avatar_path, usuario_filtrado.avatar)

            self.view.mostrar_detalles_usuario(usuario_filtrado, avatar_image)
            self.view.set_estado(f"Usuario {usuario_filtrado.nombre} seleccionado.")

    def doble_clic_usuario(self, nombre_usuario):
        """Callback del doble clic: busca el usuario por nombre, establece el índice y abre la edición."""
        idx = self.model.get_indice_by_name(nombre_usuario)
        if idx != -1:
            self.usuario_seleccionado_indice = idx  # Establecer el índice seleccionado
            self.abrir_ventana_editar()

    # --- Lógica de Alta (Add) ---
    def abrir_ventana_añadir(self):
        """Crea y abre la ventana modal para añadir un usuario."""
        add_view = AddUserView(self.master, self.avatar_files)
        add_view.guardar_button.configure(command=lambda: self.añadir_usuario(add_view))
        self.view.set_estado("Abriendo ventana de alta de usuario.")

    def añadir_usuario(self, add_view):
        """Procesa los datos, añade al Modelo y refresca la UI."""
        data = add_view.get_data()

        if not data["nombre"] or not data["edad"]:
            messagebox.showerror("Error de Validación", "El nombre y la edad no pueden estar vacíos.")
            return
        try:
            edad = int(data["edad"])
        except ValueError:
            messagebox.showerror("Error de Validación", "La edad debe ser un número entero válido.")
            return

        nuevo_usuario = Usuario(
            nombre=data["nombre"],
            edad=edad,
            genero=data["genero"],
            avatar=data["avatar"]
        )

        self.model.agregar(nuevo_usuario)
        self.refrescar_lista_usuarios()
        add_view.window.destroy()

        self.view.set_estado(f"Usuario '{nuevo_usuario.nombre}' añadido. Total: {len(self.model.listar())}")
        # Intentar seleccionar el nuevo usuario (para que se vean los detalles)
        idx = self.model.get_indice_by_name(nuevo_usuario.nombre)
        if idx != -1:
            self.seleccionar_usuario_filtrado(self.model.filtrar().index(nuevo_usuario))

    # --- Lógica de Edición y Eliminación (Edit/Delete) (¡NUEVO!) ---
    def abrir_ventana_editar(self):
        """Abre la ventana modal de edición con los datos del usuario seleccionado."""
        if self.usuario_seleccionado_indice == -1:
            return  # Ya deshabilitado en la Vista, pero se comprueba

        usuario = self.model.get_usuario(self.usuario_seleccionado_indice)
        if not usuario:
            self.view.set_estado("Error: Usuario seleccionado no existe.")
            return

        edit_view = EditUserView(self.master, self.avatar_files)
        edit_view.set_data(usuario)

        # Usar el índice REAL para la actualización
        indice_a_editar = self.usuario_seleccionado_indice
        edit_view.guardar_button.configure(
            command=lambda: self.editar_usuario_confirmar(edit_view, indice_a_editar)
        )
        self.view.set_estado(f"Abriendo edición para {usuario.nombre}.")

    def editar_usuario_confirmar(self, edit_view, indice_real):
        """Procesa los datos editados, actualiza el modelo y refresca la UI."""
        data = edit_view.get_data()

        try:
            data['edad'] = int(data['edad'])
        except ValueError:
            messagebox.showerror("Error de Validación", "La edad debe ser un número entero válido.")
            return

        self.model.actualizar(indice_real, data)
        edit_view.window.destroy()
        self.refrescar_lista_usuarios()

        # Volver a seleccionar el usuario (es el mismo índice)
        usuario_actualizado = self.model.get_usuario(indice_real)
        if usuario_actualizado:
            # Encontrar su posición en la lista filtrada para seleccionarlo
            usuarios_filtrados = self.model.filtrar(self.view.busqueda_var.get(), self.view.genero_filtro_var.get())
            try:
                indice_filtrado = usuarios_filtrados.index(usuario_actualizado)
                self.seleccionar_usuario_filtrado(indice_filtrado)
            except ValueError:
                # Si el usuario editado ya no cumple el filtro, solo se refresca la lista
                self.view.mostrar_detalles_usuario(None, None)
                self.usuario_seleccionado_indice = -1

        self.view.set_estado(f"Usuario '{data['nombre']}' editado correctamente.")

    def eliminar_usuario(self):
        """Elimina el usuario seleccionado del modelo y refresca la UI."""
        if self.usuario_seleccionado_indice == -1:
            return

        usuario_a_eliminar = self.model.get_usuario(self.usuario_seleccionado_indice)

        if messagebox.askyesno("Confirmar Eliminación",
                               f"¿Estás seguro de que quieres eliminar a {usuario_a_eliminar.nombre}?"):
            self.model.eliminar(self.usuario_seleccionado_indice)
            self.usuario_seleccionado_indice = -1  # Limpiar la selección
            self.refrescar_lista_usuarios()
            self.view.set_estado(f"Usuario {usuario_a_eliminar.nombre} eliminado. Total: {len(self.model.listar())}")
        else:
            self.view.set_estado("Eliminación cancelada.")

    # --- Lógica de Persistencia (CSV) ---
    def guardar_usuarios(self):
        """Llama al modelo para guardar en CSV y da feedback al usuario."""
        try:
            count = self.model.guardar_csv()
            messagebox.showinfo("Guardado OK", f"Se han guardado {count} usuarios correctamente.")
            self.view.set_estado(f"Guardado OK. {count} usuarios guardados en CSV.")
        except Exception as e:
            messagebox.showerror("Error de Guardado", f"Ocurrió un error al guardar el archivo: {e}")
            self.view.set_estado(f"Error de Guardado: {e}")

    def cargar_usuarios(self):
        """Llama al modelo para cargar desde CSV y actualiza la lista."""
        try:
            count = self.model.cargar_csv()
            messagebox.showinfo("Carga OK", f"Se han cargado {count} usuarios desde el archivo.")
            self.refrescar_lista_usuarios()
            self.view.set_estado(f"Carga OK. {count} usuarios cargados desde CSV.")
        except Exception as e:
            messagebox.showerror("Error de Carga", f"Ocurrió un error al cargar el archivo: {e}")
            self.view.set_estado(f"Error de Carga: {e}")