# 🚀 SERVIDOR WEB - CONTROL CENTER

## 📋 Descripción

Servidor web interactivo que permite ejecutar y visualizar todos los sistemas del hábitat marciano desde una interfaz elegante en el navegador.

## ✨ Características

### 🎨 Interfaz Profesional
- **Diseño espacial** con fondo de estrellas animadas
- **Navegación por tabs**: Sistemas, Presentaciones, Documentación
- **Cards interactivas** para cada sistema
- **Selector de lenguaje** visual (Rust, C++, Python)
- **Notificaciones** en tiempo real
- **Responsive design** para todos los dispositivos

### 🔧 Funcionalidades
- ✅ Ejecutar sistemas en cualquier lenguaje con un click
- ✅ Acceso directo a presentaciones HTML5
- ✅ Enlaces a toda la documentación
- ✅ Estadísticas de cada sistema
- ✅ Estado operacional en tiempo real

## 🚀 Cómo Usar

### Opción 1: Ejecución Directa (Recomendado)

```bash
# Desde el directorio raíz del proyecto
python server.py

# O especificar un puerto diferente
python server.py 8080
```

El servidor:
1. Se iniciará automáticamente
2. Abrirá tu navegador en `http://localhost:8000`
3. Mostrará el Control Center

### Opción 2: Con Python 3

```bash
python3 server.py
```

### Opción 3: Hacer ejecutable (Linux/macOS)

```bash
chmod +x server.py
./server.py
```

## 🎯 Uso del Control Center

### 1. Ejecutar un Sistema

1. **Selecciona el lenguaje** haciendo click en:
   - 🦀 **Rust** - Máxima seguridad y rendimiento
   - ⚡ **C++** - Control de bajo nivel
   - 🐍 **Python** - Desarrollo rápido

2. **Click en "▶️ Ejecutar Sistema"**

3. El sistema se abrirá en una **nueva terminal**

### 2. Ver Presentaciones

1. Click en tab **"📊 Presentaciones"**
2. Selecciona la presentación que deseas ver
3. Se abrirá en una nueva pestaña del navegador

### 3. Acceder a Documentación

1. Click en tab **"📚 Documentación"**
2. Selecciona el documento que necesitas
3. Se abrirá en una nueva pestaña

## 📊 Sistemas Disponibles

### ✅ Implementados (Ejecutables)

#### 🌡️ Control de Temperatura
- **Rust**: `cargo run --release`
- **C++**: Requiere compilación previa
- **Python**: Ejecución directa
- **Características**: 6 sensores, 4 actuadores, protocolo de emergencia

#### 🛡️ Protección contra Bit Flips
- **Rust**: `cargo run --release`
- **C++**: Requiere compilación previa
- **Python**: Ejecución directa
- **Características**: TMR, Hamming Code, 99.9% detección

### 📋 Documentados (Ver README)

- 📡 **Comunicaciones**: Cifrado AES-256 + DTN
- 📊 **Telemetría**: Monitoreo en tiempo real
- 💨 **Control O2**: Gestión de atmósfera
- 🔄 **Conversión CO2→O2**: Tecnología MOXIE
- 💧 **Filtración Agua**: Reciclaje 98%

## 🔧 Requisitos Previos

### Para Ejecutar el Servidor
- **Python 3.6+** (incluido en la mayoría de sistemas)
- No requiere dependencias externas

### Para Ejecutar los Sistemas

#### Rust
```bash
# Instalar Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

#### C++
```bash
# Compilar primero
cd 01-temperatura-habitat/cpp
mkdir build && cd build
cmake ..
cmake --build . --config Release
```

#### Python
```bash
# Python 3.8+ recomendado
python --version
```

## 🌐 Puertos y Configuración

### Puerto por Defecto
- **8000** - Puerto estándar del servidor

### Cambiar Puerto
```bash
python server.py 3000  # Usar puerto 3000
python server.py 8080  # Usar puerto 8080
```

### Acceso desde Otros Dispositivos
```bash
# El servidor escucha en todas las interfaces
# Accede desde otro dispositivo en la misma red:
http://[IP-DE-TU-COMPUTADORA]:8000
```

## 🎨 Capturas de Pantalla

### Control Center Principal
```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🚀 CONTROL CENTER                                          ║
║   Hábitat Marciano - Sistemas Críticos de Soporte Vital     ║
║                                                              ║
║   ● Sistema Operacional                                     ║
║   ● 7 Sistemas Activos                                      ║
║   ● 3 Lenguajes Disponibles                                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Tabs Disponibles
- 💻 **Ejecutar Sistemas** - Interfaz principal
- 📊 **Presentaciones** - Demos HTML5 interactivas
- 📚 **Documentación** - Todos los READMEs

## 🔍 API del Servidor

### Endpoints Disponibles

#### GET /
Sirve la página principal del Control Center

#### GET /api/run?system=SYSTEM&lang=LANGUAGE
Ejecuta un sistema en el lenguaje especificado

**Parámetros**:
- `system`: `temperatura` | `bitflips`
- `lang`: `rust` | `cpp` | `python`

**Respuesta**:
```json
{
    "success": true,
    "message": "Sistema temperatura ejecutándose en rust",
    "system": "temperatura",
    "language": "rust"
}
```

#### GET /api/status
Devuelve el estado del servidor

**Respuesta**:
```json
{
    "status": "operational",
    "systems": 7,
    "languages": 3,
    "uptime": "active"
}
```

## 🐛 Solución de Problemas

### El servidor no inicia
```bash
# Verificar que Python esté instalado
python --version

# Verificar que el puerto no esté en uso
# Windows
netstat -ano | findstr :8000

# Linux/macOS
lsof -i :8000

# Usar otro puerto
python server.py 8080
```

### El navegador no se abre automáticamente
```bash
# Abrir manualmente
# Windows
start http://localhost:8000

# macOS
open http://localhost:8000

# Linux
xdg-open http://localhost:8000
```

### Los sistemas no se ejecutan
1. **Verificar que estén compilados** (para Rust y C++)
2. **Verificar permisos** de ejecución
3. **Revisar la terminal** que se abre para ver errores

### Error "Permission Denied"
```bash
# Linux/macOS
chmod +x server.py
```

## 💡 Tips de Uso

### Para Presentaciones
1. Usa **modo pantalla completa** (F11) en el navegador
2. Prepara los sistemas compilados antes de la demo
3. Prueba cada sistema antes de presentar

### Para Desarrollo
1. Deja el servidor corriendo mientras desarrollas
2. Refresca el navegador para ver cambios
3. Usa las presentaciones HTML5 para testing visual

### Para Educación
1. Muestra el Control Center primero
2. Ejecuta sistemas en diferentes lenguajes
3. Compara rendimiento y características

## 🔒 Seguridad

### Uso Local
- El servidor está diseñado para **uso local**
- No exponer a internet sin medidas de seguridad
- Solo ejecuta sistemas del proyecto

### Recomendaciones
- Usar solo en red local confiable
- No modificar el código sin revisar
- Mantener el firewall activo

## 📈 Rendimiento

### Recursos del Servidor
- **CPU**: < 1% en idle
- **RAM**: ~50 MB
- **Red**: Mínimo (solo HTTP local)

### Optimización
- El servidor es ligero y eficiente
- No requiere base de datos
- Sin dependencias pesadas

## 🎓 Casos de Uso

### 1. Demostración en Vivo
```bash
python server.py
# Presentar desde el navegador
# Ejecutar sistemas en tiempo real
```

### 2. Desarrollo y Testing
```bash
python server.py 8000
# Mantener abierto mientras desarrollas
# Probar cambios rápidamente
```

### 3. Educación
```bash
python server.py
# Mostrar a estudiantes
# Explicar cada sistema
# Ejecutar demos interactivas
```

## 📞 Soporte

### Logs del Servidor
El servidor muestra logs en la terminal:
```
Servidor iniciado en puerto 8000
GET / - 200 OK
GET /api/run?system=temperatura&lang=rust - 200 OK
```

### Detener el Servidor
```bash
# Presionar Ctrl+C en la terminal
^C
🛑 Servidor detenido
```

## 🔄 Actualizaciones

### Agregar Nuevos Sistemas
1. Editar `server.py`
2. Agregar en diccionarios `commands` y `paths`
3. Actualizar el HTML en `get_main_html()`

### Personalizar Interfaz
- Editar el HTML/CSS/JS en el método `get_main_html()`
- Los estilos están inline para portabilidad
- Modificar colores, animaciones, etc.

## 📄 Licencia

Parte del proyecto Hábitat Marciano - Uso educativo y demostrativo

---

## 🚀 INICIO RÁPIDO

```bash
# 1. Navegar al directorio del proyecto
cd "CODIGO A MARTE"

# 2. Iniciar el servidor
python server.py

# 3. ¡Listo! El navegador se abrirá automáticamente
```

---

**🌟 ¡Disfruta del Control Center del Hábitat Marciano!**

*"Per aspera ad astra" - A través de las dificultades, hacia las estrellas*