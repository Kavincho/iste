from database.connection import get_db_connection
from bson import ObjectId
import datetime

class Usuario:
    def __init__(self, nombre=None, email=None, password=None, fecha=None, _id=None):
        self.nombre = nombre
        self.email = email
        self.password = password
        self.fecha = fecha or datetime.datetime.now()
        self._id = _id
    
    def to_dict(self):
        """Convierte el objeto a diccionario para MongoDB"""
        return {
            'nombre': self.nombre,
            'email': self.email,
            'password': self.password,
            'fecha': self.fecha
        }
    
    @staticmethod
    def from_dict(data):
        """Crea un objeto Usuario desde un diccionario de MongoDB"""
        return Usuario(
            nombre=data.get('nombre'),
            email=data.get('email'),
            password=data.get('password'),
            fecha=data.get('fecha'),
            _id=str(data.get('_id')) if data.get('_id') else None
        )
    
    def save(self):
        """Guarda el usuario en la base de datos"""
        db = get_db_connection()
        if db is None:
            raise Exception("Error de conexión a la base de datos")
            
        if self._id:
            # Actualizar usuario existente
            result = db.usuarios.update_one(
                {'_id': ObjectId(self._id)},
                {'$set': self.to_dict()}
            )
            return result.modified_count > 0
        else:
            # Crear nuevo usuario
            result = db.usuarios.insert_one(self.to_dict())
            self._id = str(result.inserted_id)
            return True
    
    @staticmethod
    def find_all():
        """Obtiene todos los usuarios"""
        db = get_db_connection()
        if db is None:
            raise Exception("Error de conexión a la base de datos")
            
        usuarios = list(db.usuarios.find())
        return [Usuario.from_dict(usuario) for usuario in usuarios]
    
    @staticmethod
    def find_by_id(usuario_id):
        """Busca un usuario por ID"""
        try:
            db = get_db_connection()
            if db is None:
                raise Exception("Error de conexión a la base de datos")
                
            usuario_data = db.usuarios.find_one({'_id': ObjectId(usuario_id)})
            return Usuario.from_dict(usuario_data) if usuario_data else None
        except Exception as e:
            print(f"Error al buscar usuario por ID: {e}")
            return None
    
    @staticmethod
    def find_by_email(email):
        """Busca un usuario por email"""
        db = get_db_connection()
        if db is None:
            raise Exception("Error de conexión a la base de datos")
            
        usuario_data = db.usuarios.find_one({'email': email})
        return Usuario.from_dict(usuario_data) if usuario_data else None
    
    def delete(self):
        """Elimina el usuario de la base de datos"""
        if self._id:
            db = get_db_connection()
            if db is None:
                raise Exception("Error de conexión a la base de datos")
                
            result = db.usuarios.delete_one({'_id': ObjectId(self._id)})
            return result.deleted_count > 0
        return False
    
    @staticmethod
    def delete_by_id(usuario_id):
        """Elimina un usuario por ID"""
        try:
            db = get_db_connection()
            if db is None:
                raise Exception("Error de conexión a la base de datos")
                
            result = db.usuarios.delete_one({'_id': ObjectId(usuario_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error al eliminar usuario por ID: {e}")
            return False 