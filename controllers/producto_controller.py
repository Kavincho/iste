from models.producto import Producto
from flask import jsonify, request

class ProductoController:
    
    @staticmethod
    def crear_producto():
        """Crea un nuevo producto"""
        try:
            data = request.json
            if not data:
                return jsonify({"error": "No se enviaron datos"}), 400
            
            # Validar datos requeridos
            nombre = data.get('nombre')
            precio = data.get('precio')
            
            if not nombre or precio is None:
                return jsonify({"error": "Nombre y precio son requeridos"}), 400
            
            # Validar que el precio sea un número positivo
            try:
                precio = float(precio)
                if precio < 0:
                    return jsonify({"error": "El precio debe ser positivo"}), 400
            except ValueError:
                return jsonify({"error": "El precio debe ser un número válido"}), 400
            
            # Crear producto
            producto = Producto(
                nombre=nombre,
                descripcion=data.get('descripcion', ''),
                precio=precio,
                stock=data.get('stock', 0),
                categoria=data.get('categoria', 'General'),
                imagen=data.get('imagen', '')
            )
            
            if producto.save():
                return jsonify({
                    "mensaje": f"Producto creado exitosamente: {nombre}",
                    "producto": {
                        "id": producto._id,
                        "nombre": producto.nombre,
                        "precio": producto.precio,
                        "stock": producto.stock,
                        "categoria": producto.categoria
                    }
                }), 201
            else:
                return jsonify({"error": "Error al guardar el producto"}), 500
                
        except Exception as e:
            return jsonify({"error": f"Error interno: {str(e)}"}), 500
    
    @staticmethod
    def obtener_productos():
        """Obtiene todos los productos"""
        try:
            productos = Producto.find_all()
            productos_data = []
            
            for producto in productos:
                productos_data.append({
                    "id": producto._id,
                    "nombre": producto.nombre,
                    "descripcion": producto.descripcion,
                    "precio": producto.precio,
                    "stock": producto.stock,
                    "categoria": producto.categoria,
                    "imagen": producto.imagen,
                    "fecha": producto.fecha.isoformat() if producto.fecha else None
                })
            
            return jsonify({
                "productos": productos_data,
                "total_registros": len(productos_data)
            }), 200
            
        except Exception as e:
            return jsonify({"error": f"Error interno: {str(e)}"}), 500
    
    @staticmethod
    def obtener_producto(producto_id):
        """Obtiene un producto específico"""
        try:
            producto = Producto.find_by_id(producto_id)
            if not producto:
                return jsonify({"error": "Producto no encontrado"}), 404
            
            return jsonify({
                "producto": {
                    "id": producto._id,
                    "nombre": producto.nombre,
                    "descripcion": producto.descripcion,
                    "precio": producto.precio,
                    "stock": producto.stock,
                    "categoria": producto.categoria,
                    "imagen": producto.imagen,
                    "fecha": producto.fecha.isoformat() if producto.fecha else None
                }
            }), 200
            
        except Exception as e:
            return jsonify({"error": f"Error interno: {str(e)}"}), 500
    
    @staticmethod
    def buscar_productos():
        """Busca productos por nombre"""
        try:
            nombre = request.args.get('q', '')
            if not nombre:
                return jsonify({"error": "Parámetro de búsqueda requerido"}), 400
            
            productos = Producto.search_by_name(nombre)
            productos_data = []
            
            for producto in productos:
                productos_data.append({
                    "id": producto._id,
                    "nombre": producto.nombre,
                    "descripcion": producto.descripcion,
                    "precio": producto.precio,
                    "stock": producto.stock,
                    "categoria": producto.categoria,
                    "imagen": producto.imagen
                })
            
            return jsonify({
                "productos": productos_data,
                "total_encontrados": len(productos_data),
                "busqueda": nombre
            }), 200
            
        except Exception as e:
            return jsonify({"error": f"Error interno: {str(e)}"}), 500
    
    @staticmethod
    def productos_por_categoria():
        """Obtiene productos por categoría"""
        try:
            categoria = request.args.get('categoria', '')
            if not categoria:
                return jsonify({"error": "Categoría requerida"}), 400
            
            productos = Producto.find_by_categoria(categoria)
            productos_data = []
            
            for producto in productos:
                productos_data.append({
                    "id": producto._id,
                    "nombre": producto.nombre,
                    "descripcion": producto.descripcion,
                    "precio": producto.precio,
                    "stock": producto.stock,
                    "categoria": producto.categoria,
                    "imagen": producto.imagen
                })
            
            return jsonify({
                "productos": productos_data,
                "total_en_categoria": len(productos_data),
                "categoria": categoria
            }), 200
            
        except Exception as e:
            return jsonify({"error": f"Error interno: {str(e)}"}), 500
    
    @staticmethod
    def actualizar_producto(producto_id):
        """Actualiza un producto existente"""
        try:
            data = request.json
            if not data:
                return jsonify({"error": "No se enviaron datos"}), 400
            
            # Verificar si el producto existe
            producto = Producto.find_by_id(producto_id)
            if not producto:
                return jsonify({"error": "Producto no encontrado"}), 404
            
            # Actualizar campos
            if 'nombre' in data:
                producto.nombre = data['nombre']
            if 'descripcion' in data:
                producto.descripcion = data['descripcion']
            if 'precio' in data:
                try:
                    precio = float(data['precio'])
                    if precio < 0:
                        return jsonify({"error": "El precio debe ser positivo"}), 400
                    producto.precio = precio
                except ValueError:
                    return jsonify({"error": "El precio debe ser un número válido"}), 400
            if 'stock' in data:
                producto.stock = data['stock']
            if 'categoria' in data:
                producto.categoria = data['categoria']
            if 'imagen' in data:
                producto.imagen = data['imagen']
            
            if producto.save():
                return jsonify({
                    "mensaje": "Producto actualizado correctamente",
                    "producto": {
                        "id": producto._id,
                        "nombre": producto.nombre,
                        "precio": producto.precio,
                        "stock": producto.stock,
                        "categoria": producto.categoria
                    }
                }), 200
            else:
                return jsonify({"error": "Error al actualizar el producto"}), 500
                
        except Exception as e:
            return jsonify({"error": f"Error interno: {str(e)}"}), 500
    
    @staticmethod
    def eliminar_producto(producto_id):
        """Elimina un producto"""
        try:
            # Verificar si el producto existe
            producto = Producto.find_by_id(producto_id)
            if not producto:
                return jsonify({"error": "Producto no encontrado"}), 404
            
            if producto.delete():
                return jsonify({
                    "mensaje": "Producto eliminado correctamente",
                    "id_eliminado": producto_id
                }), 200
            else:
                return jsonify({"error": "Error al eliminar el producto"}), 500
                
        except Exception as e:
            return jsonify({"error": f"Error interno: {str(e)}"}), 500 