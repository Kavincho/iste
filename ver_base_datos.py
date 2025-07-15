#!/usr/bin/env python3
"""
Script para ver el contenido de la base de datos MongoDB
"""

from database.connection import get_db_connection
from bson import ObjectId
import json

def mostrar_usuarios():
    """Muestra todos los usuarios en la base de datos"""
    print("\n👥 USUARIOS EN LA BASE DE DATOS")
    print("=" * 50)
    
    db = get_db_connection()
    if db is None:
        print("❌ Error: No se pudo conectar a la base de datos")
        return
    
    usuarios = list(db.usuarios.find())
    
    if not usuarios:
        print("📭 No hay usuarios registrados")
        return
    
    for i, usuario in enumerate(usuarios, 1):
        print(f"\n🔹 Usuario {i}:")
        print(f"   ID: {usuario['_id']}")
        print(f"   Nombre: {usuario.get('nombre', 'N/A')}")
        print(f"   Email: {usuario.get('email', 'N/A')}")
        print(f"   Fecha: {usuario.get('fecha', 'N/A')}")
        print(f"   Password: {'*' * len(usuario.get('password', ''))}")

def mostrar_productos():
    """Muestra todos los productos en la base de datos"""
    print("\n🛍️ PRODUCTOS EN LA BASE DE DATOS")
    print("=" * 50)
    
    db = get_db_connection()
    if db is None:
        print("❌ Error: No se pudo conectar a la base de datos")
        return
    
    productos = list(db.productos.find())
    
    if not productos:
        print("📭 No hay productos registrados")
        return
    
    for i, producto in enumerate(productos, 1):
        print(f"\n🔹 Producto {i}:")
        print(f"   ID: {producto['_id']}")
        print(f"   Nombre: {producto.get('nombre', 'N/A')}")
        print(f"   Descripción: {producto.get('descripcion', 'N/A')}")
        print(f"   Precio: ${producto.get('precio', 0):.2f}")
        print(f"   Stock: {producto.get('stock', 0)}")
        print(f"   Categoría: {producto.get('categoria', 'N/A')}")
        print(f"   Fecha: {producto.get('fecha', 'N/A')}")

def mostrar_numeros():
    """Muestra todos los números en la base de datos"""
    print("\n🔢 NÚMEROS EN LA BASE DE DATOS")
    print("=" * 50)
    
    db = get_db_connection()
    if db is None:
        print("❌ Error: No se pudo conectar a la base de datos")
        return
    
    numeros = list(db.numeros.find())
    
    if not numeros:
        print("📭 No hay números registrados")
        return
    
    for i, numero in enumerate(numeros, 1):
        print(f"\n🔹 Número {i}:")
        print(f"   ID: {numero['_id']}")
        print(f"   Iteraciones: {numero.get('iteraciones', 'N/A')}")
        print(f"   Fecha: {numero.get('fecha', 'N/A')}")

def mostrar_estadisticas():
    """Muestra estadísticas de la base de datos"""
    print("\n📊 ESTADÍSTICAS DE LA BASE DE DATOS")
    print("=" * 50)
    
    db = get_db_connection()
    if db is None:
        print("❌ Error: No se pudo conectar a la base de datos")
        return
    
    # Contar documentos en cada colección
    total_usuarios = db.usuarios.count_documents({})
    total_productos = db.productos.count_documents({})
    total_numeros = db.numeros.count_documents({})
    
    print(f"👥 Total de usuarios: {total_usuarios}")
    print(f"🛍️ Total de productos: {total_productos}")
    print(f"🔢 Total de números: {total_numeros}")
    
    # Mostrar colecciones disponibles
    colecciones = db.list_collection_names()
    print(f"\n📁 Colecciones disponibles: {', '.join(colecciones)}")

def buscar_por_id():
    """Busca un documento específico por ID"""
    print("\n🔍 BUSCAR POR ID")
    print("=" * 50)
    
    tipo = input("Tipo de documento (usuarios/productos/numeros): ").lower()
    id_buscar = input("ID a buscar: ")
    
    if not tipo or not id_buscar:
        print("❌ Debes especificar tipo e ID")
        return
    
    db = get_db_connection()
    if db is None:
        print("❌ Error: No se pudo conectar a la base de datos")
        return
    
    try:
        if tipo == "usuarios":
            coleccion = db.usuarios
        elif tipo == "productos":
            coleccion = db.productos
        elif tipo == "numeros":
            coleccion = db.numeros
        else:
            print("❌ Tipo de documento no válido")
            return
        
        documento = coleccion.find_one({'_id': ObjectId(id_buscar)})
        
        if documento:
            print(f"\n✅ Documento encontrado:")
            print(json.dumps(documento, default=str, indent=2))
        else:
            print("❌ Documento no encontrado")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def menu_principal():
    """Menú principal del script"""
    while True:
        print("\n" + "=" * 60)
        print("🗄️ VISOR DE BASE DE DATOS MONGODB")
        print("=" * 60)
        print("1. 👥 Ver usuarios")
        print("2. 🛍️ Ver productos")
        print("3. 🔢 Ver números")
        print("4. 📊 Ver estadísticas")
        print("5. 🔍 Buscar por ID")
        print("6. 🚪 Salir")
        print("=" * 60)
        
        opcion = input("\nSelecciona una opción (1-6): ")
        
        if opcion == "1":
            mostrar_usuarios()
        elif opcion == "2":
            mostrar_productos()
        elif opcion == "3":
            mostrar_numeros()
        elif opcion == "4":
            mostrar_estadisticas()
        elif opcion == "5":
            buscar_por_id()
        elif opcion == "6":
            print("\n👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción no válida. Intenta de nuevo.")
        
        input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    print("🚀 Iniciando visor de base de datos...")
    menu_principal() 