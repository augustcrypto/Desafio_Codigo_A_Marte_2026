# 📊 PRESENTACIONES - HÁBITAT MARCIANO

## 🎯 Descripción

Este directorio contiene presentaciones interactivas y documentación visual de todos los sistemas críticos del hábitat marciano.

## 📁 Contenido

### 🌐 Presentaciones HTML5 Interactivas

#### `index.html` - Portal Principal
**Cómo usar**: Abre este archivo en tu navegador web
- Portal de navegación a todas las presentaciones
- Estadísticas del proyecto
- Animaciones de fondo espacial
- Diseño responsive

#### `01-temperatura-habitat.html` - Control de Temperatura
**Características interactivas**:
- ✅ Visualización en tiempo real de sensores
- ✅ Simulación de actuadores térmicos
- ✅ Control deslizante de temperatura marciana
- ✅ Simulaciones de condiciones extremas
- ✅ Alertas del sistema
- ✅ Arquitectura visual del sistema

**Simulaciones disponibles**:
- 🟢 Condiciones Normales
- 🔵 Ola de Frío
- 🔴 Ola de Calor
- 🚨 Emergencia

#### `02-proteccion-bitflips.html` - Protección contra Radiación
**Características interactivas**:
- ✅ Grid de memoria de 64 celdas (clickeable)
- ✅ Visualización TMR con 3 réplicas
- ✅ Medidor de radiación cósmica
- ✅ Estadísticas en tiempo real
- ✅ Animaciones de corrección de errores

**Simulaciones disponibles**:
- ⚡ Bit Flip Simple
- ⚡⚡ Múltiples Bit Flips
- ☀️ Tormenta Solar
- 🔍 Verificación de Memoria
- 🔄 Reset del Sistema

### 📝 Presentación en Markdown

#### `PRESENTACION_GENERAL.md` - Presentación Completa
**Contenido** (520 líneas):
1. Introducción y Contexto
2. Desafíos de Marte
3. Arquitectura General
4. Descripción de los 7 Sistemas
5. Tecnologías Utilizadas (Rust, C++, Python)
6. Resultados y Métricas
7. Conclusiones

**Formato**: Markdown con diagramas ASCII
**Uso**: Ideal para presentaciones técnicas o documentación

## 🚀 Cómo Usar las Presentaciones

### Opción 1: Navegador Web (Recomendado)

```bash
# Navega al directorio de presentaciones
cd presentaciones

# Abre el portal principal en tu navegador
# Windows
start index.html

# macOS
open index.html

# Linux
xdg-open index.html
```

### Opción 2: Servidor Local

Para mejor experiencia (especialmente si tienes problemas con CORS):

```bash
# Python 3
python -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000

# Node.js (si tienes http-server instalado)
npx http-server

# Luego abre en el navegador:
# http://localhost:8000
```

### Opción 3: Visualizador de Markdown

Para la presentación general:

```bash
# Con VS Code
code PRESENTACION_GENERAL.md

# Con cualquier editor de Markdown
# O visualizadores online como:
# - https://dillinger.io/
# - https://stackedit.io/
```

## 🎨 Características de las Presentaciones HTML5

### Tecnologías Utilizadas
- **HTML5**: Estructura semántica
- **CSS3**: Animaciones y efectos visuales
- **JavaScript Vanilla**: Interactividad sin dependencias
- **Responsive Design**: Adaptable a móviles y tablets

### Efectos Visuales
- ✨ Animaciones de fade-in y slide
- 🌟 Fondo de estrellas animado
- 💫 Efectos de hover y transiciones
- 🎭 Gradientes dinámicos
- ⚡ Animaciones de error y corrección

### Sin Dependencias Externas
- ❌ No requiere Node.js
- ❌ No requiere npm/yarn
- ❌ No requiere frameworks
- ✅ Solo HTML, CSS y JavaScript puro
- ✅ Funciona offline

## 📱 Compatibilidad

### Navegadores Soportados
- ✅ Chrome/Edge (Recomendado)
- ✅ Firefox
- ✅ Safari
- ✅ Opera
- ⚠️ Internet Explorer (funcionalidad limitada)

### Dispositivos
- ✅ Desktop (Windows, macOS, Linux)
- ✅ Tablets
- ✅ Smartphones (diseño responsive)

## 🎓 Uso Educativo

### Para Presentaciones
1. Abre `index.html` en modo presentación del navegador (F11)
2. Navega entre las diferentes presentaciones
3. Usa las simulaciones interactivas para demostrar conceptos

### Para Demostraciones
1. **Control de Temperatura**: Muestra cómo el sistema responde a cambios
2. **Bit Flips**: Demuestra la corrección de errores en tiempo real

### Para Documentación
- Usa `PRESENTACION_GENERAL.md` para documentación técnica
- Exporta a PDF si necesitas versión impresa

## 🔧 Personalización

### Modificar Colores
Edita las variables CSS en la sección `<style>`:
```css
/* Ejemplo: Cambiar color principal */
background: linear-gradient(135deg, #TU_COLOR_1, #TU_COLOR_2);
```

### Agregar Nuevas Simulaciones
Edita el JavaScript al final de cada archivo HTML:
```javascript
function tuNuevaSimulacion() {
    // Tu código aquí
}
```

### Cambiar Contenido
El contenido está en HTML semántico, fácil de modificar:
```html
<div class="section">
    <h2>Tu Título</h2>
    <p>Tu contenido</p>
</div>
```

## 📊 Estructura de Archivos

```
presentaciones/
├── index.html                      # Portal principal
├── 01-temperatura-habitat.html     # Demo interactiva temperatura
├── 02-proteccion-bitflips.html     # Demo interactiva bit flips
├── PRESENTACION_GENERAL.md         # Presentación completa
└── README.md                       # Este archivo
```

## 🎯 Próximas Presentaciones

Las siguientes presentaciones HTML5 están planificadas:
- [ ] 03-comunicaciones.html
- [ ] 04-telemetria.html
- [ ] 05-control-o2.html
- [ ] 06-conversion-co2-o2.html
- [ ] 07-filtracion-agua.html

Por ahora, estos sistemas están documentados en el README principal del proyecto.

## 💡 Tips de Uso

### Para Presentaciones en Vivo
1. Usa modo pantalla completa (F11)
2. Prepara las simulaciones antes de mostrarlas
3. Explica cada sección antes de interactuar
4. Usa el botón de reset entre demostraciones

### Para Grabación de Video
1. Usa resolución 1920x1080
2. Graba en Chrome para mejor rendimiento
3. Muestra las animaciones lentamente
4. Explica cada interacción

### Para Documentación
1. Toma screenshots de las visualizaciones
2. Exporta el Markdown a PDF
3. Incluye enlaces a las demos HTML

## 🐛 Solución de Problemas

### Las animaciones no funcionan
- Verifica que JavaScript esté habilitado
- Usa un navegador moderno
- Limpia la caché del navegador

### Los estilos no se cargan
- Verifica que el archivo HTML esté completo
- Abre desde un servidor local si hay problemas

### Las simulaciones no responden
- Refresca la página (F5)
- Verifica la consola del navegador (F12)
- Usa el botón de reset

## 📞 Soporte

Para problemas o sugerencias sobre las presentaciones:
1. Revisa este README
2. Consulta el código fuente (está comentado)
3. Verifica la consola del navegador para errores

## 📄 Licencia

Estas presentaciones son parte del proyecto de Hábitat Marciano y están diseñadas para uso educativo y demostrativo.

---

**🚀 ¡Disfruta explorando los sistemas del hábitat marciano!**

*"Per aspera ad astra" - A través de las dificultades, hacia las estrellas*