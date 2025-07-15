# 🚀 API REST con Flask y MongoDB

Una aplicación web moderna construida con **Flask** y **MongoDB** siguiendo el patrón **MVC** (Model-View-Controller).

## ✨ Características

- **Arquitectura MVC**: Separación clara de responsabilidades
- **API REST**: Endpoints para CRUD de usuarios y productos
- **Base de datos MongoDB**: Almacenamiento flexible y escalable
- **CORS habilitado**: Compatible con aplicaciones frontend
- **Manejo de errores mejorado**: Validaciones robustas de conexión
- **Variables de entorno**: Configuración segura y flexible

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
git clone <tu-repositorio>
cd server
```

### 2. Crear entorno virtual
```bash
python -m venv venv
```

### 3. Activar entorno virtual
**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5. Configurar variables de entorno
Crea un archivo `.env` en la raíz del proyecto:

```env
# Configuración de la base de datos MongoDB
MONGO_URI=mongodb://localhost:27017/
DATABASE_NAME=ecommerce_db

# Configuración de la aplicación Flask
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=tu_clave_secreta_aqui

# Configuración del servidor
HOST=localhost
PORT=5000
```

### 6. Iniciar MongoDB
Asegúrate de que MongoDB esté ejecutándose en tu sistema.

### 7. Ejecutar la aplicación
```bash
python app.py
```

La aplicación estará disponible en: http://localhost:5000

## 📊 Estructura del Proyecto

```
server/
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias de Python
├── .env                  # Variables de entorno (crear manualmente)
├── controllers/          # Controladores MVC
│   ├── usuario_controller.py
│   └── producto_controller.py
├── models/              # Modelos de datos
│   ├── usuario.py
│   └── producto.py
├── database/            # Configuración de base de datos
│   └── connection.py
├── templates/           # Plantillas HTML
│   └── index.html
├── static/             # Archivos estáticos
│   ├── css/
│   └── js/
└── views/              # Vistas (si se implementan)
```

## 🔧 API Endpoints

### Usuarios
- `POST /api/usuarios` - Crear usuario
- `GET /api/usuarios` - Obtener todos los usuarios
- `GET /api/usuarios/<id>` - Obtener usuario por ID
- `DELETE /api/usuarios/<id>` - Eliminar usuario
- `POST /api/login` - Iniciar sesión

### Productos
- `POST /api/productos` - Crear producto
- `GET /api/productos` - Obtener todos los productos
- `GET /api/productos/<id>` - Obtener producto por ID
- `PUT /api/productos/<id>` - Actualizar producto
- `DELETE /api/productos/<id>` - Eliminar producto
- `GET /api/productos/buscar` - Buscar productos por nombre
- `GET /api/productos/categoria` - Productos por categoría

### Utilidades
- `GET /api/health` - Estado de la API
- `GET /` - Página principal (Frontend)
- `GET /test` - Prueba simple

## 🐛 Correcciones Recientes

### Errores de Linter Corregidos
- ✅ **Validación de conexión a BD**: Agregadas validaciones para verificar que `db` no sea `None`
- ✅ **Manejo de excepciones**: Mejorado el manejo de errores en modelos
- ✅ **Variables de entorno**: Implementado soporte para archivos `.env`
- ✅ **Verificación de conexión**: Agregado ping a MongoDB para verificar conectividad

### Archivos Modificados
- `models/usuario.py` - Validaciones de conexión agregadas
- `models/producto.py` - Validaciones de conexión agregadas
- `database/connection.py` - Soporte para variables de entorno
- `app.py` - Mejor manejo de errores de inicialización
- `requirements.txt` - Agregada dependencia `python-dotenv`

## 🔍 Solución de Problemas

### Error de Conexión a MongoDB
Si ves el mensaje "Error de conexión a la base de datos":
1. Verifica que MongoDB esté ejecutándose
2. Comprueba la URI en el archivo `.env`
3. Asegúrate de que el puerto 27017 esté disponible

### Variables de Entorno
Si las variables de entorno no se cargan:
1. Verifica que el archivo `.env` esté en la raíz del proyecto
2. Asegúrate de que `python-dotenv` esté instalado
3. Reinicia la aplicación después de modificar `.env`

## 🚀 Próximos Pasos

- [ ] Implementar autenticación JWT
- [ ] Agregar validación de datos con Marshmallow
- [ ] Implementar tests unitarios
- [ ] Agregar documentación con Swagger
- [ ] Implementar logging estructurado

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. 