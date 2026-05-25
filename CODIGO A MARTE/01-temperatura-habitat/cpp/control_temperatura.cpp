// Sistema Crítico de Control de Temperatura para Hábitat Marciano
// Implementación en C++ con gestión de recursos RAII y manejo de excepciones

#include <iostream>
#include <vector>
#include <memory>
#include <thread>
#include <chrono>
#include <mutex>
#include <algorithm>
#include <numeric>
#include <iomanip>
#include <stdexcept>
#include <cmath>

// Constantes críticas del sistema
constexpr float TEMP_MIN_HABITAT = 18.0f;  // °C
constexpr float TEMP_MAX_HABITAT = 24.0f;  // °C
constexpr float TEMP_MIN_HUERTA = 20.0f;   // °C
constexpr float TEMP_MAX_HUERTA = 28.0f;   // °C
constexpr float TEMP_CRITICA_MIN = 10.0f;  // °C - Alerta crítica
constexpr float TEMP_CRITICA_MAX = 35.0f;  // °C - Alerta crítica

enum class ZonaHabitat {
    HABITAT,
    HUERTA
};

enum class EstadoSistema {
    NORMAL,
    ADVERTENCIA,
    CRITICO,
    EMERGENCIA
};

class SensorTemperatura {
private:
    uint32_t id_;
    ZonaHabitat zona_;
    float temperatura_;
    bool activo_;
    uint32_t lecturas_fallidas_;
    mutable std::mutex mutex_;

public:
    SensorTemperatura(uint32_t id, ZonaHabitat zona)
        : id_(id), zona_(zona), temperatura_(20.0f), 
          activo_(true), lecturas_fallidas_(0) {}

    float leer_temperatura() {
        std::lock_guard<std::mutex> lock(mutex_);
        
        if (!activo_ || lecturas_fallidas_ >= 3) {
            throw std::runtime_error("Sensor " + std::to_string(id_) + " inactivo o fallido");
        }

        // Simulación de lectura con variación
        float variacion = std::fmod(id_ * 0.1f, 2.0f) - 1.0f;
        temperatura_ += variacion;
        
        return temperatura_;
    }

    void calibrar() {
        std::lock_guard<std::mutex> lock(mutex_);
        lecturas_fallidas_ = 0;
        activo_ = true;
        std::cout << "✓ Sensor " << id_ << " calibrado\n";
    }

    uint32_t get_id() const { return id_; }
    bool esta_activo() const { 
        std::lock_guard<std::mutex> lock(mutex_);
        return activo_; 
    }
    float get_temperatura() const { 
        std::lock_guard<std::mutex> lock(mutex_);
        return temperatura_; 
    }
};

class ActuadorTermico {
private:
    uint32_t id_;
    ZonaHabitat zona_;
    float potencia_;  // 0.0 a 100.0 %
    bool activo_;
    mutable std::mutex mutex_;

public:
    ActuadorTermico(uint32_t id, ZonaHabitat zona)
        : id_(id), zona_(zona), potencia_(0.0f), activo_(true) {}

    void ajustar_potencia(float nueva_potencia) {
        std::lock_guard<std::mutex> lock(mutex_);
        potencia_ = std::clamp(nueva_potencia, 0.0f, 100.0f);
        std::cout << "🔧 Actuador " << id_ << " ajustado a " 
                  << std::fixed << std::setprecision(1) << potencia_ << "% potencia\n";
    }

    void activar() {
        std::lock_guard<std::mutex> lock(mutex_);
        activo_ = true;
        std::cout << "✓ Actuador " << id_ << " activado\n";
    }

    void desactivar() {
        std::lock_guard<std::mutex> lock(mutex_);
        activo_ = false;
        potencia_ = 0.0f;
        std::cout << "⚠ Actuador " << id_ << " desactivado\n";
    }

    uint32_t get_id() const { return id_; }
    bool esta_activo() const { 
        std::lock_guard<std::mutex> lock(mutex_);
        return activo_; 
    }
    float get_potencia() const { 
        std::lock_guard<std::mutex> lock(mutex_);
        return potencia_; 
    }
};

class SistemaControlTemperatura {
private:
    std::vector<std::unique_ptr<SensorTemperatura>> sensores_habitat_;
    std::vector<std::unique_ptr<SensorTemperatura>> sensores_huerta_;
    std::vector<std::unique_ptr<ActuadorTermico>> actuadores_habitat_;
    std::vector<std::unique_ptr<ActuadorTermico>> actuadores_huerta_;
    EstadoSistema estado_;
    mutable std::mutex mutex_;

    float obtener_temperatura_promedio(ZonaHabitat zona) {
        auto& sensores = (zona == ZonaHabitat::HABITAT) ? 
                         sensores_habitat_ : sensores_huerta_;
        
        std::vector<float> lecturas_validas;
        
        for (auto& sensor : sensores) {
            try {
                float temp = sensor->leer_temperatura();
                lecturas_validas.push_back(temp);
            } catch (const std::exception& e) {
                // Sensor fallido, continuar con otros
            }
        }

        if (lecturas_validas.empty()) {
            throw std::runtime_error("No hay sensores operativos");
        }

        float suma = std::accumulate(lecturas_validas.begin(), 
                                     lecturas_validas.end(), 0.0f);
        return suma / lecturas_validas.size();
    }

    EstadoSistema evaluar_estado(float temp_habitat, float temp_huerta) {
        if (temp_habitat < TEMP_CRITICA_MIN || temp_habitat > TEMP_CRITICA_MAX ||
            temp_huerta < TEMP_CRITICA_MIN || temp_huerta > TEMP_CRITICA_MAX) {
            return EstadoSistema::EMERGENCIA;
        } else if (temp_habitat < TEMP_MIN_HABITAT - 2.0f || 
                   temp_habitat > TEMP_MAX_HABITAT + 2.0f ||
                   temp_huerta < TEMP_MIN_HUERTA - 2.0f || 
                   temp_huerta > TEMP_MAX_HUERTA + 2.0f) {
            return EstadoSistema::CRITICO;
        } else if (temp_habitat < TEMP_MIN_HABITAT || temp_habitat > TEMP_MAX_HABITAT ||
                   temp_huerta < TEMP_MIN_HUERTA || temp_huerta > TEMP_MAX_HUERTA) {
            return EstadoSistema::ADVERTENCIA;
        }
        return EstadoSistema::NORMAL;
    }

    float calcular_potencia_necesaria(float temp_actual, float temp_objetivo) {
        float diferencia = temp_objetivo - temp_actual;
        float potencia = std::clamp(std::abs(diferencia) * 10.0f, 0.0f, 100.0f);
        return (diferencia > 0.0f) ? potencia : -potencia;
    }

    void ajustar_actuadores(ZonaHabitat zona, float potencia) {
        auto& actuadores = (zona == ZonaHabitat::HABITAT) ? 
                          actuadores_habitat_ : actuadores_huerta_;
        
        size_t actuadores_activos = std::count_if(actuadores.begin(), actuadores.end(),
            [](const auto& a) { return a->esta_activo(); });
        
        if (actuadores_activos > 0) {
            float potencia_por_actuador = std::abs(potencia) / actuadores_activos;
            
            for (auto& actuador : actuadores) {
                if (actuador->esta_activo()) {
                    actuador->ajustar_potencia(potencia_por_actuador);
                }
            }
        }
    }

    void protocolo_emergencia() {
        std::cout << "\n🚨 PROTOCOLO DE EMERGENCIA ACTIVADO\n";
        std::cout << "   1. Activando todos los actuadores disponibles\n";
        std::cout << "   2. Notificando a control de misión\n";
        std::cout << "   3. Preparando sistemas de respaldo\n";
        
        for (auto& actuador : actuadores_habitat_) {
            actuador->activar();
            actuador->ajustar_potencia(100.0f);
        }
        
        for (auto& actuador : actuadores_huerta_) {
            actuador->activar();
            actuador->ajustar_potencia(100.0f);
        }
    }

    std::string estado_a_string(EstadoSistema estado) const {
        switch (estado) {
            case EstadoSistema::NORMAL: return "NORMAL";
            case EstadoSistema::ADVERTENCIA: return "ADVERTENCIA";
            case EstadoSistema::CRITICO: return "CRITICO";
            case EstadoSistema::EMERGENCIA: return "EMERGENCIA";
            default: return "DESCONOCIDO";
        }
    }

    std::string icono_estado(EstadoSistema estado) const {
        switch (estado) {
            case EstadoSistema::NORMAL: return "✓";
            case EstadoSistema::ADVERTENCIA: return "⚠";
            case EstadoSistema::CRITICO: return "🔴";
            case EstadoSistema::EMERGENCIA: return "🚨";
            default: return "?";
        }
    }

public:
    SistemaControlTemperatura() : estado_(EstadoSistema::NORMAL) {
        // Redundancia: 3 sensores por zona
        for (uint32_t i = 1; i <= 3; ++i) {
            sensores_habitat_.push_back(
                std::make_unique<SensorTemperatura>(i, ZonaHabitat::HABITAT));
        }
        
        for (uint32_t i = 4; i <= 6; ++i) {
            sensores_huerta_.push_back(
                std::make_unique<SensorTemperatura>(i, ZonaHabitat::HUERTA));
        }

        // Redundancia: 2 actuadores por zona
        for (uint32_t i = 1; i <= 2; ++i) {
            actuadores_habitat_.push_back(
                std::make_unique<ActuadorTermico>(i, ZonaHabitat::HABITAT));
        }
        
        for (uint32_t i = 3; i <= 4; ++i) {
            actuadores_huerta_.push_back(
                std::make_unique<ActuadorTermico>(i, ZonaHabitat::HUERTA));
        }
    }

    void ciclo_control() {
        std::lock_guard<std::mutex> lock(mutex_);
        
        std::cout << "\n" << std::string(60, '=') << "\n";
        std::cout << "🔄 Iniciando ciclo de control de temperatura\n";
        std::cout << std::string(60, '=') << "\n";

        try {
            // Leer temperaturas
            float temp_habitat = obtener_temperatura_promedio(ZonaHabitat::HABITAT);
            float temp_huerta = obtener_temperatura_promedio(ZonaHabitat::HUERTA);

            std::cout << "\n📊 LECTURAS ACTUALES:\n";
            std::cout << std::fixed << std::setprecision(2);
            std::cout << "   Hábitat: " << temp_habitat << "°C (Rango: " 
                      << TEMP_MIN_HABITAT << "°C - " << TEMP_MAX_HABITAT << "°C)\n";
            std::cout << "   Huerta:  " << temp_huerta << "°C (Rango: " 
                      << TEMP_MIN_HUERTA << "°C - " << TEMP_MAX_HUERTA << "°C)\n";

            // Evaluar estado
            estado_ = evaluar_estado(temp_habitat, temp_huerta);
            std::cout << "\n" << icono_estado(estado_) << " ESTADO DEL SISTEMA: " 
                      << estado_a_string(estado_) << "\n";

            // Calcular y aplicar ajustes
            float temp_objetivo_habitat = (TEMP_MIN_HABITAT + TEMP_MAX_HABITAT) / 2.0f;
            float temp_objetivo_huerta = (TEMP_MIN_HUERTA + TEMP_MAX_HUERTA) / 2.0f;

            float potencia_habitat = calcular_potencia_necesaria(temp_habitat, temp_objetivo_habitat);
            float potencia_huerta = calcular_potencia_necesaria(temp_huerta, temp_objetivo_huerta);

            std::cout << "\n🎯 AJUSTES CALCULADOS:\n";
            ajustar_actuadores(ZonaHabitat::HABITAT, potencia_habitat);
            ajustar_actuadores(ZonaHabitat::HUERTA, potencia_huerta);

            // Protocolo de emergencia
            if (estado_ == EstadoSistema::EMERGENCIA) {
                protocolo_emergencia();
            }

            std::cout << "✓ Ciclo completado exitosamente\n";

        } catch (const std::exception& e) {
            std::cerr << "✗ Error en ciclo: " << e.what() << "\n";
            throw;
        }
    }

    void diagnostico_sistema() const {
        std::lock_guard<std::mutex> lock(mutex_);
        
        std::cout << "\n" << std::string(60, '=') << "\n";
        std::cout << "🔍 DIAGNÓSTICO DEL SISTEMA\n";
        std::cout << std::string(60, '=') << "\n";
        
        std::cout << "\n📡 Sensores Hábitat:\n";
        for (const auto& sensor : sensores_habitat_) {
            std::string estado = sensor->esta_activo() ? "✓ Operativo" : "✗ Inactivo";
            std::cout << "   Sensor " << sensor->get_id() << ": " << estado 
                      << " - " << std::fixed << std::setprecision(2) 
                      << sensor->get_temperatura() << "°C\n";
        }
        
        std::cout << "\n📡 Sensores Huerta:\n";
        for (const auto& sensor : sensores_huerta_) {
            std::string estado = sensor->esta_activo() ? "✓ Operativo" : "✗ Inactivo";
            std::cout << "   Sensor " << sensor->get_id() << ": " << estado 
                      << " - " << std::fixed << std::setprecision(2) 
                      << sensor->get_temperatura() << "°C\n";
        }
        
        std::cout << "\n🔧 Actuadores Hábitat:\n";
        for (const auto& actuador : actuadores_habitat_) {
            std::string estado = actuador->esta_activo() ? "✓ Operativo" : "✗ Inactivo";
            std::cout << "   Actuador " << actuador->get_id() << ": " << estado 
                      << " - " << std::fixed << std::setprecision(1) 
                      << actuador->get_potencia() << "% potencia\n";
        }
        
        std::cout << "\n🔧 Actuadores Huerta:\n";
        for (const auto& actuador : actuadores_huerta_) {
            std::string estado = actuador->esta_activo() ? "✓ Operativo" : "✗ Inactivo";
            std::cout << "   Actuador " << actuador->get_id() << ": " << estado 
                      << " - " << std::fixed << std::setprecision(1) 
                      << actuador->get_potencia() << "% potencia\n";
        }
    }
};

int main() {
    std::cout << std::string(60, '=') << "\n";
    std::cout << "🚀 SISTEMA DE CONTROL DE TEMPERATURA - HÁBITAT MARCIANO\n";
    std::cout << std::string(60, '=') << "\n";
    std::cout << "Versión: 1.0.0 - C++\n";
    std::cout << "Estado: Sistema Crítico - Máxima Prioridad\n";

    try {
        auto sistema = std::make_unique<SistemaControlTemperatura>();
        
        // Diagnóstico inicial
        sistema->diagnostico_sistema();
        
        std::cout << "\n🔄 Iniciando monitoreo continuo...\n";
        
        // Simulación de 5 ciclos de control
        for (int ciclo = 1; ciclo <= 5; ++ciclo) {
            std::cout << "\n" << std::string(60, '=') << "\n";
            std::cout << "CICLO #" << ciclo << "\n";
            
            std::this_thread::sleep_for(std::chrono::seconds(2));
            
            sistema->ciclo_control();
        }
        
        // Diagnóstico final
        sistema->diagnostico_sistema();
        
        std::cout << "\n" << std::string(60, '=') << "\n";
        std::cout << "✓ Sistema de control finalizado\n";
        std::cout << std::string(60, '=') << "\n";

    } catch (const std::exception& e) {
        std::cerr << "🚨 Error crítico: " << e.what() << "\n";
        return 1;
    }

    return 0;
}

// Made with Bob
