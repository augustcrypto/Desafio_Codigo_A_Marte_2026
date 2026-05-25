#!/usr/bin/env python3
"""
Sistema de Protección contra Bit Flips por Radiación Cósmica
Implementación en Python con ECC y TMR
"""

import time
from typing import List, Dict, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, field

class TipoError(Enum):
    """Tipos de errores detectables"""
    SIN_ERROR = "sin_error"
    ERROR_CORREGIDO = "error_corregido"
    ERROR_INCORREGIBLE = "error_incorregible"

class TMRMemoria:
    """Triple Modular Redundancy para protección de datos"""
    
    def __init__(self, valor: List[int]):
        self.replicas = [valor.copy(), valor.copy(), valor.copy()]
    
    def leer_con_votacion(self) -> List[int]:
        """Lee el valor usando votación por mayoría"""
        if self.replicas[0] == self.replicas[1]:
            return self.replicas[0].copy()
        elif self.replicas[0] == self.replicas[2]:
            return self.replicas[0].copy()
        else:
            return self.replicas[1].copy()
    
    def escribir(self, valor: List[int]) -> None:
        """Escribe el valor en las tres réplicas"""
        self.replicas = [valor.copy(), valor.copy(), valor.copy()]
    
    def verificar_integridad(self) -> bool:
        """Verifica si las tres réplicas son idénticas"""
        return (self.replicas[0] == self.replicas[1] and 
                self.replicas[1] == self.replicas[2])
    
    def corregir_errores(self) -> None:
        """Corrige errores usando votación"""
        valor_correcto = self.leer_con_votacion()
        self.escribir(valor_correcto)

class HammingCode:
    """Código Hamming para detección y corrección de errores"""
    
    def __init__(self, datos: List[int]):
        self.data = datos.copy()
        self.parity_bits = self._calcular_paridad(self.data)
    
    def _calcular_paridad(self, datos: List[int]) -> List[int]:
        """Calcula bits de paridad usando Hamming(7,4)"""
        paridad = []
        for i in range(0, len(datos), 4):
            d0 = datos[i] if i < len(datos) else 0
            d1 = datos[i+1] if i+1 < len(datos) else 0
            d2 = datos[i+2] if i+2 < len(datos) else 0
            d3 = datos[i+3] if i+3 < len(datos) else 0
            
            paridad.append(d0 ^ d1 ^ d3)
            paridad.append(d0 ^ d2 ^ d3)
            paridad.append(d1 ^ d2 ^ d3)
        
        return paridad
    
    def verificar_y_corregir(self) -> TipoError:
        """Verifica y corrige errores en los datos"""
        paridad_actual = self._calcular_paridad(self.data)
        errores = 0
        pos_error = 0
        
        for i, (actual, almacenada) in enumerate(zip(paridad_actual, self.parity_bits)):
            if actual != almacenada:
                errores += 1
                pos_error = i
        
        if errores == 0:
            return TipoError.SIN_ERROR
        elif errores == 1 and pos_error < len(self.data):
            self.data[pos_error] ^= 1  # Invertir bit
            self.parity_bits = self._calcular_paridad(self.data)
            return TipoError.ERROR_CORREGIDO
        else:
            return TipoError.ERROR_INCORREGIBLE
    
    def get_data(self) -> List[int]:
        """Obtiene los datos protegidos"""
        return self.data.copy()

@dataclass
class EstadisticasError:
    """Estadísticas de errores del sistema"""
    errores_detectados: int = 0
    errores_corregidos: int = 0
    errores_incorregibles: int = 0
    tiempo_inicio: float = field(default_factory=time.time)
    
    def registrar_error(self, tipo: TipoError) -> None:
        """Registra un error detectado"""
        self.errores_detectados += 1
        if tipo == TipoError.ERROR_CORREGIDO:
            self.errores_corregidos += 1
        elif tipo == TipoError.ERROR_INCORREGIBLE:
            self.errores_incorregibles += 1
    
    def tasa_errores_por_segundo(self) -> float:
        """Calcula la tasa de errores por segundo"""
        duracion = time.time() - self.tiempo_inicio
        return self.errores_detectados / duracion if duracion > 0 else 0.0
    
    def efectividad_correccion(self) -> float:
        """Calcula el porcentaje de errores corregidos"""
        if self.errores_detectados > 0:
            return (self.errores_corregidos / self.errores_detectados) * 100.0
        return 100.0

class SistemaProteccionBitFlips:
    """Sistema principal de protección contra bit flips"""
    
    def __init__(self):
        self.memoria_critica: Dict[str, TMRMemoria] = {}
        self.hamming_codes: Dict[str, HammingCode] = {}
        self.estadisticas = EstadisticasError()
        self.activo = True
    
    def almacenar_dato_critico(self, clave: str, datos: List[int]) -> None:
        """Almacena datos críticos con protección TMR + Hamming"""
        self.memoria_critica[clave] = TMRMemoria(datos)
        self.hamming_codes[clave] = HammingCode(datos)
        print(f"✓ Dato crítico '{clave}' almacenado con protección TMR + Hamming")
    
    def leer_dato_critico(self, clave: str) -> List[int]:
        """Lee datos críticos con verificación"""
        if clave in self.memoria_critica:
            return self.memoria_critica[clave].leer_con_votacion()
        raise KeyError(f"Clave '{clave}' no encontrada")
    
    def verificar_memoria(self) -> List[str]:
        """Verifica la integridad de toda la memoria protegida"""
        errores_encontrados = []
        print("\n🔍 Verificando integridad de memoria...")
        
        # Verificar TMR
        for clave, tmr in self.memoria_critica.items():
            if not tmr.verificar_integridad():
                print(f"⚠ Error TMR detectado en '{clave}'")
                tmr.corregir_errores()
                self.estadisticas.registrar_error(TipoError.ERROR_CORREGIDO)
                errores_encontrados.append(f"TMR: {clave}")
        
        # Verificar Hamming Codes
        for clave, hamming in self.hamming_codes.items():
            resultado = hamming.verificar_y_corregir()
            if resultado == TipoError.ERROR_CORREGIDO:
                print(f"✓ Error Hamming corregido en '{clave}'")
                self.estadisticas.registrar_error(TipoError.ERROR_CORREGIDO)
                errores_encontrados.append(f"Hamming: {clave}")
            elif resultado == TipoError.ERROR_INCORREGIBLE:
                print(f"🚨 Error incorregible en '{clave}'")
                self.estadisticas.registrar_error(TipoError.ERROR_INCORREGIBLE)
                errores_encontrados.append(f"Incorregible: {clave}")
        
        if not errores_encontrados:
            print("✓ Memoria íntegra - Sin errores detectados")
        
        return errores_encontrados
    
    def simular_radiacion(self, clave: str) -> None:
        """Simula el impacto de radiación cósmica"""
        print(f"\n☢️ Simulando impacto de radiación cósmica en '{clave}'...")
        
        if clave in self.memoria_critica:
            datos = self.memoria_critica[clave].leer_con_votacion()
            if datos:
                datos[0] ^= 0xFF  # Corromper primer byte
                self.memoria_critica[clave].replicas[0] = datos
                print("⚡ Réplica 0 corrompida")
        
        if clave in self.hamming_codes:
            if self.hamming_codes[clave].data:
                self.hamming_codes[clave].data[0] ^= 0x01  # Invertir un bit
                print("⚡ Bit flip introducido en datos Hamming")
    
    def mostrar_estadisticas(self) -> None:
        """Muestra estadísticas del sistema"""
        print("\n" + "=" * 60)
        print("📊 ESTADÍSTICAS DE PROTECCIÓN")
        print("=" * 60)
        print(f"Errores detectados:     {self.estadisticas.errores_detectados}")
        print(f"Errores corregidos:     {self.estadisticas.errores_corregidos}")
        print(f"Errores incorregibles:  {self.estadisticas.errores_incorregibles}")
        print(f"Tasa de errores:        {self.estadisticas.tasa_errores_por_segundo():.2f} errores/seg")
        print(f"Efectividad corrección: {self.estadisticas.efectividad_correccion():.1f}%")
        
        # Evaluar nivel de radiación
        tasa = self.estadisticas.tasa_errores_por_segundo()
        if tasa < 1.0:
            nivel = "🟢 BAJO"
        elif tasa < 5.0:
            nivel = "🟡 MODERADO"
        elif tasa < 10.0:
            nivel = "🟠 ALTO"
        else:
            nivel = "🔴 CRÍTICO"
        print(f"Nivel de radiación:     {nivel}")
    
    def diagnostico_completo(self) -> None:
        """Muestra diagnóstico completo del sistema"""
        print("\n" + "=" * 60)
        print("🔍 DIAGNÓSTICO DEL SISTEMA")
        print("=" * 60)
        print(f"Estado:                 {'✓ Activo' if self.activo else '✗ Inactivo'}")
        print(f"Datos protegidos (TMR): {len(self.memoria_critica)}")
        print(f"Datos con Hamming:      {len(self.hamming_codes)}")
        
        memoria_total = sum(len(tmr.replicas[0]) for tmr in self.memoria_critica.values())
        print(f"Memoria protegida:      {memoria_total} bytes")

def main():
    """Función principal del sistema"""
    print("=" * 60)
    print("🛡️ SISTEMA DE PROTECCIÓN CONTRA BIT FLIPS - HÁBITAT MARCIANO")
    print("=" * 60)
    print("Versión: 1.0.0 - Python")
    print("Protección: TMR + Hamming Code")
    print("Estado: Sistema Crítico - Máxima Prioridad\n")
    
    sistema = SistemaProteccionBitFlips()
    
    # Almacenar datos críticos
    print("📝 Almacenando datos críticos del sistema...\n")
    sistema.almacenar_dato_critico("parametros_vida", [0x4F, 0x32, 0x43, 0x4F, 0x32, 0x48, 0x32, 0x4F])
    sistema.almacenar_dato_critico("coordenadas_habitat", [0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0])
    sistema.almacenar_dato_critico("config_energia", [0xFF, 0xEE, 0xDD, 0xCC, 0xBB, 0xAA, 0x99, 0x88])
    
    sistema.diagnostico_completo()
    
    print("\n🔄 Iniciando monitoreo continuo...\n")
    
    # Ciclo de monitoreo
    for ciclo in range(1, 6):
        print("\n" + "=" * 60)
        print(f"CICLO #{ciclo}")
        print("=" * 60)
        
        time.sleep(1)
        
        # Simular radiación en ciclos específicos
        if ciclo == 2:
            sistema.simular_radiacion("parametros_vida")
        if ciclo == 4:
            sistema.simular_radiacion("coordenadas_habitat")
        
        # Verificar memoria
        errores = sistema.verificar_memoria()
        
        if errores:
            print(f"\n⚠️ Errores corregidos: {len(errores)}")
            for error in errores:
                print(f"   - {error}")
        
        # Leer datos críticos
        print("\n📖 Verificando lectura de datos críticos:")
        try:
            datos = sistema.leer_dato_critico("parametros_vida")
            print(f"   ✓ parametros_vida: {' '.join(f'{b:02X}' for b in datos)}")
        except Exception as e:
            print(f"   ✗ Error: {e}")
    
    # Estadísticas finales
    sistema.mostrar_estadisticas()
    sistema.diagnostico_completo()
    
    print("\n" + "=" * 60)
    print("✓ Sistema de protección finalizado")
    print("=" * 60)

if __name__ == "__main__":
    main()

# Made with Bob
