from model.libro import Libro
from model.usuario import Usuario
from viewmodel import biblioteca_vm as vm
import uuid


def main():
    categorias = ["Ciencia", "Literatura", "Historia"]

    # Libros iniciales
    vm.create_libro("Fisica Basica", "Serway", "Ciencia")
    vm.create_libro("Cien años de soledad", "Gabriel Garcia Marquez", "Literatura")
    vm.create_libro("Historia Universal", "Juan Perez", "Historia")

    while True:
        print("\n--- Menu Biblioteca Universitaria ---")
        print("1. Mostrar libros")
        print("2. Agregar libro")
        print("3. Agregar usuario")
        print("4. Prestar libro")
        print("5. Devolver libro")
        print("6. Salir")
        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            libros = vm.libros_ref.get() or {}
            if not libros:
                print("No hay libros en la biblioteca.")
            else:
                for libro_id, data in libros.items():
                    estado = "Disponible" if data["disponible"] else "Prestado"
                    print(f"Título: {data['titulo']}, Autor: {data['autor']}, Categoria: {data['categoria']}, Estado: {estado}")

        elif opcion == "2":
            titulo = input("Titulo del libro: ")
            autor = input("Autor: ")
            print("Categorias disponibles:", ", ".join(categorias))
            categoria = input("Categoria: ")
            if categoria not in categorias:
                print("Categoria no valida. Se agregara a la lista de categorias.")
                categorias.append(categoria)
            vm.create_libro(titulo, autor, categoria)
            print("Libro agregado correctamente.")

        elif opcion == "3":
            nombre = input("Nombre del usuario: ")
            id_usuario = str(uuid.uuid4())  # ID generado automáticamente
            print(f"Se generó el ID único del usuario: {id_usuario}")
            if vm.get_usuario(id_usuario):
                print("Ya existe un usuario con ese ID (muy raro, pero puede pasar).")
            else:
                vm.create_usuario(nombre, id_usuario)
                print("Usuario agregado correctamente.")

        elif opcion == "4":
            id_usuario = input("ID del usuario: ")
            usuario_data = vm.get_usuario(id_usuario)
            if not usuario_data:
                print("Usuario no encontrado.")
                continue

            libros = vm.libros_ref.get() or {}
            print("Libros disponibles:")
            for libro_id, data in libros.items():
                if data["disponible"]:
                    print(f"{libro_id}: {data['titulo']} ({data['categoria']})")

            libro_id = input("ID del libro a prestar: ")
            libro_data = vm.get_libro(libro_id)
            if not libro_data:
                print("Libro no encontrado.")
                continue
            if not libro_data["disponible"]:
                print("Libro no disponible.")
                continue

            # Actualizar disponibilidad y agregar a usuario
            vm.update_libro(libro_id, disponible=False)
            libros_prestados = usuario_data.get("libros_prestados", [])
            libros_prestados.append(Libro(libro_data["titulo"], libro_data["autor"], libro_data["categoria"]).to_dict())
            vm.update_usuario(id_usuario, libros_prestados=libros_prestados)
            print("Libro prestado correctamente.")

        elif opcion == "5":
            id_usuario = input("ID del usuario: ")
            usuario_data = vm.get_usuario(id_usuario)
            if not usuario_data:
                print("Usuario no encontrado.")
                continue

            prestamos = usuario_data.get("libros_prestados", [])
            if not prestamos:
                print("El usuario no tiene libros prestados.")
                continue

            print("Libros prestados:")
            for idx, libro in enumerate(prestamos):
                print(f"{idx+1}. {libro['titulo']} ({libro['categoria']})")

            indice_input = int(input("Seleccione el numero del libro a devolver: ")) - 1
            if not (0 <= indice_input < len(prestamos)):
                print("Índice fuera de rango.")
                continue

            libro_dev = prestamos.pop(indice_input)
            # Buscar ID del libro en Firebase
            libros = vm.libros_ref.get() or {}
            libro_id = None
            for lid, data in libros.items():
                if data["titulo"] == libro_dev["titulo"] and data["autor"] == libro_dev["autor"]:
                    libro_id = lid
                    break
            if libro_id:
                vm.update_libro(libro_id, disponible=True)

            vm.update_usuario(id_usuario, libros_prestados=prestamos)
            print(f"Libro devuelto correctamente: '{libro_dev['titulo']}'.")

        elif opcion == "6":
            print("¡Has salido de la biblioteca U!")
            break
        else:
            print("Opcion no valida. Intente de nuevo.")


if __name__ == "__main__":
    main()
