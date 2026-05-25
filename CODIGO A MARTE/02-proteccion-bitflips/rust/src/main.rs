// Sistema de Protección contra Bit Flips por Radiación Cósmica
// Implementación en Rust con ECC (Error Correction Code) y Triple Modular Redundancy

use std::sync::{Arc, Mutex};
use std::thread;
use std::time::{Duration, Instant};
use std::collections::HashMap;

// Constantes del sistema
const MEMORIA_CRITICA_SIZE: usize = 1024;  // KB
const INTERVALO_VERIFICACION_MS: u64 = 100;  // Verificación cada 100ms
const UMBRAL_ERRORES_CRITICO: u32 = 10;  // Errores por segundo
const TMR_REPLICAS: usize = 3;  // Triple Modular Redundancy

#[derive(Debug, Clone, Copy, PartialEq)]
enum TipoError {
    BitFlipSimple,      // 1 bit alterado
    BitFlipMultiple,    // Múltiples bits alterados
    ErrorCorregido,     // Error detectado y corregido
    ErrorIncorregible,  // Error no corregible
}

#[derive(Debug, Clone, Copy)]
struct EstadisticasError {
    errores_detectados: u32,
    errores_corregidos: u32,
    errores_incorregibles: u32,
    tiempo_ultima_deteccion: Option<Instant>,
}

impl EstadisticasError {
    fn new() -> Self {
        EstadisticasError {
            errores_detectados: 0,
            errores_corregidos: 0,
            errores_incorregibles: 0,
            tiempo_ultima_deteccion: None,
        }
    }

    fn registrar_error(&mut self, tipo: TipoError) {
        self.errores_detectados += 1;
        self.tiempo_ultima_deteccion = Some(Instant::now());
        
        match tipo {
            TipoError::ErrorCorregido => self.errores_corregidos += 1,
            TipoError::ErrorIncorregible => self.errores_incorregibles += 1,
            _ => {}
        }
    }

    fn tasa_errores_por_segundo(&self) -> f64 {
        if let Some(tiempo) = self.tiempo_ultima_deteccion {
            let duracion = tiempo.elapsed().as_secs_f64();
            if duracion > 0.0 {
                return self.errores_detectados as f64 / duracion;
            }
        }
        0.0
    }
}

// Hamming Code para detección y corrección de errores
struct HammingCode {
    data: Vec<u8>,
    parity_bits: Vec<u8>,
}

impl HammingCode {
    fn new(data: Vec<u8>) -> Self {
        let parity_bits = Self::calcular_paridad(&data);
        HammingCode { data, parity_bits }
    }

    fn calcular_paridad(data: &[u8]) -> Vec<u8> {
        let mut paridad = Vec::new();
        
        // Calcular bits de paridad usando Hamming(7,4)
        for chunk in data.chunks(4) {
            let p1 = chunk.get(0).unwrap_or(&0) ^ chunk.get(1).unwrap_or(&0) ^ chunk.get(3).unwrap_or(&0);
            let p2 = chunk.get(0).unwrap_or(&0) ^ chunk.get(2).unwrap_or(&0) ^ chunk.get(3).unwrap_or(&0);
            let p3 = chunk.get(1).unwrap_or(&0) ^ chunk.get(2).unwrap_or(&0) ^ chunk.get(3).unwrap_or(&0);
            
            paridad.push(*p1);
            paridad.push(*p2);
            paridad.push(*p3);
        }
        
        paridad
    }

    fn verificar_y_corregir(&mut self) -> Result<TipoError, String> {
        let paridad_actual = Self::calcular_paridad(&self.data);
        
        // Comparar paridad calculada con paridad almacenada
        let mut errores = 0;
        let mut posicion_error = 0;
        
        for (i, (actual, almacenada)) in paridad_actual.iter().zip(self.parity_bits.iter()).enumerate() {
            if actual != almacenada {
                errores += 1;
                posicion_error = i;
            }
        }

        match errores {
            0 => Ok(TipoError::BitFlipSimple),  // Sin errores
            1 => {
                // Error simple, corregible
                if posicion_error < self.data.len() {
                    self.data[posicion_error] ^= 1;  // Invertir bit
                    self.parity_bits = Self::calcular_paridad(&self.data);
                    Ok(TipoError::ErrorCorregido)
                } else {
                    Err("Posición de error fuera de rango".to_string())
                }
            }
            _ => Ok(TipoError::ErrorIncorregible),  // Múltiples errores
        }
    }

    fn get_data(&self) -> &[u8] {
        &self.data
    }
}

// Triple Modular Redundancy (TMR)
struct TMRMemoria<T: Clone + PartialEq> {
    replicas: [T; TMR_REPLICAS],
}

impl<T: Clone + PartialEq> TMRMemoria<T> {
    fn new(valor: T) -> Self {
        TMRMemoria {
            replicas: [valor.clone(), valor.clone(), valor],
        }
    }

    fn leer_con_votacion(&self) -> T {
        // Votación por mayoría
        if self.replicas[0] == self.replicas[1] {
            self.replicas[0].clone()
        } else if self.replicas[0] == self.replicas[2] {
            self.replicas[0].clone()
        } else {
            self.replicas[1].clone()
        }
    }

    fn escribir(&mut self, valor: T) {
        self.replicas = [valor.clone(), valor.clone(), valor];
    }

    fn verificar_integridad(&self) -> bool {
        self.replicas[0] == self.replicas[1] && 
        self.replicas[1] == self.replicas[2]
    }

    fn corregir_errores(&mut self) {
        let valor_correcto = self.leer_con_votacion();
        self.escribir(valor_correcto);
    }
}

// Sistema principal de protección
struct SistemaProteccionBitFlips {
    memoria_critica: HashMap<String, TMRMemoria<Vec<u8>>>,
    hamming_codes: HashMap<String, HammingCode>,
    estadisticas: EstadisticasError,
    activo: bool,
}

impl SistemaProteccionBitFlips {
    fn new() -> Self {
        SistemaProteccionBitFlips {
            memoria_critica: HashMap::new(),
            hamming_codes: HashMap::new(),
            estadisticas: EstadisticasError::new(),
            activo: true,
        }
    }

    fn almacenar_dato_critico(&mut self, clave: String, datos: Vec<u8>) {
        // Almacenar con TMR
        let tmr = TMRMemoria::new(datos.clone());
        self.memoria_critica.insert(clave.clone(), tmr);

        // Almacenar con Hamming Code
        let hamming = HammingCode::new(datos);
        self.hamming_codes.insert(clave, hamming);

        println!("✓ Dato crítico '{}' almacenado con protección TMR + Hamming", clave);
    }

    fn leer_dato_critico(&mut self, clave: &str) -> Result<Vec<u8>, String> {
        // Leer con TMR
        if let Some(tmr) = self.memoria_critica.get(clave) {
            let datos = tmr.leer_con_votacion();
            
            // Verificar con Hamming Code
            if let Some(hamming) = self.hamming_codes.get(clave) {
                let datos_hamming = hamming.get_data();
                
                if datos == datos_hamming {
                    Ok(datos)
                } else {
                    Err(format!("Inconsistencia detectada en '{}'", clave))
                }
            } else {
                Ok(datos)
            }
        } else {
            Err(format!("Clave '{}' no encontrada", clave))
        }
    }

    fn verificar_memoria(&mut self) -> Vec<String> {
        let mut errores_encontrados = Vec::new();

        println!("\n🔍 Verificando integridad de memoria...");

        // Verificar TMR
        for (clave, tmr) in self.memoria_critica.iter_mut() {
            if !tmr.verificar_integridad() {
                println!("⚠ Error TMR detectado en '{}'", clave);
                tmr.corregir_errores();
                self.estadisticas.registrar_error(TipoError::ErrorCorregido);
                errores_encontrados.push(format!("TMR: {}", clave));
            }
        }

        // Verificar Hamming Codes
        for (clave, hamming) in self.hamming_codes.iter_mut() {
            match hamming.verificar_y_corregir() {
                Ok(TipoError::ErrorCorregido) => {
                    println!("✓ Error Hamming corregido en '{}'", clave);
                    self.estadisticas.registrar_error(TipoError::ErrorCorregido);
                    errores_encontrados.push(format!("Hamming: {}", clave));
                }
                Ok(TipoError::ErrorIncorregible) => {
                    println!("🚨 Error incorregible en '{}'", clave);
                    self.estadisticas.registrar_error(TipoError::ErrorIncorregible);
                    errores_encontrados.push(format!("Incorregible: {}", clave));
                }
                Err(e) => {
                    println!("✗ Error al verificar '{}': {}", clave, e);
                }
                _ => {}
            }
        }

        if errores_encontrados.is_empty() {
            println!("✓ Memoria íntegra - Sin errores detectados");
        }

        errores_encontrados
    }

    fn simular_radiacion(&mut self, clave: &str) {
        println!("\n☢️ Simulando impacto de radiación cósmica en '{}'...", clave);
        
        if let Some(tmr) = self.memoria_critica.get_mut(clave) {
            // Corromper una réplica
            if let Some(replica) = tmr.replicas.get_mut(0) {
                if !replica.is_empty() {
                    replica[0] ^= 0xFF;  // Invertir todos los bits del primer byte
                    println!("⚡ Réplica 0 corrompida");
                }
            }
        }

        if let Some(hamming) = self.hamming_codes.get_mut(clave) {
            // Corromper un bit en los datos
            if !hamming.data.is_empty() {
                hamming.data[0] ^= 0x01;  // Invertir un bit
                println!("⚡ Bit flip introducido en datos Hamming");
            }
        }
    }

    fn mostrar_estadisticas(&self) {
        println!("\n{'='*60}");
        println!("📊 ESTADÍSTICAS DE PROTECCIÓN");
        println!("{'='*60}");
        println!("Errores detectados:     {}", self.estadisticas.errores_detectados);
        println!("Errores corregidos:     {}", self.estadisticas.errores_corregidos);
        println!("Errores incorregibles:  {}", self.estadisticas.errores_incorregibles);
        println!("Tasa de errores:        {:.2} errores/seg", 
                 self.estadisticas.tasa_errores_por_segundo());
        
        let efectividad = if self.estadisticas.errores_detectados > 0 {
            (self.estadisticas.errores_corregidos as f64 / 
             self.estadisticas.errores_detectados as f64) * 100.0
        } else {
            100.0
        };
        println!("Efectividad corrección: {:.1}%", efectividad);

        // Evaluar nivel de radiación
        let tasa = self.estadisticas.tasa_errores_por_segundo();
        let nivel = if tasa < 1.0 {
            "🟢 BAJO"
        } else if tasa < 5.0 {
            "🟡 MODERADO"
        } else if tasa < 10.0 {
            "🟠 ALTO"
        } else {
            "🔴 CRÍTICO"
        };
        println!("Nivel de radiación:     {}", nivel);
    }

    fn diagnostico_completo(&self) {
        println!("\n{'='*60}");
        println!("🔍 DIAGNÓSTICO DEL SISTEMA");
        println!("{'='*60}");
        println!("Estado:                 {}", if self.activo { "✓ Activo" } else { "✗ Inactivo" });
        println!("Datos protegidos (TMR): {}", self.memoria_critica.len());
        println!("Datos con Hamming:      {}", self.hamming_codes.len());
        println!("Memoria protegida:      {} KB", 
                 self.memoria_critica.values()
                     .map(|tmr| tmr.replicas[0].len())
                     .sum::<usize>() / 1024);
    }
}

fn main() {
    println!("{'='*60}");
    println!("🛡️ SISTEMA DE PROTECCIÓN CONTRA BIT FLIPS - HÁBITAT MARCIANO");
    println!("{'='*60}");
    println!("Versión: 1.0.0 - Rust");
    println!("Protección: TMR + Hamming Code");
    println!("Estado: Sistema Crítico - Máxima Prioridad\n");

    let mut sistema = SistemaProteccionBitFlips::new();

    // Almacenar datos críticos
    println!("📝 Almacenando datos críticos del sistema...\n");
    
    sistema.almacenar_dato_critico(
        "parametros_vida".to_string(),
        vec![0x4F, 0x32, 0x43, 0x4F, 0x32, 0x48, 0x32, 0x4F]  // O2, CO2, H2O
    );
    
    sistema.almacenar_dato_critico(
        "coordenadas_habitat".to_string(),
        vec![0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0]
    );
    
    sistema.almacenar_dato_critico(
        "config_energia".to_string(),
        vec![0xFF, 0xEE, 0xDD, 0xCC, 0xBB, 0xAA, 0x99, 0x88]
    );

    sistema.diagnostico_completo();

    // Ciclo de monitoreo
    println!("\n🔄 Iniciando monitoreo continuo...\n");

    for ciclo in 1..=5 {
        println!("\n{'='*60}");
        println!("CICLO #{}", ciclo);
        println!("{'='*60}");

        thread::sleep(Duration::from_secs(1));

        // Simular radiación en ciclos específicos
        if ciclo == 2 {
            sistema.simular_radiacion("parametros_vida");
        }
        if ciclo == 4 {
            sistema.simular_radiacion("coordenadas_habitat");
        }

        // Verificar memoria
        let errores = sistema.verificar_memoria();
        
        if !errores.is_empty() {
            println!("\n⚠️ Errores corregidos: {}", errores.len());
            for error in errores {
                println!("   - {}", error);
            }
        }

        // Leer datos críticos
        println!("\n📖 Verificando lectura de datos críticos:");
        match sistema.leer_dato_critico("parametros_vida") {
            Ok(datos) => println!("   ✓ parametros_vida: {:02X?}", datos),
            Err(e) => println!("   ✗ Error: {}", e),
        }
    }

    // Estadísticas finales
    sistema.mostrar_estadisticas();
    sistema.diagnostico_completo();

    println!("\n{'='*60}");
    println!("✓ Sistema de protección finalizado");
    println!("{'='*60}");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tmr_votacion() {
        let tmr = TMRMemoria::new(vec![1, 2, 3]);
        assert_eq!(tmr.leer_con_votacion(), vec![1, 2, 3]);
    }

    #[test]
    fn test_hamming_sin_error() {
        let mut hamming = HammingCode::new(vec![1, 2, 3, 4]);
        assert!(hamming.verificar_y_corregir().is_ok());
    }

    #[test]
    fn test_sistema_almacenar_leer() {
        let mut sistema = SistemaProteccionBitFlips::new();
        let datos = vec![1, 2, 3, 4];
        sistema.almacenar_dato_critico("test".to_string(), datos.clone());
        assert_eq!(sistema.leer_dato_critico("test").unwrap(), datos);
    }
}

// Made with Bob
