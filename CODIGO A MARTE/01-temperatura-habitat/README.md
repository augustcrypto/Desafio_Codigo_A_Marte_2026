# 🌡️ Sistema de Control de Temperatura - Hábitat Marciano

## 📋 Descripción

Sistema crítico de control de temperatura para el hábitat marciano y la huerta. Implementado en tres lenguajes para máxima confiabilidad y redundancia.

## 🎯 Características Principales

- **Redundancia de Sensores**: 3 sensores por zona (hábitat y huerta)
- **Redundancia de Actuadores**: 2 actuadores por zona
- **Detección de Fallos**: Identificación automática de sensores defectuosos
- **Protocolo de Emergencia**: Activación automática en condiciones críticas
- **Monitoreo Continuo**: Ciclos de control cada 2 segundos
- **Thread-Safe**: Implementación segura para concurrencia

## 📊 Parámetros de Operación

### Hábitat Principal
- **Rango Normal**: 18°C - 24°C
- **Temperatura Objetivo**: 21°C

### Huerta Marciana
- **Rango Normal**: 20°C - 28°C
- **Temperatura Objetivo**: 24°C

### Alertas Críticas
- **Mínima Crítica**: 10°C
- **Máxima Crítica**: 35°C

## 🚀 Implementaciones

### Rust (Máxima Seguridad)

**Características**:
- Seguridad de memoria garantizada en tiempo de compilación
- Concurrencia sin data races
- Rendimiento óptimo

**Compilar y Ejecutar**:
```bash
cd rust
cargo build --release
cargo run --release
```

**Ejecutar Tests**:
```bash
cargo test
```

### C++ (Alto Rendimiento)

**Características**:
- RAII para gestión de recursos
- Smart pointers para seguridad de memoria
- Optimización de nivel 3

**Compilar y Ejecutar**:
```bash
cd cpp
mkdir build && cd build
cmake ..
cmake --build . --config Release
./control_temperatura  # Linux/Mac
control_temperatura.exe  # Windows
```

### Python (Desarrollo Rápido)

**Características**:
- Type hints para claridad
- Dataclasses para estructuras
- Threading para concurrencia

**Ejecutar**:
```bash
cd python
python control_temperatura.py
```

## 🔍 Estados del Sistema

| Estado | Descripción | Acción |
|--------|-------------|--------|
| ✓ NORMAL | Temperatura en rango óptimo | Ajustes mínimos |
| ⚠ ADVERTENCIA | Temperatura fuera de rango | Ajustes moderados |
| 🔴 CRÍTICO | Temperatura muy fuera de rango | Ajustes máximos |
| 🚨 EMERGENCIA | Temperatura peligrosa | Protocolo de emergencia |

## 📈 Arquitectura del Sistema

```
┌─────────────────────────────────────────┐
│     Sistema Control Temperatura         │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────────┐  ┌──────────────┐   │
│  │   Hábitat    │  │    Huerta    │   │
│  ├──────────────┤  ├──────────────┤   │
│  │ Sensor 1,2,3 │  │ Sensor 4,5,6 │   │
│  │ Actuador 1,2 │  │ Actuador 3,4 │   │
│  └──────────────┘  └──────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │   Control Logic                 │   │
│  │   - Promedio de sensores        │   │
│  │   - Evaluación de estado        │   │
│  │   - Cálculo de potencia         │   │
│  │   - Protocolo de emergencia     │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

## 🛡️ Seguridad y Confiabilidad

1. **Redundancia**: Múltiples sensores y actuadores por zona
2. **Detección de Fallos**: Identificación automática de componentes defectuosos
3. **Protocolo de Emergencia**: Respuesta automática a condiciones críticas
4. **Thread-Safety**: Protección con mutex en todas las operaciones críticas
5. **Manejo de Errores**: Excepciones y errores manejados apropiadamente

## 📝 Ejemplo de Salida

```
============================================================
🚀 SISTEMA DE CONTROL DE TEMPERATURA - HÁBITAT MARCIANO
============================================================
Versión: 1.0.0
Estado: Sistema Crítico - Máxima Prioridad

🔍 DIAGNÓSTICO DEL SISTEMA
============================================================

📡 Sensores Hábitat:
   Sensor 1: ✓ Operativo - 20.50°C
   Sensor 2: ✓ Operativo - 20.30°C
   Sensor 3: ✓ Operativo - 20.70°C

📊 LECTURAS ACTUALES:
   Hábitat: 20.50°C (Rango: 18.0°C - 24.0°C)
   Huerta:  23.20°C (Rango: 20.0°C - 28.0°C)

✓ ESTADO DEL SISTEMA: NORMAL

🎯 AJUSTES CALCULADOS:
🔧 Actuador 1 ajustado a 2.5% potencia
🔧 Actuador 2 ajustado a 2.5% potencia
```

## 🔧 Mantenimiento

### Calibración de Sensores
Los sensores se calibran automáticamente cuando se detectan fallos. Para calibración manual, usar el método `calibrar()`.

### Diagnóstico
El sistema proporciona diagnóstico completo al inicio y al final de cada sesión.

## ⚠️ Consideraciones para Marte

- **Presión Atmosférica**: 0.6% de la Tierra
- **Temperatura Externa**: -63°C promedio
- **Radiación**: Sin campo magnético protector
- **Aislamiento**: Crítico para mantener temperatura
- **Energía**: Sistema solar con baterías de respaldo

## 📚 Referencias

- NASA Mars Habitat Design Guidelines
- ESA Life Support Systems
- Mars Society Technical Papers

## 👥 Equipo

Sistema desarrollado para el proyecto de Hábitat Marciano.

## 📄 Licencia

Sistema crítico - Uso exclusivo para misiones espaciales.