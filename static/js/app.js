// Variables globales
let productos = [];
let carrito = [];
let usuarioActual = null;

// API Base URL
const API_BASE = '/api';

// Inicialización cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    cargarProductos();
    cargarCarritoDesdeStorage();
    actualizarContadorCarrito();
    
    // Event listeners
    document.getElementById('searchInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            buscarProductos();
        }
    });
});

// ===== FUNCIONES DE PRODUCTOS =====

async function cargarProductos() {
    try {
        mostrarLoading(true);
        const response = await fetch(`${API_BASE}/productos`);
        const data = await response.json();
        
        if (response.ok) {
            productos = data.productos;
            mostrarProductos(productos);
        } else {
            mostrarError('Error al cargar productos: ' + data.error);
        }
    } catch (error) {
        mostrarError('Error de conexión: ' + error.message);
    } finally {
        mostrarLoading(false);
    }
}

function mostrarProductos(productosAMostrar) {
    const grid = document.getElementById('productosGrid');
    
    if (productosAMostrar.length === 0) {
        grid.innerHTML = `
            <div class="no-productos">
                <i class="fas fa-search"></i>
                <h3>No se encontraron productos</h3>
                <p>Intenta con otros términos de búsqueda</p>
            </div>
        `;
        return;
    }
    
    grid.innerHTML = productosAMostrar.map(producto => `
        <div class="producto-card">
            <div class="producto-imagen">
                <img src="${producto.imagen || 'https://m.media-amazon.com/images/I/71bs7yw8FXL._AC_SL1500_.jpg'}" alt="${producto.nombre}" style="width:100%;height:200px;object-fit:cover;">
            </div>
            <div class="producto-info">
                <h3 class="producto-nombre">${producto.nombre}</h3>
                <p class="producto-descripcion">${producto.descripcion || 'Sin descripción'}</p>
                <div class="producto-precio">$${producto.precio.toFixed(2)}</div>
                <div class="producto-stock">
                    <i class="fas fa-check-circle"></i>
                    Stock: ${producto.stock} unidades
                </div>
                <div class="producto-acciones">
                    <button class="btn-agregar" onclick="agregarAlCarrito('${producto.id}', '${producto.nombre}', ${producto.precio})">
                        <i class="fas fa-cart-plus"></i>
                        Agregar
                    </button>
                    <button class="btn-detalles" onclick="verDetallesProducto('${producto.id}')">
                        <i class="fas fa-eye"></i>
                        Detalles
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

async function buscarProductos() {
    const query = document.getElementById('searchInput').value.trim();
    
    if (!query) {
        cargarProductos();
        return;
    }
    
    try {
        mostrarLoading(true);
        const response = await fetch(`${API_BASE}/productos/buscar?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        
        if (response.ok) {
            mostrarProductos(data.productos);
        } else {
            mostrarError('Error en la búsqueda: ' + data.error);
        }
    } catch (error) {
        mostrarError('Error de conexión: ' + error.message);
    } finally {
        mostrarLoading(false);
    }
}

async function filtrarPorCategoria() {
    const categoria = document.getElementById('categoriaSelect').value;
    
    if (!categoria) {
        cargarProductos();
        return;
    }
    
    try {
        mostrarLoading(true);
        const response = await fetch(`${API_BASE}/productos/categoria?categoria=${encodeURIComponent(categoria)}`);
        const data = await response.json();
        
        if (response.ok) {
            mostrarProductos(data.productos);
        } else {
            mostrarError('Error al filtrar: ' + data.error);
        }
    } catch (error) {
        mostrarError('Error de conexión: ' + error.message);
    } finally {
        mostrarLoading(false);
    }
}

async function verDetallesProducto(productoId) {
    try {
        const response = await fetch(`${API_BASE}/productos/${productoId}`);
        const data = await response.json();
        
        if (response.ok) {
            const producto = data.producto;
            mostrarModalDetalles(producto);
        } else {
            mostrarError('Error al cargar detalles: ' + data.error);
        }
    } catch (error) {
        mostrarError('Error de conexión: ' + error.message);
    }
}

function mostrarModalDetalles(producto) {
    const modalHTML = `
        <div class="modal" id="detallesModal">
            <div class="modal-content">
                <div class="modal-header">
                    <h3>${producto.nombre}</h3>
                    <button class="close-btn" onclick="cerrarModal('detallesModal')">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="modal-body">
                    <div class="producto-detalles">
                        <div class="producto-imagen-grande">
                            <img src="${producto.imagen || 'https://m.media-amazon.com/images/I/71bs7yw8FXL._AC_SL1500_.jpg'}" alt="${producto.nombre}" style="width:100%;height:300px;object-fit:cover;border-radius:15px;">
                        </div>
                        <div class="producto-info-detallada">
                            <h4>Descripción:</h4>
                            <p>${producto.descripcion || 'Sin descripción disponible'}</p>
                            <h4>Precio:</h4>
                            <p class="precio-grande">$${producto.precio.toFixed(2)}</p>
                            <h4>Stock:</h4>
                            <p>${producto.stock} unidades disponibles</p>
                            <h4>Categoría:</h4>
                            <p>${producto.categoria}</p>
                            <button class="btn-primary" onclick="agregarAlCarrito('${producto.id}', '${producto.nombre}', ${producto.precio}); cerrarModal('detallesModal')">
                                <i class="fas fa-cart-plus"></i>
                                Agregar al Carrito
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    document.getElementById('detallesModal').style.display = 'block';
}

// ===== FUNCIONES DEL CARRITO =====

function agregarAlCarrito(productoId, nombre, precio) {
    const itemExistente = carrito.find(item => item.id === productoId);
    
    if (itemExistente) {
        itemExistente.cantidad += 1;
    } else {
        carrito.push({
            id: productoId,
            nombre: nombre,
            precio: precio,
            cantidad: 1
        });
    }
    
    guardarCarritoEnStorage();
    actualizarContadorCarrito();
    mostrarNotificacion(`${nombre} agregado al carrito`);
}

function removerDelCarrito(productoId) {
    carrito = carrito.filter(item => item.id !== productoId);
    guardarCarritoEnStorage();
    actualizarContadorCarrito();
    actualizarCarritoModal();
}

function actualizarCantidad(productoId, nuevaCantidad) {
    if (nuevaCantidad <= 0) {
        removerDelCarrito(productoId);
        return;
    }
    
    const item = carrito.find(item => item.id === productoId);
    if (item) {
        item.cantidad = nuevaCantidad;
        guardarCarritoEnStorage();
        actualizarContadorCarrito();
        actualizarCarritoModal();
    }
}

function actualizarContadorCarrito() {
    const totalItems = carrito.reduce((total, item) => total + item.cantidad, 0);
    document.querySelector('.cart-count').textContent = totalItems;
}

function mostrarCarrito() {
    actualizarCarritoModal();
    document.getElementById('carritoModal').style.display = 'block';
}

function actualizarCarritoModal() {
    const carritoItems = document.getElementById('carritoItems');
    const carritoTotal = document.getElementById('carritoTotal');
    
    if (carrito.length === 0) {
        carritoItems.innerHTML = `
            <div class="carrito-vacio">
                <i class="fas fa-shopping-cart"></i>
                <p>Tu carrito está vacío</p>
            </div>
        `;
        carritoTotal.textContent = '0.00';
        return;
    }
    
    carritoItems.innerHTML = carrito.map(item => `
        <div class="carrito-item">
            <div class="carrito-item-info">
                <div class="carrito-item-nombre">${item.nombre}</div>
                <div class="carrito-item-precio">$${item.precio.toFixed(2)}</div>
            </div>
            <div class="carrito-item-cantidad">
                <button onclick="actualizarCantidad('${item.id}', ${item.cantidad - 1})">-</button>
                <span>${item.cantidad}</span>
                <button onclick="actualizarCantidad('${item.id}', ${item.cantidad + 1})">+</button>
            </div>
            <button class="btn-eliminar" onclick="removerDelCarrito('${item.id}')">
                <i class="fas fa-trash"></i>
            </button>
        </div>
    `).join('');
    
    const total = carrito.reduce((sum, item) => sum + (item.precio * item.cantidad), 0);
    carritoTotal.textContent = total.toFixed(2);
}

function finalizarCompra() {
    if (!usuarioActual) {
        mostrarError('Debes iniciar sesión para finalizar la compra');
        cerrarModal('carritoModal');
        mostrarLogin();
        return;
    }
    
    if (carrito.length === 0) {
        mostrarError('Tu carrito está vacío');
        return;
    }
    
    // Aquí iría la lógica para procesar la compra
    mostrarNotificacion('¡Compra realizada con éxito!');
    carrito = [];
    guardarCarritoEnStorage();
    actualizarContadorCarrito();
    actualizarCarritoModal();
    cerrarModal('carritoModal');
}

// ===== FUNCIONES DE AUTENTICACIÓN =====

async function login(event) {
    event.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch(`${API_BASE}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            usuarioActual = data.usuario;
            localStorage.setItem('usuario', JSON.stringify(usuarioActual));
            mostrarNotificacion('¡Inicio de sesión exitoso!');
            cerrarModal('loginModal');
            actualizarUIUsuario();
        } else {
            mostrarError('Error de login: ' + data.error);
        }
    } catch (error) {
        mostrarError('Error de conexión: ' + error.message);
    }
}

async function registrar(event) {
    event.preventDefault();
    
    const nombre = document.getElementById('nombre').value;
    const email = document.getElementById('emailReg').value;
    const password = document.getElementById('passwordReg').value;
    
    try {
        const response = await fetch(`${API_BASE}/usuarios`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ nombre, email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            mostrarNotificacion('¡Cuenta creada exitosamente!');
            cerrarModal('registroModal');
            mostrarLogin();
        } else {
            mostrarError('Error al registrar: ' + data.error);
        }
    } catch (error) {
        mostrarError('Error de conexión: ' + error.message);
    }
}

function cerrarSesion() {
    usuarioActual = null;
    localStorage.removeItem('usuario');
    actualizarUIUsuario();
    mostrarNotificacion('Sesión cerrada');
}

function actualizarUIUsuario() {
    const btnLogin = document.querySelector('.btn-login');
    
    if (usuarioActual) {
        btnLogin.innerHTML = `
            <i class="fas fa-user"></i>
            ${usuarioActual.nombre}
        `;
        btnLogin.onclick = cerrarSesion;
    } else {
        btnLogin.innerHTML = `
            <i class="fas fa-user"></i>
            Iniciar Sesión
        `;
        btnLogin.onclick = mostrarLogin;
    }
}

// ===== FUNCIONES DE UI =====

function mostrarLogin() {
    document.getElementById('loginModal').style.display = 'block';
}

function mostrarRegistro() {
    cerrarModal('loginModal');
    document.getElementById('registroModal').style.display = 'block';
}

function cerrarModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
    
    // Limpiar modales dinámicos
    if (modalId === 'detallesModal') {
        document.getElementById(modalId).remove();
    }
}

function scrollToProductos() {
    document.getElementById('productos').scrollIntoView({ 
        behavior: 'smooth' 
    });
}

function mostrarLoading(mostrar) {
    const loading = document.getElementById('loading');
    loading.style.display = mostrar ? 'block' : 'none';
}

function mostrarError(mensaje) {
    mostrarNotificacion(mensaje, 'error');
}

function mostrarNotificacion(mensaje, tipo = 'success') {
    const notificacion = document.createElement('div');
    notificacion.className = `notificacion ${tipo}`;
    notificacion.innerHTML = `
        <i class="fas fa-${tipo === 'error' ? 'exclamation-circle' : 'check-circle'}"></i>
        <span>${mensaje}</span>
    `;
    
    document.body.appendChild(notificacion);
    
    // Animación de entrada
    setTimeout(() => notificacion.classList.add('show'), 100);
    
    // Auto-remover después de 3 segundos
    setTimeout(() => {
        notificacion.classList.remove('show');
        setTimeout(() => notificacion.remove(), 300);
    }, 3000);
}

// ===== FUNCIONES DE STORAGE =====

function guardarCarritoEnStorage() {
    localStorage.setItem('carrito', JSON.stringify(carrito));
}

function cargarCarritoDesdeStorage() {
    const carritoGuardado = localStorage.getItem('carrito');
    if (carritoGuardado) {
        carrito = JSON.parse(carritoGuardado);
    }
    
    const usuarioGuardado = localStorage.getItem('usuario');
    if (usuarioGuardado) {
        usuarioActual = JSON.parse(usuarioGuardado);
        actualizarUIUsuario();
    }
}

// ===== EVENT LISTENERS GLOBALES =====

// Cerrar modales al hacer clic fuera
window.addEventListener('click', function(event) {
    const modales = document.querySelectorAll('.modal');
    modales.forEach(modal => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
});

// Navegación suave
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// Navegación activa
window.addEventListener('scroll', function() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    
    let current = '';
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (pageYOffset >= sectionTop - 200) {
            current = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
}); 