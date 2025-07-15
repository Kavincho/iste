#!/usr/bin/env python3
"""
Script de diagnóstico para verificar la configuración de Flask y archivos estáticos
"""

import os
import sys

def verificar_archivos():
    """Verifica que todos los archivos necesarios existan"""
    print("🔍 Verificando archivos...")
    
    archivos_requeridos = [
        'app.py',
        'templates/index.html',
        'templates/test.html',
        'templates/index_simple.html',
        'static/css/style.css',
        'static/js/app.js',
        'database/connection.py',
        'models/usuario.py',
        'models/producto.py',
        'controllers/usuario_controller.py',
        'controllers/producto_controller.py'
    ]
    
    archivos_faltantes = []
    for archivo in archivos_requeridos:
        if os.path.exists(archivo):
            print(f"✅ {archivo}")
        else:
            print(f"❌ {archivo} - NO ENCONTRADO")
            archivos_faltantes.append(archivo)
    
    return len(archivos_faltantes) == 0

def verificar_estructura():
    """Verifica la estructura de directorios"""
    print("\n📁 Verificando estructura de directorios...")
    
    directorios = ['templates', 'static', 'static/css', 'static/js', 'models', 'controllers', 'database']
    
    for directorio in directorios:
        if os.path.exists(directorio):
            print(f"✅ {directorio}/")
        else:
            print(f"❌ {directorio}/ - NO ENCONTRADO")

def verificar_dependencias():
    """Verifica que las dependencias estén instaladas"""
    print("\n📦 Verificando dependencias...")
    
    try:
        import flask
        print("✅ Flask")
    except ImportError:
        print("❌ Flask no está instalado")
        return False
    
    try:
        import flask_cors
        print("✅ Flask-CORS")
    except ImportError:
        print("❌ Flask-CORS no está instalado")
        return False
    
    try:
        import pymongo
        print("✅ PyMongo")
    except ImportError:
        print("❌ PyMongo no está instalado")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv")
    except ImportError:
        print("❌ python-dotenv no está instalado")
        return False
    
    return True

def verificar_configuracion_flask():
    """Verifica la configuración de Flask"""
    print("\n⚙️ Verificando configuración de Flask...")
    
    try:
        # Importar la aplicación Flask
        sys.path.append('.')
        from app import app
        
        print("✅ Aplicación Flask importada correctamente")
        
        # Verificar configuración de archivos estáticos
        if hasattr(app, 'static_folder'):
            print(f"✅ Carpeta estática configurada: {app.static_folder}")
        else:
            print("❌ Carpeta estática no configurada")
        
        if hasattr(app, 'static_url_path'):
            print(f"✅ URL path estático configurado: {app.static_url_path}")
        else:
            print("❌ URL path estático no configurado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al importar aplicación Flask: {e}")
        return False

def verificar_contenido_css():
    """Verifica el contenido del archivo CSS"""
    print("\n🎨 Verificando archivo CSS...")
    
    try:
        with open('static/css/style.css', 'r', encoding='utf-8') as f:
            contenido = f.read()
            
        if len(contenido) > 0:
            print(f"✅ CSS tiene {len(contenido)} caracteres")
            
            # Verificar algunas clases importantes
            clases_importantes = ['.header', '.navbar', '.hero', '.btn-primary', '.productos-grid']
            for clase in clases_importantes:
                if clase in contenido:
                    print(f"✅ Clase {clase} encontrada")
                else:
                    print(f"⚠️ Clase {clase} no encontrada")
        else:
            print("❌ Archivo CSS está vacío")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Error al leer archivo CSS: {e}")
        return False

def verificar_contenido_js():
    """Verifica el contenido del archivo JavaScript"""
    print("\n🔧 Verificando archivo JavaScript...")
    
    try:
        with open('static/js/app.js', 'r', encoding='utf-8') as f:
            contenido = f.read()
            
        if len(contenido) > 0:
            print(f"✅ JavaScript tiene {len(contenido)} caracteres")
            
            # Verificar algunas funciones importantes
            funciones_importantes = ['cargarProductos', 'mostrarProductos', 'agregarAlCarrito']
            for funcion in funciones_importantes:
                if funcion in contenido:
                    print(f"✅ Función {funcion} encontrada")
                else:
                    print(f"⚠️ Función {funcion} no encontrada")
        else:
            print("❌ Archivo JavaScript está vacío")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Error al leer archivo JavaScript: {e}")
        return False

def main():
    """Función principal del diagnóstico"""
    print("🚀 DIAGNÓSTICO DE LA APLICACIÓN FLASK")
    print("=" * 50)
    
    # Ejecutar todas las verificaciones
    archivos_ok = verificar_archivos()
    verificar_estructura()
    dependencias_ok = verificar_dependencias()
    flask_ok = verificar_configuracion_flask()
    css_ok = verificar_contenido_css()
    js_ok = verificar_contenido_js()
    
    # Resumen
    print("\n" + "=" * 50)
    print("📊 RESUMEN DEL DIAGNÓSTICO")
    print("=" * 50)
    
    if all([archivos_ok, dependencias_ok, flask_ok, css_ok, js_ok]):
        print("🎉 ¡Todo está configurado correctamente!")
        print("\n📝 Próximos pasos:")
        print("1. Ejecuta: python app.py")
        print("2. Abre: http://localhost:5000")
        print("3. Para pruebas: http://localhost:5000/test-template")
        print("4. Para versión simple: http://localhost:5000/simple")
    else:
        print("⚠️ Se encontraron algunos problemas:")
        if not archivos_ok:
            print("- Faltan algunos archivos requeridos")
        if not dependencias_ok:
            print("- Faltan algunas dependencias")
        if not flask_ok:
            print("- Problema con la configuración de Flask")
        if not css_ok:
            print("- Problema con el archivo CSS")
        if not js_ok:
            print("- Problema con el archivo JavaScript")
        
        print("\n🔧 Soluciones:")
        print("1. Instala dependencias: pip install -r requirements.txt")
        print("2. Verifica que todos los archivos estén en su lugar")
        print("3. Reinicia la aplicación después de los cambios")

if __name__ == "__main__":
    main() 