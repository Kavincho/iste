# 🏗️ Arquitectura MVC - E-commerce

## 📁 Estructura del Proyecto

```
server/
├── models/                 # 🗃️ Modelos (Datos y lógica de negocio)
│   ├── __init__.py
│   ├── usuario.py         # Modelo de Usuario
│   └── producto.py        # Modelo de Producto
├── controllers/           # 🎮 Controladores (Lógica de aplicación)
│   ├── __init__.py
│   ├── usuario_controller.py
│   └── producto_controller.py
├── database/             # 🗄️ Base de datos
│   ├── __init__.py
│   └── connection.py     # Conexión a MongoDB
├── views/                # 👁️ Vistas (Interfaz de usuario)
├── static/               # 📁 Archivos estáticos
│   ├── css/
│   └── js/
├── templates/            # 📄 Plantillas HTML
├── app.py               # 🚀 Aplicación principal con arquitectura MVC
└── README_MVC.md        # 📖 Esta documentación
```

## 🎯 ¿Qué es MVC?

### **Modelo (Model)**
- **Representa los datos** y la lógica de negocio
- **Se conecta con la base de datos**
- **Contiene las reglas** del negocio
- **Ejemplo:** `Usuario`, `Producto`

### **Vista (View)**
- **Muestra la información** al usuario
- **Interfaz de usuario** (HTML, CSS, JS)
- **No contiene lógica** de negocio
- **Ejemplo:** Páginas web, formularios

### **Controlador (Controller)**
- **Recibe las peticiones** del usuario
- **Coordina** entre Modelo y Vista
- **Procesa** la lógica de la aplicación
- **Ejemplo:** `UsuarioController`, `ProductoController`

## 🚀 Cómo usar la nueva arquitectura

### **1. Iniciar la aplicación:**
```bash
python app.py
```

### **2. Endpoints disponibles:**

#### **Usuarios:**
- `POST /api/usuarios` - Crear usuario
- `GET /api/usuarios` - Obtener todos los usuarios
- `GET /api/usuarios/<id>` - Obtener usuario específico
- `DELETE /api/usuarios/<id>` - Eliminar usuario
- `POST /api/login` - Autenticar usuario

#### **Productos:**
- `POST /api/productos` - Crear producto
- `GET /api/productos` - Obtener todos los productos
- `GET /api/productos/<id>` - Obtener producto específico
- `PUT /api/productos/<id>` - Actualizar producto
- `DELETE /api/productos/<id>` - Eliminar producto
- `GET /api/productos/buscar?q=nombre` - Buscar productos
- `GET /api/productos/categoria?categoria=nombre` - Productos por categoría

#### **Compatibilidad:**
- Las rutas antiguas siguen funcionando (`/usuario`, `/numeros`, etc.)

## 🔧 Ventajas de MVC

### **✅ Separación de responsabilidades:**
- **Modelo:** Solo maneja datos
- **Vista:** Solo muestra información
- **Controlador:** Solo procesa lógica

### **✅ Mantenibilidad:**
- Código más organizado
- Fácil de modificar
- Fácil de probar

### **✅ Escalabilidad:**
- Fácil agregar nuevas funcionalidades
- Fácil cambiar tecnologías
- Fácil trabajar en equipo

### **✅ Reutilización:**
- Modelos se pueden usar en diferentes vistas
- Controladores se pueden usar en diferentes contextos

## 📝 Ejemplo de uso

### **Crear un usuario:**
```bash
curl -X POST http://localhost:5000/api/usuarios \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez",
    "email": "juan@ejemplo.com",
    "password": "123456"
  }'
```

### **Crear un producto:**
```bash
curl -X POST http://localhost:5000/api/productos \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Laptop Gaming",
    "descripcion": "Laptop para juegos",
    "precio": 999.99,
    "stock": 10,
    "categoria": "Electrónicos"
  }'
```

### **Buscar productos:**
```bash
curl "http://localhost:5000/api/productos/buscar?q=laptop"
```

## 🔄 Migración desde la estructura anterior

### **Antes (Sin MVC):**
```python
# Todo mezclado en app.py
@app.route('/usuario', methods=['POST'])
def guardar_usuario():
    data = request.json
    # Lógica de validación
    # Lógica de base de datos
    # Lógica de respuesta
    return jsonify(...)
```

### **Ahora (Con MVC):**
```python
# app_mvc.py - Solo rutas
@app.route('/api/usuarios', methods=['POST'])
def crear_usuario():
    return UsuarioController.crear_usuario()

# controllers/usuario_controller.py - Lógica de negocio
class UsuarioController:
    @staticmethod
    def crear_usuario():
        # Lógica de validación
        # Lógica de respuesta

# models/usuario.py - Datos
class Usuario:
    def save(self):
        # Lógica de base de datos
```

## 🎯 Próximos pasos

1. **Crear vistas HTML** para el frontend
2. **Agregar autenticación** con JWT
3. **Implementar carrito de compras**
4. **Agregar sistema de pedidos**
5. **Integrar pasarela de pagos**
6. **Agregar funcionalidades de IA**

## 🛠️ Tecnologías utilizadas

- **Backend:** Python + Flask
- **Base de datos:** MongoDB
- **Arquitectura:** MVC (Model-View-Controller)
- **CORS:** Habilitado para frontend
- **Validación:** En controladores
- **Serialización:** JSON automático

---

**¡Tu aplicación ahora tiene una arquitectura profesional y escalable! 🎉** 