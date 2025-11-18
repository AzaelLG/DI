import customtkinter as ctk
from model.usuario_model import GestorUsuarios
from view.main_view import MainView
from pathlib import Path
from PIL import Image

class AppController:
    def __init__(self, master):
        self.master = master
        self.model = GestorUsuarios()
        self.view = MainView(master)
        
        # Inicializar rutas de archivo (Pista clave del enunciado)
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.ASSETS_PATH = self.BASE_DIR / "assets"
        self.avatar_images = {} # Caché para mantener vivas las referencias a CTkImage

        # Llamada inicial para poblar la lista al arrancar (Paso 1.3 - Punto 6)
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