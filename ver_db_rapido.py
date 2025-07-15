#!/usr/bin/env python3
"""
Script rápido para ver el contenido de la base de datos
"""

from database.connection import get_db_connection

def ver_base_datos_rapido():
    """Muestra rápidamente el contenido de la base de datos"""
    print("🗄️ CONTENIDO DE LA BASE DE DATOS")
    print("=" * 50)
    
    db = get_db_connection()
    if db is None:
        print("❌ Error: No se pudo conectar a la base de datos")
        return
    
    # Estadísticas generales
    total_usuarios = db.usuarios.count_documents({})
    total_productos = db.productos.count_documents({})
    total_numeros = db.numeros.count_documents({})
    
    print(f"👥 Usuarios: {total_usuarios}")
    print(f"🛍️ Productos: {total_productos}")
    print(f"🔢 Números: {total_numeros}")
    
    # Mostrar algunos usuarios
    if total_usuarios > 0:
        print(f"\n👥 ÚLTIMOS USUARIOS:")
        usuarios = list(db.usuarios.find().limit(3))
        for usuario in usuarios:
            print(f"   • {usuario.get('nombre', 'N/A')} - {usuario.get('email', 'N/A')}")
    
    # Mostrar algunos productos
    if total_productos > 0:
        print(f"\n🛍️ PRODUCTOS DISPONIBLES:")
        productos = list(db.productos.find().limit(5))
        for producto in productos:
            print(f"   • {producto.get('nombre', 'N/A')} - ${producto.get('precio', 0):.2f} - Stock: {producto.get('stock', 0)}")
    
    # Mostrar algunos números
    if total_numeros > 0:
        print(f"\n🔢 ÚLTIMOS NÚMEROS:")
        numeros = list(db.numeros.find().limit(3))
        for numero in numeros:
            print(f"   • Iteraciones: {numero.get('iteraciones', 'N/A')} - Fecha: {numero.get('fecha', 'N/A')}")

if __name__ == "__main__":
    ver_base_datos_rapido() 