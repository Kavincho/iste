from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de la base de datos
MONGO_URI = os.getenv('MONGO_URI', "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv('DATABASE_NAME', "ecommerce_db")

def get_db_connection():
    """Obtiene la conexión a la base de datos MongoDB"""
    try:
        client = MongoClient(MONGO_URI)
        # Verificar que la conexión funciona
        client.admin.command('ping')
        db = client[DATABASE_NAME]
        return db
    except Exception as e:
        print(f"Error conectando a MongoDB: {e}")
        return None

def init_database():
    """Inicializa la base de datos con las colecciones necesarias"""
    db = get_db_connection()
    if db is None:
        print("Error al inicializar la base de datos: No se pudo conectar")
        return False
        
    try:
        # Crear colecciones si no existen
        collections = ['usuarios', 'productos', 'pedidos', 'numeros']
        for collection in collections:
            if collection not in db.list_collection_names():
                db.create_collection(collection)
                print(f"Colección '{collection}' creada")
        
        print("Base de datos inicializada correctamente")
        return True
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        return False 