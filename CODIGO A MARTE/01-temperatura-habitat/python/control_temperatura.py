#!/usr/bin/env python3
"""
Sistema Crítico de Control de Temperatura para Hábitat Marciano
Implementación en Python con type hints y manejo robusto de errores
"""

import time
import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from statistics import mean
import sys

# Constantes críticas del sistema
TEMP_MIN_HABITAT = 18.0  # °C
TEMP_MAX_HABITAT = 24.0  # °C
TEMP_MIN_HUERTA = 20.0   # °C
TEMP_MAX_HUERTA = 28.0   # °C
TEMP_CRITICA_MIN = 10.0  # °C - Alerta crítica
TEMP_CRITICA_MAX = 35.0  # °C - Alerta crítica


class ZonaHabitat(Enum):
    """Zonas del hábitat marciano"""
    HABITAT = "habitat"
    HUERTA = "huerta"


class EstadoSistema(Enum):
    """Estados posibles del sistema de control"""
    NORMAL = "normal"
    ADVERTENCIA = "advertencia"
    CRITICO = "critico"
    EMERGENCIA = "emergencia"


@dataclass
class SensorTemperatura:
    """Sensor de temperatura con redundancia y detección de fallos"""
    id: int
    zona: ZonaHabitat
    temperatura: float = 20.0
    activo: bool = True
    lecturas_fallidas: int = 0
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def leer_temperatura(self) -> float:
        """Lee la temperatura del sensor con manejo de errores"""
        with self._lock:
            if not self.activo or self.lecturas_fallidas >= 3:
                raise RuntimeError(f"Sensor {self.id} inactivo o fallido")
            
            # Simulación de lectura con variación
            variacion = (self.id * 0.1) % 2.0 - 1.0
            self.temperatura += variacion
            
            return self.temperatura

    def calibrar(self) -> None:
        """Calibra el sensor y resetea contadores de fallo"""
        with self._lock:
            self.lecturas_fallidas = 0
            self.activo = True
            print(f"✓ Sensor {self.id} calibrado")

    def __str__(self) -> str:
        estado = "✓ Operativo" if self.activo else "✗ Inactivo"
        return f"Sensor {self.id}: {estado} - {self.temperatura:.2f}°C"


@dataclass
class ActuadorTermico:
    """Actuador térmico para control de temperatura"""
    id: int
    zona: ZonaHabitat
    potencia: float = 0.0  # 0.0 a 100.0 %
    activo: bool = True
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def ajustar_potencia(self, nueva_potencia: float) -> None:
        """Ajusta la potencia del actuador"""
        with self._lock:
            self.potencia = max(0.0, min(100.0, nueva_potencia))
            print(f"🔧 Actuador {self.id} ajustado a {self.potencia:.1f}% potencia")

    def activar(self) -> None:
        """Activa el actuador"""
        with self._lock:
            self.activo = True
            print(f"✓ Actuador {self.id} activado")

    def desactivar(self) -> None:
        """Desactiva el actuador"""
        with self._lock:
            self.activo = False
            self.potencia = 0.0
            print(f"⚠ Actuador {self.id} desactivado")

    def __str__(self) -> str:
        estado = "✓ Operativo" if self.activo else "✗ Inactivo"
        return f"Actuador {self.id}: {estado} - {self.potencia:.1f}% potencia"


class SistemaControlTemperatura:
    """Sistema principal de control de temperatura del hábitat marciano"""

    def __init__(self):
        # Redundancia: 3 sensores por zona
        self.sensores_habitat: List[SensorTemperatura] = [
            SensorTemperatura(id=i, zona=ZonaHabitat.HABITAT)
            for i in range(1, 4)
        ]
        
        self.sensores_huerta: List[SensorTemperatura] = [
            SensorTemperatura(id=i, zona=ZonaHabitat.HUERTA)
            for i in range(4, 7)
        ]

        # Redundancia: 2 actuadores por zona
        self.actuadores_habitat: List[ActuadorTermico] = [
            ActuadorTermico(id=i, zona=ZonaHabitat.HABITAT)
            for i in range(1, 3)
        ]
        
        self.actuadores_huerta: List[ActuadorTermico] = [
            ActuadorTermico(id=i, zona=ZonaHabitat.HUERTA)
            for i in range(3, 5)
        ]

        self.estado: EstadoSistema = EstadoSistema.NORMAL
        self._lock = threading.Lock()

    def obtener_temperatura_promedio(self, zona: ZonaHabitat) -> float:
        """Obtiene la temperatura promedio de una zona usando sensores redundantes"""
        sensores = (self.sensores_habitat if zona == ZonaHabitat.HABITAT 
                   else self.sensores_huerta)
        
        lecturas_validas = []
        
        for sensor in sensores:
            try:
                temp = sensor.leer_temperatura()
                lecturas_validas.append(temp)
            except RuntimeError:
                # Sensor fallido, continuar con otros
                pass
        
        if not lecturas_validas:
            raise RuntimeError("No hay sensores operativos")
        
        return mean(lecturas_validas)

    def evaluar_estado(self, temp_habitat: float, temp_huerta: float) -> EstadoSistema:
        """Evalúa el estado del sistema basado en las temperaturas"""
        if (temp_habitat < TEMP_CRITICA_MIN or temp_habitat > TEMP_CRITICA_MAX or
            temp_huerta < TEMP_CRITICA_MIN or temp_huerta > TEMP_CRITICA_MAX):
            return EstadoSistema.EMERGENCIA
        elif (temp_habitat < TEMP_MIN_HABITAT - 2.0 or temp_habitat > TEMP_MAX_HABITAT + 2.0 or
              temp_huerta < TEMP_MIN_HUERTA - 2.0 or temp_huerta > TEMP_MAX_HUERTA + 2.0):
            return EstadoSistema.CRITICO
        elif (temp_habitat < TEMP_MIN_HABITAT or temp_habitat > TEMP_MAX_HABITAT or
              temp_huerta < TEMP_MIN_HUERTA or temp_huerta > TEMP_MAX_HUERTA):
            return EstadoSistema.ADVERTENCIA
        else:
            return EstadoSistema.NORMAL

    def calcular_potencia_necesaria(self, temp_actual: float, temp_objetivo: float) -> float:
        """Calcula la potencia necesaria para alcanzar la temperatura objetivo"""
        diferencia = temp_objetivo - temp_actual
        potencia = max(0.0, min(100.0, abs(diferencia) * 10.0))
        
        return potencia if diferencia > 0.0 else -potencia

    def ajustar_actuadores(self, zona: ZonaHabitat, potencia: float) -> None:
        """Ajusta los actuadores de una zona con la potencia calculada"""
        actuadores = (self.actuadores_habitat if zona == ZonaHabitat.HABITAT 
                     else self.actuadores_huerta)
        
        actuadores_activos = [a for a in actuadores if a.activo]
        
        if actuadores_activos:
            potencia_por_actuador = abs(potencia) / len(actuadores_activos)
            
            for actuador in actuadores_activos:
                actuador.ajustar_potencia(potencia_por_actuador)

    def protocolo_emergencia(self) -> None:
        """Activa el protocolo de emergencia"""
        print("\n🚨 PROTOCOLO DE EMERGENCIA ACTIVADO")
        print("   1. Activando todos los actuadores disponibles")
        print("   2. Notificando a control de misión")
        print("   3. Preparando sistemas de respaldo")
        
        for actuador in self.actuadores_habitat + self.actuadores_huerta:
            actuador.activar()
            actuador.ajustar_potencia(100.0)

    def ciclo_control(self) -> None:
        """Ejecuta un ciclo completo de control de temperatura"""
        with self._lock:
            print("\n" + "=" * 60)
            print("🔄 Iniciando ciclo de control de temperatura")
            print("=" * 60)

            try:
                # Leer temperaturas
                temp_habitat = self.obtener_temperatura_promedio(ZonaHabitat.HABITAT)
                temp_huerta = self.obtener_temperatura_promedio(ZonaHabitat.HUERTA)

                print("\n📊 LECTURAS ACTUALES:")
                print(f"   Hábitat: {temp_habitat:.2f}°C "
                      f"(Rango: {TEMP_MIN_HABITAT:.1f}°C - {TEMP_MAX_HABITAT:.1f}°C)")
                print(f"   Huerta:  {temp_huerta:.2f}°C "
                      f"(Rango: {TEMP_MIN_HUERTA:.1f}°C - {TEMP_MAX_HUERTA:.1f}°C)")

                # Evaluar estado
                self.estado = self.evaluar_estado(temp_habitat, temp_huerta)
                
                iconos = {
                    EstadoSistema.NORMAL: "✓",
                    EstadoSistema.ADVERTENCIA: "⚠",
                    EstadoSistema.CRITICO: "🔴",
                    EstadoSistema.EMERGENCIA: "🚨"
                }
                
                print(f"\n{iconos[self.estado]} ESTADO DEL SISTEMA: {self.estado.value.upper()}")

                # Calcular y aplicar ajustes
                temp_objetivo_habitat = (TEMP_MIN_HABITAT + TEMP_MAX_HABITAT) / 2.0
                temp_objetivo_huerta = (TEMP_MIN_HUERTA + TEMP_MAX_HUERTA) / 2.0

                potencia_habitat = self.calcular_potencia_necesaria(
                    temp_habitat, temp_objetivo_habitat)
                potencia_huerta = self.calcular_potencia_necesaria(
                    temp_huerta, temp_objetivo_huerta)

                print("\n🎯 AJUSTES CALCULADOS:")
                self.ajustar_actuadores(ZonaHabitat.HABITAT, potencia_habitat)
                self.ajustar_actuadores(ZonaHabitat.HUERTA, potencia_huerta)

                # Protocolo de emergencia
                if self.estado == EstadoSistema.EMERGENCIA:
                    self.protocolo_emergencia()

                print("✓ Ciclo completado exitosamente")

            except Exception as e:
                print(f"✗ Error en ciclo: {e}")
                raise

    def diagnostico_sistema(self) -> None:
        """Muestra un diagnóstico completo del sistema"""
        with self._lock:
            print("\n" + "=" * 60)
            print("🔍 DIAGNÓSTICO DEL SISTEMA")
            print("=" * 60)
            
            print("\n📡 Sensores Hábitat:")
            for sensor in self.sensores_habitat:
                print(f"   {sensor}")
            
            print("\n📡 Sensores Huerta:")
            for sensor in self.sensores_huerta:
                print(f"   {sensor}")
            
            print("\n🔧 Actuadores Hábitat:")
            for actuador in self.actuadores_habitat:
                print(f"   {actuador}")
            
            print("\n🔧 Actuadores Huerta:")
            for actuador in self.actuadores_huerta:
                print(f"   {actuador}")


def main():
    """Función principal del sistema"""
    print("=" * 60)
    print("🚀 SISTEMA DE CONTROL DE TEMPERATURA - HÁBITAT MARCIANO")
    print("=" * 60)
    print("Versión: 1.0.0 - Python")
    print("Estado: Sistema Crítico - Máxima Prioridad")

    try:
        sistema = SistemaControlTemperatura()
        
        # Diagnóstico inicial
        sistema.diagnostico_sistema()
        
        print("\n🔄 Iniciando monitoreo continuo...\n")
        
        # Simulación de 5 ciclos de control
        for ciclo in range(1, 6):
            print("\n" + "=" * 60)
            print(f"CICLO #{ciclo}")
            
            time.sleep(2)
            
            sistema.ciclo_control()
        
        # Diagnóstico final
        sistema.diagnostico_sistema()
        
        print("\n" + "=" * 60)
        print("✓ Sistema de control finalizado")
        print("=" * 60)

    except KeyboardInterrupt:
        print("\n\n⚠ Sistema interrumpido por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n🚨 Error crítico: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

# Made with Bob
