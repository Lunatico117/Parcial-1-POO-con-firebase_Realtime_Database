import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv
import os
from model.usuario import Usuario
from model.libro import Libro
import uuid

# Cargar variables de entorno
load_dotenv()
cred_path = os.getenv("FIREBASE_CREDENTIALS")
db_url = os.getenv("FIREBASE_DB_URL")

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {"databaseURL": db_url})

usuarios_ref = db.reference("usuarios")
libros_ref = db.reference("libros")

# -------- CRUD Usuarios --------
def create_usuario(nombre: str, id_usuario: str = None) -> str:
    if not id_usuario:
        id_usuario = str(uuid.uuid4())
    usuario = Usuario(nombre, id_usuario)
    usuarios_ref.child(id_usuario).set(usuario.to_dict())
    return id_usuario

def get_usuario(id_usuario: str) -> dict:
    return usuarios_ref.child(id_usuario).get()

def update_usuario(id_usuario: str, nombre: str = None):
    updates = {}
    if nombre:
        updates["nombre"] = nombre
    if updates:
        usuarios_ref.child(id_usuario).update(updates)

def delete_usuario(id_usuario: str):
    usuarios_ref.child(id_usuario).delete()

# -------- CRUD Libros --------
def create_libro(titulo: str, autor: str, categoria: str) -> str:
    libro_id = str(uuid.uuid4())
    libro = Libro(titulo, autor, categoria)
    libros_ref.child(libro_id).set(libro.to_dict())
    return libro_id

def get_libro(libro_id: str) -> dict:
    return libros_ref.child(libro_id).get()

def update_libro(libro_id, titulo=None, autor=None, categoria=None, disponible=None):
    updates = {}
    if titulo:
        updates["titulo"] = titulo
    if autor:
        updates["autor"] = autor
    if categoria:
        updates["categoria"] = categoria
    if disponible is not None:
        updates["disponible"] = disponible
    if updates:
        libros_ref.child(libro_id).update(updates)

def delete_libro(libro_id):
    libros_ref.child(libro_id).delete()
