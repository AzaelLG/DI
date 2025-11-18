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

    def __init__(self):
        self._usuarios = []
        self._cargar_datos_de_ejemplo()  # Carga datos de prueba al inicio

    def _cargar_datos_de_ejemplo(self):
        """Añade usuarios de ejemplo para la prueba inicial."""
        self._usuarios.append(Usuario("Ana García", 28, "Femenino", "avatar1.png"))
        self._usuarios.append(Usuario("Luis Pérez", 34, "Masculino", "avatar2.png"))
        self._usuarios.append(Usuario("Elena Ruiz", 22, "Femenino", "avatar3.png"))

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

    def agregar(self, usuario):
        """Añade un nuevo objeto Usuario a la lista."""
        self._usuarios.append(usuario)