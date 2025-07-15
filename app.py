from flask import Flask, jsonify, render_template
from flask_cors import CORS
from controllers.usuario_controller import UsuarioController
from controllers.producto_controller import ProductoController
from database.connection import init_database
import datetime

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)

# Inicializar la base de datos
if not init_database():
    print("(0.0)  Advertencia: No se pudo inicializar la base de datos. Algunas funcionalidades pueden no estar disponibles.")

# ===== RUTAS DE USUARIOS =====
@app.route('/api/usuarios', methods=['POST'])
def crear_usuario():
    return UsuarioController.crear_usuario()

@app.route('/api/usuarios', methods=['GET'])
def obtener_usuarios():
    return UsuarioController.obtener_usuarios()

@app.route('/api/usuarios/<usuario_id>', methods=['GET'])
def obtener_usuario(usuario_id):
    return UsuarioController.obtener_usuario(usuario_id)

@app.route('/api/usuarios/<usuario_id>', methods=['DELETE'])
def eliminar_usuario(usuario_id):
    return UsuarioController.eliminar_usuario(usuario_id)

@app.route('/api/login', methods=['POST'])
def login():
    return UsuarioController.login()

# ===== RUTAS DE PRODUCTOS =====
@app.route('/api/productos', methods=['POST'])
def crear_producto():
    return ProductoController.crear_producto()

@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    return ProductoController.obtener_productos()

@app.route('/api/productos/<producto_id>', methods=['GET'])
def obtener_producto(producto_id):
    return ProductoController.obtener_producto(producto_id)

@app.route('/api/productos/<producto_id>', methods=['PUT'])
def actualizar_producto(producto_id):
    return ProductoController.actualizar_producto(producto_id)

@app.route('/api/productos/<producto_id>', methods=['DELETE'])
def eliminar_producto(producto_id):
    return ProductoController.eliminar_producto(producto_id)

@app.route('/api/productos/buscar', methods=['GET'])
def buscar_productos():
    return ProductoController.buscar_productos()

@app.route('/api/productos/categoria', methods=['GET'])
def productos_por_categoria():
    return ProductoController.productos_por_categoria()

# ===== RUTAS COMPATIBILIDAD (mantener las rutas antiguas) =====
@app.route('/usuario', methods=['POST'])
def guardar_usuario_old():
    return UsuarioController.crear_usuario()

@app.route('/usuario', methods=['GET'])
def obtener_usuario_old():
    return UsuarioController.obtener_usuarios()

@app.route('/usuario/<usuario_id>', methods=['DELETE'])
def eliminar_usuario_old(usuario_id):
    return UsuarioController.eliminar_usuario(usuario_id)

# Mantener la ruta de números para compatibilidad
@app.route('/numeros', methods=['GET'])
def obtener_numeros():
    from database.connection import get_db_connection
    db = get_db_connection()
    if db is None:
        return jsonify({"error": "Error de conexión a la base de datos"}), 500
    
    numeros_db = list(db.numeros.find())
    
    # Convertir ObjectId a string para que sea JSON serializable
    for numero in numeros_db:
        if '_id' in numero:
            numero['_id'] = str(numero['_id'])
    
    return jsonify({
        "numeros": numeros_db,
        "total_registros": len(numeros_db)
    })

@app.route('/mamadas', methods=['POST'])
def home():
    from database.connection import get_db_connection
    from flask import request
    
    data = request.json
    if not data or 'iteraciones' not in data:
        return jsonify({"error": "Debes enviar el número de iteraciones"}), 400
    
    numero_iteraciones = data['iteraciones']
    
    # Validar que sea un número válido
    try:
        numero_iteraciones = int(numero_iteraciones)
        if numero_iteraciones < 0:
            return jsonify({"error": "El número de iteraciones debe ser positivo"}), 400
    except ValueError:
        return jsonify({"error": "El número de iteraciones debe ser un número válido"}), 400
    
    # Almacenar en MongoDB
    db = get_db_connection()
    if db is None:
        return jsonify({"error": "Error de conexión a la base de datos"}), 500
    
    datos_numeros = {
        "iteraciones": numero_iteraciones,
        "fecha": datetime.datetime.now()
    }
    result_numeros = db.numeros.insert_one(datos_numeros)
    
    texto = ""
    for i in range(numero_iteraciones):
        texto += f"{i+1}\n"
        
    return jsonify({
        "resultado": texto,
        "iteraciones": numero_iteraciones,
        "mensaje": f"Iteraciones almacenadas en BD: {numero_iteraciones}",
        "id_numeros": str(result_numeros.inserted_id)
    })

# ===== RUTA DE PRUEBA =====
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "OK",
        "message": "API funcionando correctamente",
        "timestamp": datetime.datetime.now().isoformat()
    })

# ===== RUTA PRINCIPAL DEL FRONTEND =====
@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error al cargar template: {str(e)}", 500

# ===== RUTA ALTERNATIVA SIMPLE =====
@app.route('/simple')
def index_simple():
    try:
        return render_template('index_simple.html')
    except Exception as e:
        return f"Error al cargar template simple: {str(e)}", 500

# ===== RUTA DE PRUEBA SIMPLE =====
@app.route('/test')
def test():
    return "¡Flask está funcionando correctamente!"

# ===== RUTA DE PRUEBA DE TEMPLATE =====
@app.route('/test-template')
def test_template():
    try:
        return render_template('test.html')
    except Exception as e:
        return f"Error al cargar template de prueba: {str(e)}", 500

# ===== RUTA PARA VERIFICAR ARCHIVOS ESTÁTICOS =====
@app.route('/static-test')
def static_test():
    try:
        with open('test_static.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Archivo de prueba no encontrado", 404

if __name__ == '__main__':
    print("🚀 Iniciando aplicación con arquitectura MVC...")
    print("📊 Base de datos: MongoDB")
    print("🔧 Framework: Flask")
    print("🌐 CORS: Habilitado")
    print("📝 Endpoints disponibles:")
    print("   - GET  / - Página principal (Frontend)")
    print("   - POST /api/usuarios - Crear usuario")
    print("   - GET  /api/usuarios - Obtener usuarios")
    print("   - POST /api/productos - Crear producto")
    print("   - GET  /api/productos - Obtener productos")
    print("   - GET  /api/health - Estado de la API")
    print("\n✨ Aplicación lista en http://localhost:5000")
    app.run(debug=True) 