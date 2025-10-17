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
                for data in libros.values():
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
            disponibles = {lid: data for lid, data in libros.items() if data["disponible"]}

            if not disponibles:
                print("No hay libros disponibles en este momento.")
                continue

            print("Libros disponibles:")
            for idx, (lid, data) in enumerate(disponibles.items(), start=1):
                print(f"{idx}. {data['titulo']} ({data['categoria']})")

            # Selección por número
            try:
                seleccion = int(input("Seleccione el número del libro a prestar: ")) - 1
                if not (0 <= seleccion < len(disponibles)):
                    print("Número inválido.")
                    continue
            except ValueError:
                print("Entrada inválida.")
                continue

            # ID del libro seleccionado
            libro_id = list(disponibles.keys())[seleccion]
            libro_data = disponibles[libro_id]

            # Actualizar disponibilidad en Firebase
            vm.update_libro(libro_id, disponible=False)

            # Guardar libro prestado en usuario con ID incluido
            libros_prestados = usuario_data.get("libros_prestados", [])
            libros_prestados.append({
                "id": libro_id,
                "titulo": libro_data["titulo"],
                "autor": libro_data["autor"],
                "categoria": libro_data["categoria"]
            })
            vm.update_usuario(id_usuario, libros_prestados=libros_prestados)

            print(f"Libro '{libro_data['titulo']}' prestado correctamente.")

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
