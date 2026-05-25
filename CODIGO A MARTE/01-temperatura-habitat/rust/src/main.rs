// Sistema Crítico de Control de Temperatura para Hábitat Marciano
// Implementación en Rust con seguridad de memoria y concurrencia

use std::sync::{Arc, Mutex};
use std::thread;
use std::time::Duration;

// Constantes críticas del sistema
const TEMP_MIN_HABITAT: f32 = 18.0;  // °C
const TEMP_MAX_HABITAT: f32 = 24.0;  // °C
const TEMP_MIN_HUERTA: f32 = 20.0;   // °C
const TEMP_MAX_HUERTA: f32 = 28.0;   // °C
const TEMP_CRITICA_MIN: f32 = 10.0;  // °C - Alerta crítica
const TEMP_CRITICA_MAX: f32 = 35.0;  // °C - Alerta crítica

#[derive(Debug, Clone, Copy, PartialEq)]
enum ZonaHabitat {
    Habitat,
    Huerta,
}

#[derive(Debug, Clone, Copy, PartialEq)]
enum EstadoSistema {
    Normal,
    Advertencia,
    Critico,
    Emergencia,
}

#[derive(Debug, Clone)]
struct SensorTemperatura {
    id: u32,
    zona: ZonaHabitat,
    temperatura: f32,
    activo: bool,
    lecturas_fallidas: u32,
}

impl SensorTemperatura {
    fn new(id: u32, zona: ZonaHabitat) -> Self {
        SensorTemperatura {
            id,
            zona,
            temperatura: 20.0,
            activo: true,
            lecturas_fallidas: 0,
        }
    }

    fn leer_temperatura(&mut self) -> Result<f32, String> {
        // Simulación de lectura de sensor con posible fallo
        if self.activo && self.lecturas_fallidas < 3 {
            // Simulación: temperatura con pequeña variación
            let variacion = (self.id as f32 * 0.1) % 2.0 - 1.0;
            self.temperatura += variacion;
            Ok(self.temperatura)
        } else {
            self.lecturas_fallidas += 1;
            Err(format!("Sensor {} inactivo o fallido", self.id))
        }
    }

    fn calibrar(&mut self) {
        self.lecturas_fallidas = 0;
        self.activo = true;
        println!("✓ Sensor {} calibrado", self.id);
    }
}

#[derive(Debug)]
struct ActuadorTermico {
    id: u32,
    zona: ZonaHabitat,
    potencia: f32,  // 0.0 a 100.0 %
    activo: bool,
}

impl ActuadorTermico {
    fn new(id: u32, zona: ZonaHabitat) -> Self {
        ActuadorTermico {
            id,
            zona,
            potencia: 0.0,
            activo: true,
        }
    }

    fn ajustar_potencia(&mut self, nueva_potencia: f32) {
        self.potencia = nueva_potencia.clamp(0.0, 100.0);
        println!("🔧 Actuador {} ajustado a {:.1}% potencia", self.id, self.potencia);
    }

    fn activar(&mut self) {
        self.activo = true;
        println!("✓ Actuador {} activado", self.id);
    }

    fn desactivar(&mut self) {
        self.activo = false;
        self.potencia = 0.0;
        println!("⚠ Actuador {} desactivado", self.id);
    }
}

struct SistemaControlTemperatura {
    sensores_habitat: Vec<SensorTemperatura>,
    sensores_huerta: Vec<SensorTemperatura>,
    actuadores_habitat: Vec<ActuadorTermico>,
    actuadores_huerta: Vec<ActuadorTermico>,
    estado: EstadoSistema,
}

impl SistemaControlTemperatura {
    fn new() -> Self {
        // Redundancia: 3 sensores por zona
        let sensores_habitat = vec![
            SensorTemperatura::new(1, ZonaHabitat::Habitat),
            SensorTemperatura::new(2, ZonaHabitat::Habitat),
            SensorTemperatura::new(3, ZonaHabitat::Habitat),
        ];

        let sensores_huerta = vec![
            SensorTemperatura::new(4, ZonaHabitat::Huerta),
            SensorTemperatura::new(5, ZonaHabitat::Huerta),
            SensorTemperatura::new(6, ZonaHabitat::Huerta),
        ];

        // Redundancia: 2 actuadores por zona
        let actuadores_habitat = vec![
            ActuadorTermico::new(1, ZonaHabitat::Habitat),
            ActuadorTermico::new(2, ZonaHabitat::Habitat),
        ];

        let actuadores_huerta = vec![
            ActuadorTermico::new(3, ZonaHabitat::Huerta),
            ActuadorTermico::new(4, ZonaHabitat::Huerta),
        ];

        SistemaControlTemperatura {
            sensores_habitat,
            sensores_huerta,
            actuadores_habitat,
            actuadores_huerta,
            estado: EstadoSistema::Normal,
        }
    }

    fn obtener_temperatura_promedio(&mut self, zona: ZonaHabitat) -> Result<f32, String> {
        let sensores = match zona {
            ZonaHabitat::Habitat => &mut self.sensores_habitat,
            ZonaHabitat::Huerta => &mut self.sensores_huerta,
        };

        let mut lecturas_validas = Vec::new();

        for sensor in sensores.iter_mut() {
            if let Ok(temp) = sensor.leer_temperatura() {
                lecturas_validas.push(temp);
            }
        }

        if lecturas_validas.is_empty() {
            return Err("No hay sensores operativos".to_string());
        }

        let promedio = lecturas_validas.iter().sum::<f32>() / lecturas_validas.len() as f32;
        Ok(promedio)
    }

    fn evaluar_estado(&mut self, temp_habitat: f32, temp_huerta: f32) -> EstadoSistema {
        if temp_habitat < TEMP_CRITICA_MIN || temp_habitat > TEMP_CRITICA_MAX ||
           temp_huerta < TEMP_CRITICA_MIN || temp_huerta > TEMP_CRITICA_MAX {
            EstadoSistema::Emergencia
        } else if temp_habitat < TEMP_MIN_HABITAT - 2.0 || temp_habitat > TEMP_MAX_HABITAT + 2.0 ||
                  temp_huerta < TEMP_MIN_HUERTA - 2.0 || temp_huerta > TEMP_MAX_HUERTA + 2.0 {
            EstadoSistema::Critico
        } else if temp_habitat < TEMP_MIN_HABITAT || temp_habitat > TEMP_MAX_HABITAT ||
                  temp_huerta < TEMP_MIN_HUERTA || temp_huerta > TEMP_MAX_HUERTA {
            EstadoSistema::Advertencia
        } else {
            EstadoSistema::Normal
        }
    }

    fn calcular_potencia_necesaria(&self, temp_actual: f32, temp_objetivo: f32) -> f32 {
        let diferencia = temp_objetivo - temp_actual;
        let potencia = (diferencia.abs() * 10.0).clamp(0.0, 100.0);
        
        if diferencia > 0.0 {
            potencia  // Calentar
        } else {
            -potencia  // Enfriar
        }
    }

    fn ajustar_actuadores(&mut self, zona: ZonaHabitat, potencia: f32) {
        let actuadores = match zona {
            ZonaHabitat::Habitat => &mut self.actuadores_habitat,
            ZonaHabitat::Huerta => &mut self.actuadores_huerta,
        };

        // Distribuir carga entre actuadores activos
        let actuadores_activos: Vec<_> = actuadores.iter().filter(|a| a.activo).count();
        
        if actuadores_activos > 0 {
            let potencia_por_actuador = potencia / actuadores_activos as f32;
            
            for actuador in actuadores.iter_mut() {
                if actuador.activo {
                    actuador.ajustar_potencia(potencia_por_actuador.abs());
                }
            }
        }
    }

    fn ciclo_control(&mut self) -> Result<(), String> {
        println!("\n{'='*60}");
        println!("🔄 Iniciando ciclo de control de temperatura");
        println!("{'='*60}");

        // Leer temperaturas
        let temp_habitat = self.obtener_temperatura_promedio(ZonaHabitat::Habitat)?;
        let temp_huerta = self.obtener_temperatura_promedio(ZonaHabitat::Huerta)?;

        println!("\n📊 LECTURAS ACTUALES:");
        println!("   Hábitat: {:.2}°C (Rango: {:.1}°C - {:.1}°C)", 
                 temp_habitat, TEMP_MIN_HABITAT, TEMP_MAX_HABITAT);
        println!("   Huerta:  {:.2}°C (Rango: {:.1}°C - {:.1}°C)", 
                 temp_huerta, TEMP_MIN_HUERTA, TEMP_MAX_HUERTA);

        // Evaluar estado del sistema
        self.estado = self.evaluar_estado(temp_habitat, temp_huerta);
        
        let icono_estado = match self.estado {
            EstadoSistema::Normal => "✓",
            EstadoSistema::Advertencia => "⚠",
            EstadoSistema::Critico => "🔴",
            EstadoSistema::Emergencia => "🚨",
        };
        
        println!("\n{} ESTADO DEL SISTEMA: {:?}", icono_estado, self.estado);

        // Calcular y aplicar ajustes
        let temp_objetivo_habitat = (TEMP_MIN_HABITAT + TEMP_MAX_HABITAT) / 2.0;
        let temp_objetivo_huerta = (TEMP_MIN_HUERTA + TEMP_MAX_HUERTA) / 2.0;

        let potencia_habitat = self.calcular_potencia_necesaria(temp_habitat, temp_objetivo_habitat);
        let potencia_huerta = self.calcular_potencia_necesaria(temp_huerta, temp_objetivo_huerta);

        println!("\n🎯 AJUSTES CALCULADOS:");
        self.ajustar_actuadores(ZonaHabitat::Habitat, potencia_habitat);
        self.ajustar_actuadores(ZonaHabitat::Huerta, potencia_huerta);

        // Protocolo de emergencia
        if self.estado == EstadoSistema::Emergencia {
            println!("\n🚨 PROTOCOLO DE EMERGENCIA ACTIVADO");
            self.protocolo_emergencia();
        }

        Ok(())
    }

    fn protocolo_emergencia(&mut self) {
        println!("   1. Activando todos los actuadores disponibles");
        println!("   2. Notificando a control de misión");
        println!("   3. Preparando sistemas de respaldo");
        
        // Activar todos los actuadores al máximo
        for actuador in self.actuadores_habitat.iter_mut() {
            actuador.activar();
            actuador.ajustar_potencia(100.0);
        }
        
        for actuador in self.actuadores_huerta.iter_mut() {
            actuador.activar();
            actuador.ajustar_potencia(100.0);
        }
    }

    fn diagnostico_sistema(&self) {
        println!("\n{'='*60}");
        println!("🔍 DIAGNÓSTICO DEL SISTEMA");
        println!("{'='*60}");
        
        println!("\n📡 Sensores Hábitat:");
        for sensor in &self.sensores_habitat {
            let estado = if sensor.activo { "✓ Operativo" } else { "✗ Inactivo" };
            println!("   Sensor {}: {} - {:.2}°C", sensor.id, estado, sensor.temperatura);
        }
        
        println!("\n📡 Sensores Huerta:");
        for sensor in &self.sensores_huerta {
            let estado = if sensor.activo { "✓ Operativo" } else { "✗ Inactivo" };
            println!("   Sensor {}: {} - {:.2}°C", sensor.id, estado, sensor.temperatura);
        }
        
        println!("\n🔧 Actuadores Hábitat:");
        for actuador in &self.actuadores_habitat {
            let estado = if actuador.activo { "✓ Operativo" } else { "✗ Inactivo" };
            println!("   Actuador {}: {} - {:.1}% potencia", actuador.id, estado, actuador.potencia);
        }
        
        println!("\n🔧 Actuadores Huerta:");
        for actuador in &self.actuadores_huerta {
            let estado = if actuador.activo { "✓ Operativo" } else { "✗ Inactivo" };
            println!("   Actuador {}: {} - {:.1}% potencia", actuador.id, estado, actuador.potencia);
        }
    }
}

fn main() {
    println!("{'='*60}");
    println!("🚀 SISTEMA DE CONTROL DE TEMPERATURA - HÁBITAT MARCIANO");
    println!("{'='*60}");
    println!("Versión: 1.0.0 - Rust");
    println!("Estado: Sistema Crítico - Máxima Prioridad");
    
    let sistema = Arc::new(Mutex::new(SistemaControlTemperatura::new()));
    
    // Diagnóstico inicial
    {
        let sys = sistema.lock().unwrap();
        sys.diagnostico_sistema();
    }
    
    println!("\n🔄 Iniciando monitoreo continuo...\n");
    
    // Simulación de 5 ciclos de control
    for ciclo in 1..=5 {
        println!("\n{'='*60}");
        println!("CICLO #{}", ciclo);
        
        thread::sleep(Duration::from_secs(2));
        
        let mut sys = sistema.lock().unwrap();
        match sys.ciclo_control() {
            Ok(_) => println!("✓ Ciclo completado exitosamente"),
            Err(e) => println!("✗ Error en ciclo: {}", e),
        }
    }
    
    // Diagnóstico final
    {
        let sys = sistema.lock().unwrap();
        sys.diagnostico_sistema();
    }
    
    println!("\n{'='*60}");
    println!("✓ Sistema de control finalizado");
    println!("{'='*60}");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sensor_lectura() {
        let mut sensor = SensorTemperatura::new(1, ZonaHabitat::Habitat);
        assert!(sensor.leer_temperatura().is_ok());
    }

    #[test]
    fn test_actuador_potencia() {
        let mut actuador = ActuadorTermico::new(1, ZonaHabitat::Habitat);
        actuador.ajustar_potencia(50.0);
        assert_eq!(actuador.potencia, 50.0);
    }

    #[test]
    fn test_estado_critico() {
        let mut sistema = SistemaControlTemperatura::new();
        let estado = sistema.evaluar_estado(5.0, 22.0);
        assert_eq!(estado, EstadoSistema::Emergencia);
    }
}

// Made with Bob
