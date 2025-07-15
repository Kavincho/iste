#!/usr/bin/env python3
"""
Script para agregar imágenes online a los productos en MongoDB automáticamente.
"""
from database.connection import get_db_connection

# Lista de URLs de imágenes para productos de ejemplo
imagenes = [
    "https://m.media-amazon.com/images/I/71bs7yw8FXL._AC_SL1500_.jpg",
    "https://imagenes.elpais.com/resizer/v2/GZDPJ4IFLPZZEAUWECHD7CRLA4.jpg?auth=176c483a064a78884d299c47454216fe3edd49778d6cbb762cfe29ad234824ac&width=1960&height=1470&smart=true",
    "https://media.istockphoto.com/id/1211554164/es/foto/3d-render-de-conjunto-de-recogida-de-electrodom%C3%A9sticos.jpg?s=612x612&w=0&k=20&c=Z2IF4UM4KFUJv4MUAskM5zOW6y22BMrehrxQLIzgtek=",
    "https://elcomercio.pe/resizer/Z3AP_3z2Jrz220JMLqfvmlKQsz4=/1200x789/smart/filters:format(jpeg):quality(75)/cloudfront-us-east-1.images.arcpublishing.com/elcomercio/P3WHG7NNS5DH7PDBGAMSHSLSWE.png",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTCmi2PMPyDyqWAsYkVqSsLPSJaVeSYMTX0KA&s",
    "https://image.made-in-china.com/202f0j00kemoHRAypqcv/New-Rotating-Button-Mecha-Transformers-Sneakers-Breathable-Casual-Dad-Shoes.webp",
    "https://imagenes.elpais.com/resizer/v2/E5X7AJQT7VELBLJUUEUMP6TRIM.jpg?auth=529575421d933beec6b3f55f8e98c8e4b3f184e8064119570aadbaeffaa1ce32&width=414",
    "https://www.infobae.com/new-resizer/OhxgfQPKyWQXqUU5QxoNEwSmkUQ=/arc-anglerfish-arc2-prod-infobae/public/FWQC6LQJ7FCAXHOH3OMXKLCAAQ.jpg",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTZEhAZkyuGqM0qUatm_RpjI9R6KGrfb1fQzg&s",
    "https://resources.news.e.abb.com/images/2024/3/19/1/AUAR_Robotic_Assembly_1_no_logo.jpg"
]

imagen_por_defecto = "https://m.media-amazon.com/images/I/71bs7yw8FXL._AC_SL1500_.jpg"

def agregar_imagenes():
    db = get_db_connection()
    if db is None:
        print("❌ No se pudo conectar a la base de datos.")
        return
    productos = list(db.productos.find())
    if not productos:
        print("No hay productos en la base de datos.")
        return
    print(f"Se encontraron {len(productos)} productos. Actualizando...")
    for idx, producto in enumerate(productos):
        url_img = imagenes[idx] if idx < len(imagenes) else imagen_por_defecto
        result = db.productos.update_one(
            {"_id": producto["_id"]},
            {"$set": {"imagen": url_img}}
        )
        print(f"Producto: {producto.get('nombre', 'Sin nombre')} - Imagen asignada: {url_img}")
    print("✅ Imágenes agregadas correctamente a todos los productos.")

if __name__ == "__main__":
    agregar_imagenes() 