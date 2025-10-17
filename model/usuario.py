class Usuario:
    def __init__(self, nombre, id_usuario):
        self._nombre = nombre
        self._id_usuario = id_usuario
        self._libros_prestados = []

    def tomar_libro(self, libro):
        if libro in self._libros_prestados:
            return False
        self._libros_prestados.append(libro)
        return True

    def devolver_libro(self, libro):
        if libro in self._libros_prestados:
            self._libros_prestados.remove(libro)
            return True
        return False

    def get_nombre(self):
        return self._nombre

    def get_id(self):
        return self._id_usuario

    def get_libros_prestados(self):
        return self._libros_prestados

    def to_dict(self):
        return {
            "nombre": self._nombre,
            "libros_prestados": [libro.to_dict() for libro in self._libros_prestados]
        }
