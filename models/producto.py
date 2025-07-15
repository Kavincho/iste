from database.connection import get_db_connection
from bson import ObjectId
import datetime

class Producto:
    def __init__(self, nombre=None, descripcion=None, precio=None, stock=None, categoria=None, imagen=None, fecha=None, _id=None):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock or 0
        self.categoria = categoria
        self.imagen = imagen
        self.fecha = fecha or datetime.datetime.now()
        self._id = _id
    
    def to_dict(self):
        """Convierte el objeto a diccionario para MongoDB"""
        return {
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': self.precio,
            'stock': self.stock,
            'categoria': self.categoria,
            'imagen': self.imagen,
            'fecha': self.fecha
        }
    
    @staticmethod
    def from_dict(data):
        """Crea un objeto Producto desde un diccionario de MongoDB"""
        return Producto(
            nombre=data.get('nombre'),
            descripcion=data.get('descripcion'),
            precio=data.get('precio'),
            stock=data.get('stock'),
            categoria=data.get('categoria'),
            imagen=data.get('imagen'),
            fecha=data.get('fecha'),
            _id=str(data.get('_id')) if data.get('_id') else None
        )
    
    def save(self):
        """Guarda el producto en la base de datos"""
        db = get_db_connection()
        if db is None:
            raise Exception("Error de conexión a la base de datos")
            
        if self._id:
            # Actualizar producto existente
            result = db.productos.update_one(
                {'_id': ObjectId(self._id)},
                {'$set': self.to_dict()}
            )
            return result.modified_count > 0
        else:
            # Crear nuevo producto
            result = db.productos.insert_one(self.to_dict())
            self._id = str(result.inserted_id)
            return True
    
    @staticmethod
    def find_all():
        """Obtiene todos los productos"""
        db = get_db_connection()
        if db is None:
            raise Exception("Error de conexión a la base de datos")
        productos = list(db.productos.find())
        return [Producto.from_dict(producto) for producto in productos]
    
    @staticmethod
    def find_by_id(producto_id):
        """Busca un producto por ID"""
        try:
            db = get_db_connection()
            if db is None:
                raise Exception("Error de conexión a la base de datos")
            producto_data = db.productos.find_one({'_id': ObjectId(producto_id)})
            return Producto.from_dict(producto_data) if producto_data else None
        except Exception as e:
            print(f"Error al buscar producto por ID: {e}")
            return None
    
    @staticmethod
    def find_by_categoria(categoria):
        """Busca productos por categoría"""
        db = get_db_connection()
        if db is None:
            raise Exception("Error de conexión a la base de datos")
        productos = list(db.productos.find({'categoria': categoria}))
        return [Producto.from_dict(producto) for producto in productos]
    
    @staticmethod
    def search_by_name(nombre):
        """Busca productos por nombre (búsqueda parcial)"""
        db = get_db_connection()
        if db is None:
            raise Exception("Error de conexión a la base de datos")
        # Búsqueda case-insensitive
        productos = list(db.productos.find({
            'nombre': {'$regex': nombre, '$options': 'i'}
        }))
        return [Producto.from_dict(producto) for producto in productos]
    
    def update_stock(self, cantidad):
        """Actualiza el stock del producto"""
        if self._id:
            db = get_db_connection()
            if db is None:
                raise Exception("Error de conexión a la base de datos")
            result = db.productos.update_one(
                {'_id': ObjectId(self._id)},
                {'$inc': {'stock': cantidad}}
            )
            if result.modified_count > 0:
                self.stock += cantidad
                return True
        return False
    
    def delete(self):
        """Elimina el producto de la base de datos"""
        if self._id:
            db = get_db_connection()
            if db is None:
                raise Exception("Error de conexión a la base de datos")
            result = db.productos.delete_one({'_id': ObjectId(self._id)})
            return result.deleted_count > 0
        return False 