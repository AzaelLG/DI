from tkinter import messagebox

import customtkinter as ctk
from model.usuario_model import GestorUsuarios
from view.main_view import MainView
from pathlib import Path
from PIL import Image

from registro_usuarios_ctk.model.usuario_model import Usuario
from registro_usuarios_ctk.view.main_view import AddUserView


class AppController:
    def __init__(self, master):
        self.master = master
        self.model = GestorUsuarios()
        self.view = MainView(master)
        self.view.add_button.configure(command=self.abrir_ventana_añadir)
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.ASSETS_PATH = self.BASE_DIR / "assets"
        self.avatar_images = {}
        self.avatar_files = [f.name for f in self.ASSETS_PATH.glob('*.png') if f.is_file()]
        if not self.avatar_files:
            self.avatar_files = ["default.png"]
        self._configurar_menu_commands()
        self.cargar_usuarios()
        self.view.add_button.configure(command=self.abrir_ventana_añadir)

        self.refrescar_lista_usuarios()

    def refrescar_lista_usuarios(self):
        """
        1. Pide la lista al Modelo.
        2. La pasa a la Vista junto con el callback de selección.
        """
        usuarios = self.model.listar()
        # Le pasa a la vista la lista de usuarios y el MÉTODO a llamar al hacer clic.
        self.view.actualizar_lista_usuarios(usuarios, self.seleccionar_usuario)
        
        # Limpiar detalles si la lista se vacía
        if not usuarios:
             self.view.mostrar_detalles_usuario(None, None)

    def seleccionar_usuario(self, indice):
        """
        Este es el callback.
        1. Obtiene el usuario completo del Modelo.
        2. Carga su imagen y la pasa a la Vista.
        """
        usuario = self.model.get_usuario(indice)
        if not usuario:
            return

        # Lógica para cargar la imagen (Pista clave del enunciado)
        avatar_path = self.ASSETS_PATH / usuario.avatar
        avatar_image = self._load_avatar(avatar_path, usuario.avatar)

        # Muestra los detalles en la Vista (Paso 1.3 - Punto 4)
        self.view.mostrar_detalles_usuario(usuario, avatar_image)
        
    def _load_avatar(self, path, key):
        """Carga y almacena la referencia de una imagen si no está en caché."""
        if not path.is_file():
            print(f"Advertencia: Archivo de avatar no encontrado en {path}")
            return None
            
        # Usar la clave (nombre del archivo) para la caché
        if key not in self.avatar_images:
            try:
                # Cargar con PIL.Image
                img = Image.open(path)
                # Crear CTkImage y guardarla en la caché
                self.avatar_images[key] = ctk.CTkImage(
                    light_image=img,
                    dark_image=img,
                    size=(150, 150)
                )
            except Exception as e:
                print(f"Error al cargar imagen {path}: {e}")
                return None
                
        return self.avatar_images[key]

    def abrir_ventana_añadir(self):
        """Crea y abre la ventana modal para añadir un usuario."""
        add_view = AddUserView(self.master, self.avatar_files)
        # Conectar el botón de guardar de la modal a la función de procesamiento
        # Usar lambda para pasar la referencia a la propia vista modal
        add_view.guardar_button.configure(command=lambda: self.añadir_usuario(add_view))

    def añadir_usuario(self, add_view):
        """
        Callback del botón Guardar.
        1. Valida. 2. Añade al modelo. 3. Refresca la UI.
        """
        data = add_view.get_data()

        # Validación de campos
        if not data["nombre"] or not data["edad"]:
            messagebox.showerror("Error de Validación", "El nombre y la edad no pueden estar vacíos.")
            return

        try:
            edad = int(data["edad"])
        except ValueError:
            messagebox.showerror("Error de Validación", "La edad debe ser un número entero válido.")
            return

        # 1. Crear el objeto Usuario
        nuevo_usuario = Usuario(
            nombre=data["nombre"],
            edad=edad,
            genero=data["genero"],
            avatar=data["avatar"]
        )

        # 2. Añadir al Modelo
        self.model.agregar(nuevo_usuario)

        # 3. Refrescar la Vista y cerrar la modal
        self.refrescar_lista_usuarios()
        add_view.window.destroy()

        # Intentar seleccionar el nuevo usuario para mostrar sus detalles
        idx = self.model.get_indice_by_name(nuevo_usuario.nombre)
        if idx != -1:
            self.seleccionar_usuario(idx)

    def _configurar_menu_commands(self):
        """Conecta los comandos del menú Archivo a los métodos del controlador."""
        self.view.menu_archivo.add_command(label="Cargar", command=self.cargar_usuarios)
        self.view.menu_archivo.add_command(label="Guardar", command=self.guardar_usuarios)
        self.view.menu_archivo.add_separator()
        self.view.menu_archivo.add_command(label="Salir", command=self.master.quit)  # Usa quit() para cerrar la app

    # ... (refrescar_lista_usuarios, seleccionar_usuario, _load_avatar, abrir_ventana_añadir, añadir_usuario igual)

    def guardar_usuarios(self):
        """Llama al modelo para guardar en CSV y da feedback al usuario."""
        try:
            count = self.model.guardar_csv()
            messagebox.showinfo("Guardado OK", f"Se han guardado {count} usuarios correctamente.")
        except Exception as e:
            messagebox.showerror("Error de Guardado", f"Ocurrió un error al guardar el archivo: {e}")

    def cargar_usuarios(self):
        """Llama al modelo para cargar desde CSV y actualiza la lista."""
        try:
            count = self.model.cargar_csv()
            messagebox.showinfo("Carga OK", f"Se han cargado {count} usuarios desde el archivo.")
            self.refrescar_lista_usuarios()  # Actualizar la vista con los nuevos datos
        except Exception as e:
            # Solo si ocurre un error inesperado (ej. permisos), no por FileNotFoundError
            messagebox.showerror("Error de Carga", f"Ocurrió un error al cargar el archivo: {e}")