# 📋 INSTRUCCIONES DE COMPILACIÓN Y EJECUCIÓN

## 🚀 Guía Rápida de Inicio

Este documento proporciona instrucciones detalladas para compilar y ejecutar todos los sistemas del hábitat marciano.

---

## 📦 REQUISITOS PREVIOS

### Software Necesario

#### Para Rust 🦀
```bash
# Instalar Rust (rustup)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Verificar instalación
rustc --version
cargo --version
```

#### Para C++ ⚡
```bash
# Windows (con Visual Studio)
- Instalar Visual Studio 2019+ con C++ Desktop Development
- Instalar CMake desde https://cmake.org/download/

# Linux (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install build-essential cmake g++

# macOS
xcode-select --install
brew install cmake
```

#### Para Python 🐍
```bash
# Verificar Python 3.8+
python --version  # o python3 --version

# Instalar pip si no está disponible
python -m ensurepip --upgrade
```

---

## 🌡️ SISTEMA 1: CONTROL DE TEMPERATURA

### Rust
```bash
cd 01-temperatura-habitat/rust

# Compilar
cargo build --release

# Ejecutar
cargo run --release

# Ejecutar tests
cargo test
```

### C++
```bash
cd 01-temperatura-habitat/cpp

# Compilar (Windows)
mkdir build
cd build
cmake ..
cmake --build . --config Release
.\Release\control_temperatura.exe

# Compilar (Linux/macOS)
mkdir build && cd build
cmake ..
make
./control_temperatura
```

### Python
```bash
cd 01-temperatura-habitat/python

# Ejecutar directamente
python control_temperatura.py

# O con permisos de ejecución (Linux/macOS)
chmod +x control_temperatura.py
./control_temperatura.py
```

---

## 🛡️ SISTEMA 2: PROTECCIÓN CONTRA BIT FLIPS

### Rust
```bash
cd 02-proteccion-bitflips/rust

# Compilar y ejecutar
cargo run --release

# Tests
cargo test

# Benchmarks (opcional)
cargo bench
```

### C++
```bash
cd 02-proteccion-bitflips/cpp

# Windows
mkdir build && cd build
cmake ..
cmake --build . --config Release
.\Release\proteccion_bitflips.exe

# Linux/macOS
mkdir build && cd build
cmake ..
make -j4
./proteccion_bitflips
```

### Python
```bash
cd 02-proteccion-bitflips/python
python proteccion_bitflips.py
```

---

## 🔧 COMPILACIÓN DE TODOS LOS SISTEMAS

### Script de Compilación Automática (Linux/macOS)

Crear archivo `build_all.sh`:
```bash
#!/bin/bash

echo "🚀 Compilando todos los sistemas del hábitat marciano..."

# Rust projects
for dir in */rust; do
    echo "📦 Compilando $dir..."
    cd "$dir"
    cargo build --release
    cd ../..
done

# C++ projects
for dir in */cpp; do
    echo "⚡ Compilando $dir..."
    cd "$dir"
    mkdir -p build
    cd build
    cmake ..
    make -j4
    cd ../../..
done

echo "✅ Compilación completada!"
```

Ejecutar:
```bash
chmod +x build_all.sh
./build_all.sh
```

### Script de Compilación (Windows PowerShell)

Crear archivo `build_all.ps1`:
```powershell
Write-Host "🚀 Compilando todos los sistemas del hábitat marciano..." -ForegroundColor Green

# Rust projects
Get-ChildItem -Directory -Filter "rust" -Recurse | ForEach-Object {
    Write-Host "📦 Compilando $($_.FullName)..." -ForegroundColor Cyan
    Set-Location $_.FullName
    cargo build --release
    Set-Location $PSScriptRoot
}

# C++ projects
Get-ChildItem -Directory -Filter "cpp" -Recurse | ForEach-Object {
    Write-Host "⚡ Compilando $($_.FullName)..." -ForegroundColor Yellow
    Set-Location $_.FullName
    New-Item -ItemType Directory -Force -Path "build"
    Set-Location "build"
    cmake ..
    cmake --build . --config Release
    Set-Location $PSScriptRoot
}

Write-Host "✅ Compilación completada!" -ForegroundColor Green
```

Ejecutar:
```powershell
.\build_all.ps1
```

---

## 🧪 EJECUTAR TESTS

### Todos los Tests de Rust
```bash
# Desde el directorio raíz
find . -name "Cargo.toml" -execdir cargo test \;

# O manualmente
cd 01-temperatura-habitat/rust && cargo test
cd ../../02-proteccion-bitflips/rust && cargo test
```

### Tests de Python (si se implementan)
```bash
# Instalar pytest
pip install pytest

# Ejecutar tests
pytest
```

---

## 📊 VERIFICACIÓN DE INSTALACIÓN

### Script de Verificación

Crear `verify_setup.sh`:
```bash
#!/bin/bash

echo "🔍 Verificando instalación de herramientas..."

# Verificar Rust
if command -v rustc &> /dev/null; then
    echo "✅ Rust: $(rustc --version)"
else
    echo "❌ Rust no instalado"
fi

# Verificar Cargo
if command -v cargo &> /dev/null; then
    echo "✅ Cargo: $(cargo --version)"
else
    echo "❌ Cargo no instalado"
fi

# Verificar C++ compiler
if command -v g++ &> /dev/null; then
    echo "✅ G++: $(g++ --version | head -n1)"
elif command -v clang++ &> /dev/null; then
    echo "✅ Clang++: $(clang++ --version | head -n1)"
else
    echo "❌ Compilador C++ no encontrado"
fi

# Verificar CMake
if command -v cmake &> /dev/null; then
    echo "✅ CMake: $(cmake --version | head -n1)"
else
    echo "❌ CMake no instalado"
fi

# Verificar Python
if command -v python3 &> /dev/null; then
    echo "✅ Python: $(python3 --version)"
elif command -v python &> /dev/null; then
    echo "✅ Python: $(python --version)"
else
    echo "❌ Python no instalado"
fi

echo ""
echo "🎯 Verificación completada"
```

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### Rust

**Error: "cargo: command not found"**
```bash
# Agregar Cargo al PATH
source $HOME/.cargo/env
```

**Error de compilación**
```bash
# Limpiar y recompilar
cargo clean
cargo build --release
```

### C++

**Error: "CMake not found"**
- Instalar CMake desde https://cmake.org/download/
- Agregar CMake al PATH del sistema

**Error de enlazado (linking)**
```bash
# Limpiar build
rm -rf build
mkdir build && cd build
cmake ..
```

### Python

**Error: "ModuleNotFoundError"**
```bash
# Instalar dependencias
pip install -r requirements.txt
```

**Error de permisos (Linux/macOS)**
```bash
chmod +x *.py
```

---

## 🚀 EJECUCIÓN EN PRODUCCIÓN

### Modo Daemon (Linux)

Crear servicio systemd para ejecución continua:

```ini
# /etc/systemd/system/habitat-mars.service
[Unit]
Description=Mars Habitat Control System
After=network.target

[Service]
Type=simple
User=mars
WorkingDirectory=/opt/habitat-mars
ExecStart=/opt/habitat-mars/bin/control_sistema
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Activar:
```bash
sudo systemctl enable habitat-mars
sudo systemctl start habitat-mars
sudo systemctl status habitat-mars
```

### Logs y Monitoreo

```bash
# Ver logs en tiempo real
journalctl -u habitat-mars -f

# Ver logs de las últimas 24 horas
journalctl -u habitat-mars --since "24 hours ago"
```

---

## 📈 OPTIMIZACIÓN

### Rust - Optimización Máxima
```toml
# Cargo.toml
[profile.release]
opt-level = 3
lto = true
codegen-units = 1
panic = 'abort'
```

### C++ - Flags de Optimización
```cmake
# CMakeLists.txt
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -march=native -DNDEBUG")
```

### Python - Usar PyPy para mejor rendimiento
```bash
# Instalar PyPy
sudo apt-get install pypy3

# Ejecutar con PyPy
pypy3 control_temperatura.py
```

---

## 📝 NOTAS IMPORTANTES

1. **Compilación Release**: Siempre usar `--release` en Rust y `Release` en C++ para producción
2. **Tests**: Ejecutar tests antes de desplegar
3. **Logs**: Configurar logging apropiado para debugging
4. **Monitoreo**: Implementar monitoreo de recursos del sistema
5. **Backups**: Mantener backups de configuraciones críticas

---

## 🆘 SOPORTE

Si encuentras problemas:
1. Verificar versiones de herramientas
2. Revisar logs de compilación
3. Consultar documentación específica del sistema
4. Verificar permisos de archivos

---

## ✅ CHECKLIST DE DESPLIEGUE

- [ ] Todas las herramientas instaladas
- [ ] Compilación exitosa de todos los sistemas
- [ ] Tests pasando
- [ ] Configuración de producción revisada
- [ ] Logs configurados
- [ ] Monitoreo activo
- [ ] Backups configurados
- [ ] Documentación actualizada

---

**🚀 ¡Listo para Marte!**