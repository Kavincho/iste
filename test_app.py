#!/usr/bin/env python3
"""
Script de prueba para verificar que la aplicación funciona correctamente
"""

import requests
import time

def test_app():
    """Prueba las rutas principales de la aplicación"""
    
    base_url = "http://localhost:5000"
    
    print("🧪 Probando la aplicación...")
    print("=" * 50)
    
    # Probar ruta de prueba simple
    try:
        response = requests.get(f"{base_url}/test", timeout=5)
        if response.status_code == 200:
            print("✅ Ruta /test funciona correctamente")
        else:
            print(f"❌ Ruta /test falló: {response.status_code}")
    except Exception as e:
        print(f"❌ Error al probar /test: {str(e)}")
    
    # Probar ruta principal
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Ruta principal (/) funciona correctamente")
            if "E-Commerce" in response.text:
                print("✅ HTML se está cargando correctamente")
            else:
                print("⚠️ HTML cargado pero contenido inesperado")
        else:
            print(f"❌ Ruta principal falló: {response.status_code}")
            print(f"Respuesta: {response.text}")
    except Exception as e:
        print(f"❌ Error al probar ruta principal: {str(e)}")
    
    # Probar API de productos
    try:
        response = requests.get(f"{base_url}/api/productos", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API de productos funciona: {len(data.get('productos', []))} productos encontrados")
        else:
            print(f"❌ API de productos falló: {response.status_code}")
    except Exception as e:
        print(f"❌ Error al probar API de productos: {str(e)}")
    
    # Probar API de health
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ API de health funciona correctamente")
        else:
            print(f"❌ API de health falló: {response.status_code}")
    except Exception as e:
        print(f"❌ Error al probar API de health: {str(e)}")
    
    print("=" * 50)
    print("🎯 Instrucciones:")
    print("1. Abre tu navegador")
    print("2. Ve a: http://localhost:5000")
    print("3. Si no funciona, prueba: http://127.0.0.1:5000")
    print("4. También puedes probar: http://localhost:5000/test")

if __name__ == "__main__":
    # Esperar un poco para que la app se inicie
    print("⏳ Esperando 3 segundos para que la aplicación se inicie...")
    time.sleep(3)
    test_app() 