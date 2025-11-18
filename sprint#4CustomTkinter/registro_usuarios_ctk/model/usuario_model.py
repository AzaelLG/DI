import csv


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

    def __init__(self,archivo_csv="usuarios.csv"):
        self._usuarios = []
        self.ARCHIVO_CSV = archivo_csv

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

    def guardar_csv(self):
        """Guarda la lista de usuarios en el archivo CSV."""
        with open(self.ARCHIVO_CSV, 'w', newline='', encoding='utf-8') as f:
            escritor = csv.writer(f)
            # Cabecera
            escritor.writerow(['Nombre', 'Edad', 'Género', 'Avatar'])
            # Datos
            for u in self._usuarios:
                escritor.writerow([u.nombre, u.edad, u.genero, u.avatar])
        return len(self._usuarios)  # Devolver el número de registros guardados

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
                        edad = int(edad_str)  # Validación de tipo
                        self._usuarios.append(Usuario(nombre, edad, genero, avatar))
                        registros_cargados += 1
                    except ValueError:
                        print(f"Advertencia: Fila con datos corruptos omitida: {fila}")
                    except Exception as e:
                        print(f"Error al leer fila: {fila}. Error: {e}")

        except FileNotFoundError:
            # Si el archivo no existe, no es un error, simplemente se inicia vacío.
            pass

        return registros_cargados