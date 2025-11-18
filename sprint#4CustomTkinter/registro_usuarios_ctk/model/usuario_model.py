import csv
from pathlib import Path


class Usuario:
    """Clase de datos simple para un Usuario."""

    def __init__(self, nombre, edad, genero, avatar):
        self.nombre = nombre
        self.edad = edad
        self.genero = genero
        self.avatar = avatar

    def __str__(self):
        return f"{self.nombre} ({self.edad}, {self.genero})"


class GestorUsuarios:
    """Clase que gestiona la lista de usuarios y la lógica de negocio."""

    def __init__(self, archivo_csv="usuarios.csv"):
        self.ARCHIVO_CSV = archivo_csv
        self._usuarios = []
        # No carga datos de ejemplo, se usa la carga desde CSV

    # --- Métodos de Listado/Consulta ---
    def listar(self):
        """Devuelve la lista completa de usuarios."""
        return self._usuarios

    def get_usuario(self, indice):
        """Devuelve un usuario por su índice."""
        try:
            return self._usuarios[indice]
        except IndexError:
            return None

    def get_indice_by_name(self, nombre):
        """Devuelve el índice del primer usuario con ese nombre."""
        for i, usuario in enumerate(self._usuarios):
            if usuario.nombre == nombre:
                return i
        return -1

    def filtrar(self, nombre_filtro="", genero_filtro=""):
        """Devuelve una lista de usuarios que cumplen con los criterios de búsqueda/filtrado."""
        # Normalizar filtros a minúsculas
        nombre_filtro = nombre_filtro.strip().lower()

        usuarios_filtrados = []
        for usuario in self._usuarios:
            # 1. Coincidencia por nombre (si el filtro no está vacío)
            coincide_nombre = nombre_filtro in usuario.nombre.lower() or not nombre_filtro

            # 2. Coincidencia por género (si el filtro no es "Todos")
            coincide_genero = (usuario.genero == genero_filtro or
                               not genero_filtro or
                               genero_filtro == "Todos")

            if coincide_nombre and coincide_genero:
                usuarios_filtrados.append(usuario)

        return usuarios_filtrados

    # --- Métodos de Mutación (Alta/Edición/Baja) ---
    def agregar(self, usuario):
        """Añade un nuevo objeto Usuario a la lista."""
        self._usuarios.append(usuario)

    def actualizar(self, indice, nuevos_datos):
        """
        Actualiza el usuario en un índice dado con los nuevos_datos (diccionario).
        """
        if 0 <= indice < len(self._usuarios):
            usuario = self._usuarios[indice]
            usuario.nombre = nuevos_datos.get('nombre', usuario.nombre)
            usuario.edad = nuevos_datos.get('edad', usuario.edad)
            usuario.genero = nuevos_datos.get('genero', usuario.genero)
            usuario.avatar = nuevos_datos.get('avatar', usuario.avatar)
            return True
        return False

    def eliminar(self, indice):
        """Elimina el usuario en el índice dado."""
        if 0 <= indice < len(self._usuarios):
            del self._usuarios[indice]
            return True
        return False

    # --- Métodos de Persistencia (CSV) ---
    def guardar_csv(self):
        """Guarda la lista de usuarios en el archivo CSV."""
        with open(self.ARCHIVO_CSV, 'w', newline='', encoding='utf-8') as f:
            escritor = csv.writer(f)
            # Cabecera
            escritor.writerow(['Nombre', 'Edad', 'Género', 'Avatar'])
            # Datos
            for u in self._usuarios:
                escritor.writerow([u.nombre, u.edad, u.genero, u.avatar])
        return len(self._usuarios)

    def cargar_csv(self):
        """Carga los usuarios desde el archivo CSV, manejando excepciones."""
        self._usuarios.clear()  # Limpiar antes de cargar
        registros_cargados = 0
        try:
            with open(self.ARCHIVO_CSV, 'r', encoding='utf-8') as f:
                lector = csv.reader(f)
                next(lector)  # Saltar la cabecera
                for fila in lector:
                    try:
                        nombre, edad_str, genero, avatar = fila
                        edad = int(edad_str)
                        self._usuarios.append(Usuario(nombre, edad, genero, avatar))
                        registros_cargados += 1
                    except ValueError:
                        print(f"Advertencia: Fila con datos corruptos omitida: {fila}")
        except FileNotFoundError:
            pass  # Si no existe, se inicia con la lista vacía

        return registros_cargados