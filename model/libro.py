class Libro:
    def __init__(self, titulo, autor, categoria, disponible=True):
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self._disponible = disponible

    def esta_disponible(self):
        return self._disponible

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "autor": self.autor,
            "categoria": self.categoria,
            "disponible": self._disponible
        }
