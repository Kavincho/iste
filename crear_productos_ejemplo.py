#!/usr/bin/env python3
"""
Script para crear productos de ejemplo en la base de datos
"""

from models.producto import Producto
from database.connection import init_database

def crear_productos_ejemplo():
    """Crea productos de ejemplo en la base de datos"""
    
    # Inicializar la base de datos
    init_database()
    
    # Lista de productos de ejemplo
    productos_ejemplo = [
        {
            "nombre": "iPhone 15 Pro",
            "descripcion": "El último iPhone con cámara profesional y chip A17 Pro",
            "precio": 999.99,
            "stock": 25,
            "categoria": "Electrónicos",
            "imagen": "iphone15.jpg"
        },
        {
            "nombre": "MacBook Air M2",
            "descripcion": "Laptop ultraportátil con chip M2 y hasta 18 horas de batería",
            "precio": 1199.99,
            "stock": 15,
            "categoria": "Electrónicos",
            "imagen": "macbook-air.jpg"
        },
        {
            "nombre": "Nike Air Max 270",
            "descripcion": "Zapatillas deportivas con tecnología Air Max para máximo confort",
            "precio": 129.99,
            "stock": 50,
            "categoria": "Deportes",
            "imagen": "nike-airmax.jpg"
        },
        {
            "nombre": "Samsung 4K Smart TV",
            "descripcion": "Televisor 55 pulgadas con resolución 4K y Smart TV integrado",
            "precio": 699.99,
            "stock": 10,
            "categoria": "Electrónicos",
            "imagen": "samsung-tv.jpg"
        },
        {
            "nombre": "Camiseta Básica",
            "descripcion": "Camiseta de algodón 100% en varios colores y tallas",
            "precio": 19.99,
            "stock": 100,
            "categoria": "Ropa",
            "imagen": "camiseta-basica.jpg"
        },
        {
            "nombre": "Juego de Sábanas",
            "descripcion": "Sábanas de algodón egipcio, 1000 hilos, varios colores",
            "precio": 89.99,
            "stock": 30,
            "categoria": "Hogar",
            "imagen": "sabanas.jpg"
        },
        {
            "nombre": "Pelota de Fútbol",
            "descripcion": "Pelota oficial de fútbol profesional, tamaño 5",
            "precio": 45.99,
            "stock": 40,
            "categoria": "Deportes",
            "imagen": "pelota-futbol.jpg"
        },
        {
            "nombre": "Cafetera Express",
            "descripcion": "Cafetera automática con molinillo integrado y espumador de leche",
            "precio": 299.99,
            "stock": 20,
            "categoria": "Hogar",
            "imagen": "cafetera.jpg"
        },
        {
            "nombre": "Jeans Clásicos",
            "descripcion": "Jeans de denim premium con corte clásico y lavado vintage",
            "precio": 79.99,
            "stock": 60,
            "categoria": "Ropa",
            "imagen": "jeans.jpg"
        },
        {
            "nombre": "Auriculares Bluetooth",
            "descripcion": "Auriculares inalámbricos con cancelación de ruido activa",
            "precio": 159.99,
            "stock": 35,
            "categoria": "Electrónicos",
            "imagen": "auriculares.jpg"
        }
    ]
    
    # Crear cada producto
    productos_creados = 0
    for producto_data in productos_ejemplo:
        try:
            producto = Producto(
                nombre=producto_data["nombre"],
                descripcion=producto_data["descripcion"],
                precio=producto_data["precio"],
                stock=producto_data["stock"],
                categoria=producto_data["categoria"],
                imagen=producto_data["imagen"]
            )
            
            if producto.save():
                productos_creados += 1
                print(f"✅ Producto creado: {producto.nombre}")
            else:
                print(f"❌ Error al crear: {producto.nombre}")
                
        except Exception as e:
            print(f"❌ Error al crear {producto_data['nombre']}: {str(e)}")
    
    print(f"\n🎉 Se crearon {productos_creados} productos de ejemplo exitosamente!")
    print("🌐 Ahora puedes visitar http://localhost:5000 para ver tu tienda")

if __name__ == "__main__":
    print("🚀 Creando productos de ejemplo...")
    crear_productos_ejemplo() 