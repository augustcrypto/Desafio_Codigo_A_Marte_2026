# 🚀 Guía de Despliegue y Compartir

Este documento explica cómo compartir y desplegar el proyecto **Hábitat Marciano** en diferentes plataformas.

## 📋 Tabla de Contenidos

1. [Acceso Local](#acceso-local)
2. [GitHub Pages](#github-pages)
3. [Netlify](#netlify)
4. [Vercel](#vercel)
5. [Enlaces para Compartir](#enlaces-para-compartir)
6. [Visualización de Código](#visualización-de-código)

---

## 🏠 Acceso Local

### Opción 1: Live Server (VS Code)

**Más fácil y recomendado para desarrollo:**

1. Instala la extensión **Live Server** en VS Code
2. Click derecho en `index.html` → "Open with Live Server"
3. Se abrirá automáticamente en `http://localhost:5500`

**Ventajas:**
- ✅ Recarga automática al guardar cambios
- ✅ No requiere configuración
- ✅ Funciona en todos los sistemas operativos

### Opción 2: Servidor Python

```bash
# Desde el directorio raíz del proyecto
python server.py

# O manualmente:
python -m http.server 8000
# Abrir: http://localhost:8000
```

### Opción 3: Abrir Directamente

Simplemente abre `index.html` en tu navegador. Todas las demos funcionan sin servidor.

---

## 🌐 GitHub Pages

**Hosting gratuito de GitHub para sitios estáticos**

### Paso 1: Crear Repositorio

```bash
# Inicializar Git (si no está inicializado)
git init

# Agregar archivos
git add .
git commit -m "Initial commit: Hábitat Marciano"

# Crear repositorio en GitHub y conectar
git remote add origin https://github.com/TU_USUARIO/habitat-marciano.git
git branch -M main
git push -u origin main
```

### Paso 2: Activar GitHub Pages

1. Ve a tu repositorio en GitHub
2. Click en **Settings** → **Pages**
3. En "Source", selecciona **main** branch
4. Click en **Save**
5. Espera 1-2 minutos

### Paso 3: Acceder

Tu sitio estará disponible en:
```
https://TU_USUARIO.github.io/habitat-marciano/
```

### Enlaces Directos:

- **Página Principal**: `https://TU_USUARIO.github.io/habitat-marciano/`
- **Presentación General**: `https://TU_USUARIO.github.io/habitat-marciano/presentaciones/00-presentacion-general.html`
- **Portal de Demos**: `https://TU_USUARIO.github.io/habitat-marciano/presentaciones/index.html`

---

## 🚀 Netlify

**Despliegue ultra-rápido con drag & drop**

### Método 1: Drag & Drop (Más Fácil)

1. Ve a [https://app.netlify.com/drop](https://app.netlify.com/drop)
2. Arrastra la carpeta completa del proyecto
3. ¡Listo! Tu sitio estará en línea en segundos

### Método 2: Desde GitHub

1. Ve a [https://app.netlify.com](https://app.netlify.com)
2. Click en **"New site from Git"**
3. Conecta tu repositorio de GitHub
4. Configuración:
   - **Build command**: (dejar vacío)
   - **Publish directory**: `.` (punto)
5. Click en **Deploy site**

### URL Personalizada

1. En tu sitio de Netlify, ve a **Site settings** → **Domain management**
2. Click en **"Change site name"**
3. Elige un nombre: `habitat-marciano.netlify.app`

### Enlaces Directos:

```
https://habitat-marciano.netlify.app/
https://habitat-marciano.netlify.app/presentaciones/00-presentacion-general.html
https://habitat-marciano.netlify.app/presentaciones/index.html
```

---

## ▲ Vercel

**Despliegue optimizado con CDN global**

### Método 1: Vercel CLI

```bash
# Instalar Vercel CLI
npm install -g vercel

# Desde el directorio del proyecto
vercel

# Seguir las instrucciones en pantalla
```

### Método 2: Desde GitHub

1. Ve a [https://vercel.com/new](https://vercel.com/new)
2. Importa tu repositorio de GitHub
3. Configuración:
   - **Framework Preset**: Other
   - **Build Command**: (dejar vacío)
   - **Output Directory**: `.` (punto)
4. Click en **Deploy**

### URL Personalizada

Tu sitio estará en:
```
https://habitat-marciano.vercel.app/
```

---

## 🔗 Enlaces para Compartir

### Para Presentaciones en Vivo

**Presentación General (Estilo PowerPoint):**
```
[Tu URL]/presentaciones/00-presentacion-general.html
```

**Características:**
- ✅ 12 slides interactivos
- ✅ Navegación con teclado (← →)
- ✅ Pantalla completa (F11)
- ✅ Contador de slides
- ✅ Barra de progreso

**Controles:**
- `←` / `→`: Navegar entre slides
- `Home`: Ir al inicio
- `End`: Ir al final
- `F11`: Pantalla completa

### Para Demos Interactivas

**Portal de Demos:**
```
[Tu URL]/presentaciones/index.html
```

**Demos Individuales:**
```
[Tu URL]/presentaciones/01-temperatura-habitat.html
[Tu URL]/presentaciones/02-proteccion-bitflips.html
[Tu URL]/presentaciones/05-control-o2.html
[Tu URL]/presentaciones/06-conversion-co2-o2.html
[Tu URL]/presentaciones/07-filtracion-agua.html
[Tu URL]/presentaciones/08-sistema-energia-recursos.html
```

### Para Documentación

**README Principal:**
```
[Tu URL]/README.md
```

**Presentación Markdown:**
```
[Tu URL]/presentaciones/PRESENTACION_GENERAL.md
```

---

## 👨‍💻 Visualización de Código

### GitHub

Tu código estará visible en:
```
https://github.com/TU_USUARIO/habitat-marciano
```

**Características:**
- ✅ Navegación por carpetas
- ✅ Syntax highlighting
- ✅ Búsqueda de código
- ✅ Historial de commits
- ✅ README renderizado

### GitHub Gist (Para Snippets)

Para compartir fragmentos específicos:

1. Ve a [https://gist.github.com](https://gist.github.com)
2. Pega el código
3. Comparte el enlace

### CodeSandbox

Para edición en línea:

1. Ve a [https://codesandbox.io](https://codesandbox.io)
2. Importa desde GitHub
3. Comparte el enlace de sandbox

---

## 📱 QR Code para Compartir

Genera un QR code de tu URL para presentaciones:

**Herramientas:**
- [QR Code Generator](https://www.qr-code-generator.com/)
- [QRCode Monkey](https://www.qrcode-monkey.com/)

**Uso:**
1. Pega tu URL del proyecto
2. Genera el QR
3. Descarga la imagen
4. Incluye en presentaciones o documentos

---

## 📊 Estadísticas de Uso

### Google Analytics (Opcional)

Para trackear visitas:

1. Crea una cuenta en [Google Analytics](https://analytics.google.com)
2. Obtén tu ID de tracking
3. Agrega al `<head>` de `index.html`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

---

## 🎯 Checklist de Despliegue

Antes de compartir, verifica:

- [ ] Todos los enlaces funcionan correctamente
- [ ] Las demos HTML5 cargan sin errores
- [ ] La presentación general se ve correctamente
- [ ] El README está actualizado
- [ ] Los archivos de código están bien formateados
- [ ] No hay información sensible en el código
- [ ] Las imágenes y recursos cargan correctamente
- [ ] El sitio es responsive (móvil/tablet/desktop)
- [ ] Los navegadores soportados funcionan (Chrome, Firefox, Safari, Edge)

---

## 🆘 Solución de Problemas

### Problema: Los archivos no cargan

**Solución:**
- Verifica que las rutas sean relativas (no absolutas)
- Asegúrate de que los nombres de archivo coincidan (case-sensitive en Linux)

### Problema: GitHub Pages no actualiza

**Solución:**
```bash
# Forzar actualización
git commit --allow-empty -m "Trigger rebuild"
git push
```

### Problema: CORS errors en local

**Solución:**
- Usa Live Server o un servidor HTTP
- No abras archivos directamente con `file://`

---

## 📞 Soporte

Para problemas o preguntas:

1. **GitHub Issues**: Crea un issue en el repositorio
2. **Documentación**: Revisa `README.md` y `INSTRUCCIONES_COMPILACION.md`
3. **Demos**: Prueba las demos HTML5 para verificar funcionalidad

---

## 🎓 Recursos Adicionales

### Tutoriales de Despliegue

- [GitHub Pages Docs](https://docs.github.com/en/pages)
- [Netlify Docs](https://docs.netlify.com/)
- [Vercel Docs](https://vercel.com/docs)

### Herramientas Útiles

- [Can I Use](https://caniuse.com/) - Compatibilidad de navegadores
- [PageSpeed Insights](https://pagespeed.web.dev/) - Optimización de rendimiento
- [W3C Validator](https://validator.w3.org/) - Validación HTML

---

## 🌟 Mejores Prácticas

### Para Presentaciones

1. **Prueba antes**: Abre la presentación en pantalla completa antes de presentar
2. **Backup**: Ten una copia local por si falla internet
3. **Navegación**: Practica la navegación con teclado
4. **Tiempo**: Calcula ~2-3 minutos por slide

### Para Compartir Código

1. **README claro**: Asegúrate de que el README explique todo
2. **Comentarios**: Comenta el código complejo
3. **Ejemplos**: Incluye ejemplos de uso
4. **Licencia**: Agrega un archivo LICENSE si es necesario

---

## 📝 Plantilla de Email para Compartir

```
Asunto: Proyecto Hábitat Marciano - Sistema de Soporte Vital

Hola,

Te comparto mi proyecto de sistemas críticos para colonización marciana:

🌐 Sitio Web: [TU_URL]
📊 Presentación: [TU_URL]/presentaciones/00-presentacion-general.html
🎮 Demos: [TU_URL]/presentaciones/index.html
💻 Código: https://github.com/TU_USUARIO/habitat-marciano

El proyecto incluye:
- 8 sistemas críticos implementados
- 3 lenguajes de programación (Rust, C++, Python)
- 6 demos HTML5 interactivas
- Documentación completa

Saludos,
[Tu Nombre]
```

---

## 🎉 ¡Listo para Compartir!

Tu proyecto está ahora accesible desde cualquier lugar del mundo. Comparte los enlaces y muestra tu trabajo.

**"Per aspera ad astra" - A través de las dificultades, hacia las estrellas** 🚀