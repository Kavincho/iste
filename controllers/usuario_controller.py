from models.usuario import Usuario
from flask import jsonify, request
import hashlib
import re

class UsuarioController:
    
    @staticmethod
    def crear_usuario():
        """Crea un nuevo usuario"""
        try:
            data = request.json
            if not data:
                return jsonify({"error": "No se enviaron datos"}), 400
            
            # Validar datos requeridos
            nombre = data.get('nombre')
            email = data.get('email')
            password = data.get('password')
            
            if not nombre or not email or not password:
                return jsonify({"error": "Nombre, email y password son requeridos"}), 400
            
            # Validar formato de email
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return jsonify({"error": "Formato de email inválido"}), 400
            
            # Verificar si el email ya existe
            usuario_existente = Usuario.find_by_email(email)
            if usuario_existente:
                return jsonify({"error": "El email ya está registrado"}), 400
            
            # Encriptar password (en producción usar bcrypt)
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            # Crear usuario
            usuario = Usuario(
                nombre=nombre,
                email=email,
                password=password_hash
            )
            
            if usuario.save():
                return jsonify({
                    "mensaje": f"Usuario creado exitosamente: {nombre}",
                    "usuario": {
                        "id": usuario._id,
                        "nombre": usuario.nombre,
                        "email": usuario.email
                    }
                }), 201
            else:
                return jsonify({"error": "Error al guardar el usuario"}), 500
                
        except Exception as e:
            return jsonify({"error": f"Error interno: {str(e)}"}), 500
    
    @staticmethod
    def obtener_usuarios():
        """Obtiene todos los usuarios"""
        try:
            usuarios = Usuario.find_all()
            usuarios_data = []
            
            for usuario in usuarios:
                usuarios_data.append({
                    "id": usuario._id,
                    "nombre": usuario.nombre,
                    "email": usuario.email,
                    "fecha": usuario.fecha.isoformat() if usuario.fecha else None
                })
            
            return jsonify({
                "usuarios": usuarios_data,
                "total_registros": len(usuarios_data)
            }), 200
            
        except Exception as e:
            return jsonify({"error": f"Error interno: {str(e)}"}), 500
    
    @staticmethod
    def obtener_usuario(usuario_id):
        """Obtiene un usuario específico"""
        try:
            usuario = Usuario.find_by_id(usuario_id)
            if not usuario:
                return jsonify({"error": "Usuario no encontrado"}), 404
            
            return jsonify({
                "usuario": {
                    "id": usuario._id,
                    "nombre": usuario.nombre,
                    "email": usuario.email,
                    "fecha": usuario.fecha.isoformat() if usuario.fecha else None
                }
            }), 200
            
        except Exception as e:
            return jsonify({"error": f"Error interno: {str(e)}"}), 500
    
    @staticmethod
    def eliminar_usuario(usuario_id):
        """Elimina un usuario"""
        try:
            # Verificar si el usuario existe
            usuario = Usuario.find_by_id(usuario_id)
            if not usuario:
                return jsonify({"error": "Usuario no encontrado"}), 404
            
            if Usuario.delete_by_id(usuario_id):
                return jsonify({
                    "mensaje": "Usuario eliminado correctamente",
                    "id_eliminado": usuario_id
                }), 200
            else:
                return jsonify({"error": "Error al eliminar el usuario"}), 500
                
        except Exception as e:
            return jsonify({"error": f"Error interno: {str(e)}"}), 500
            
    
    @staticmethod
    def login():
        """Autentica un usuario"""
        try:
            data = request.json
            if not data:
                return jsonify({"error": "No se enviaron datos"}), 400
            
            email = data.get('email')
            password = data.get('password')
            
            if not email or not password:
                return jsonify({"error": "Email y password son requeridos"}), 400
            
            # Buscar usuario por email
            usuario = Usuario.find_by_email(email)
            if not usuario:
                return jsonify({"error": "Credenciales inválidas"}), 401
            
            # Verificar password
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            if usuario.password != password_hash:
                return jsonify({"error": "Credenciales inválidas"}), 401
            
            return jsonify({
                "mensaje": "Login exitoso",
                "usuario": {
                    "id": usuario._id,
                    "nombre": usuario.nombre,
                    "email": usuario.email
                }
            }), 200
            
        except Exception as e:
            return jsonify({"error": f"Error interno: {str(e)}"}), 500 