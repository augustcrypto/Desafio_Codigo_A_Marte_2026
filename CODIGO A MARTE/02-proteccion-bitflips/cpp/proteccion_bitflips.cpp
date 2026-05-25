// Sistema de Protección contra Bit Flips por Radiación Cósmica
// Implementación en C++ con ECC y TMR

#include <iostream>
#include <vector>
#include <map>
#include <string>
#include <memory>
#include <algorithm>
#include <chrono>
#include <thread>
#include <iomanip>

using namespace std;
using namespace std::chrono;

enum class TipoError {
    SIN_ERROR,
    ERROR_CORREGIDO,
    ERROR_INCORREGIBLE
};

// Triple Modular Redundancy
template<typename T>
class TMRMemoria {
private:
    T replicas[3];

public:
    TMRMemoria(const T& valor) {
        replicas[0] = replicas[1] = replicas[2] = valor;
    }

    T leer_con_votacion() const {
        if (replicas[0] == replicas[1]) return replicas[0];
        if (replicas[0] == replicas[2]) return replicas[0];
        return replicas[1];
    }

    void escribir(const T& valor) {
        replicas[0] = replicas[1] = replicas[2] = valor;
    }

    bool verificar_integridad() const {
        return replicas[0] == replicas[1] && replicas[1] == replicas[2];
    }

    void corregir_errores() {
        T valor_correcto = leer_con_votacion();
        escribir(valor_correcto);
    }
};

// Hamming Code
class HammingCode {
private:
    vector<uint8_t> data;
    vector<uint8_t> parity_bits;

    vector<uint8_t> calcular_paridad(const vector<uint8_t>& datos) {
        vector<uint8_t> paridad;
        for (size_t i = 0; i < datos.size(); i += 4) {
            uint8_t d0 = i < datos.size() ? datos[i] : 0;
            uint8_t d1 = i+1 < datos.size() ? datos[i+1] : 0;
            uint8_t d2 = i+2 < datos.size() ? datos[i+2] : 0;
            uint8_t d3 = i+3 < datos.size() ? datos[i+3] : 0;
            
            paridad.push_back(d0 ^ d1 ^ d3);
            paridad.push_back(d0 ^ d2 ^ d3);
            paridad.push_back(d1 ^ d2 ^ d3);
        }
        return paridad;
    }

public:
    HammingCode(const vector<uint8_t>& datos) : data(datos) {
        parity_bits = calcular_paridad(data);
    }

    TipoError verificar_y_corregir() {
        auto paridad_actual = calcular_paridad(data);
        int errores = 0;
        size_t pos_error = 0;

        for (size_t i = 0; i < min(paridad_actual.size(), parity_bits.size()); ++i) {
            if (paridad_actual[i] != parity_bits[i]) {
                errores++;
                pos_error = i;
            }
        }

        if (errores == 0) return TipoError::SIN_ERROR;
        if (errores == 1 && pos_error < data.size()) {
            data[pos_error] ^= 1;
            parity_bits = calcular_paridad(data);
            return TipoError::ERROR_CORREGIDO;
        }
        return TipoError::ERROR_INCORREGIBLE;
    }

    const vector<uint8_t>& get_data() const { return data; }
};

// Sistema principal
class SistemaProteccionBitFlips {
private:
    map<string, unique_ptr<TMRMemoria<vector<uint8_t>>>> memoria_critica;
    map<string, unique_ptr<HammingCode>> hamming_codes;
    int errores_detectados = 0;
    int errores_corregidos = 0;
    int errores_incorregibles = 0;
    steady_clock::time_point tiempo_inicio;

public:
    SistemaProteccionBitFlips() : tiempo_inicio(steady_clock::now()) {}

    void almacenar_dato_critico(const string& clave, const vector<uint8_t>& datos) {
        memoria_critica[clave] = make_unique<TMRMemoria<vector<uint8_t>>>(datos);
        hamming_codes[clave] = make_unique<HammingCode>(datos);
        cout << "✓ Dato crítico '" << clave << "' almacenado con protección TMR + Hamming\n";
    }

    vector<uint8_t> leer_dato_critico(const string& clave) {
        if (memoria_critica.find(clave) != memoria_critica.end()) {
            return memoria_critica[clave]->leer_con_votacion();
        }
        throw runtime_error("Clave no encontrada: " + clave);
    }

    vector<string> verificar_memoria() {
        vector<string> errores_encontrados;
        cout << "\n🔍 Verificando integridad de memoria...\n";

        for (auto& [clave, tmr] : memoria_critica) {
            if (!tmr->verificar_integridad()) {
                cout << "⚠ Error TMR detectado en '" << clave << "'\n";
                tmr->corregir_errores();
                errores_detectados++;
                errores_corregidos++;
                errores_encontrados.push_back("TMR: " + clave);
            }
        }

        for (auto& [clave, hamming] : hamming_codes) {
            auto resultado = hamming->verificar_y_corregir();
            if (resultado == TipoError::ERROR_CORREGIDO) {
                cout << "✓ Error Hamming corregido en '" << clave << "'\n";
                errores_detectados++;
                errores_corregidos++;
                errores_encontrados.push_back("Hamming: " + clave);
            } else if (resultado == TipoError::ERROR_INCORREGIBLE) {
                cout << "🚨 Error incorregible en '" << clave << "'\n";
                errores_detectados++;
                errores_incorregibles++;
                errores_encontrados.push_back("Incorregible: " + clave);
            }
        }

        if (errores_encontrados.empty()) {
            cout << "✓ Memoria íntegra - Sin errores detectados\n";
        }
        return errores_encontrados;
    }

    void simular_radiacion(const string& clave) {
        cout << "\n☢️ Simulando impacto de radiación cósmica en '" << clave << "'...\n";
        
        if (memoria_critica.find(clave) != memoria_critica.end()) {
            auto datos = memoria_critica[clave]->leer_con_votacion();
            if (!datos.empty()) {
                datos[0] ^= 0xFF;
                memoria_critica[clave] = make_unique<TMRMemoria<vector<uint8_t>>>(datos);
                cout << "⚡ Réplica corrompida\n";
            }
        }
    }

    void mostrar_estadisticas() {
        auto duracion = duration_cast<seconds>(steady_clock::now() - tiempo_inicio).count();
        double tasa = duracion > 0 ? static_cast<double>(errores_detectados) / duracion : 0.0;
        double efectividad = errores_detectados > 0 ? 
            (static_cast<double>(errores_corregidos) / errores_detectados) * 100.0 : 100.0;

        cout << "\n" << string(60, '=') << "\n";
        cout << "📊 ESTADÍSTICAS DE PROTECCIÓN\n";
        cout << string(60, '=') << "\n";
        cout << "Errores detectados:     " << errores_detectados << "\n";
        cout << "Errores corregidos:     " << errores_corregidos << "\n";
        cout << "Errores incorregibles:  " << errores_incorregibles << "\n";
        cout << fixed << setprecision(2);
        cout << "Tasa de errores:        " << tasa << " errores/seg\n";
        cout << "Efectividad corrección: " << efectividad << "%\n";

        string nivel = tasa < 1.0 ? "🟢 BAJO" : 
                      tasa < 5.0 ? "🟡 MODERADO" : 
                      tasa < 10.0 ? "🟠 ALTO" : "🔴 CRÍTICO";
        cout << "Nivel de radiación:     " << nivel << "\n";
    }

    void diagnostico_completo() {
        cout << "\n" << string(60, '=') << "\n";
        cout << "🔍 DIAGNÓSTICO DEL SISTEMA\n";
        cout << string(60, '=') << "\n";
        cout << "Estado:                 ✓ Activo\n";
        cout << "Datos protegidos (TMR): " << memoria_critica.size() << "\n";
        cout << "Datos con Hamming:      " << hamming_codes.size() << "\n";
    }
};

int main() {
    cout << string(60, '=') << "\n";
    cout << "🛡️ SISTEMA DE PROTECCIÓN CONTRA BIT FLIPS - HÁBITAT MARCIANO\n";
    cout << string(60, '=') << "\n";
    cout << "Versión: 1.0.0 - C++\n";
    cout << "Protección: TMR + Hamming Code\n";
    cout << "Estado: Sistema Crítico - Máxima Prioridad\n\n";

    SistemaProteccionBitFlips sistema;

    cout << "📝 Almacenando datos críticos del sistema...\n\n";
    sistema.almacenar_dato_critico("parametros_vida", {0x4F, 0x32, 0x43, 0x4F, 0x32, 0x48, 0x32, 0x4F});
    sistema.almacenar_dato_critico("coordenadas_habitat", {0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0});
    sistema.almacenar_dato_critico("config_energia", {0xFF, 0xEE, 0xDD, 0xCC, 0xBB, 0xAA, 0x99, 0x88});

    sistema.diagnostico_completo();

    cout << "\n🔄 Iniciando monitoreo continuo...\n";

    for (int ciclo = 1; ciclo <= 5; ++ciclo) {
        cout << "\n" << string(60, '=') << "\n";
        cout << "CICLO #" << ciclo << "\n";
        cout << string(60, '=') << "\n";

        this_thread::sleep_for(seconds(1));

        if (ciclo == 2) sistema.simular_radiacion("parametros_vida");
        if (ciclo == 4) sistema.simular_radiacion("coordenadas_habitat");

        auto errores = sistema.verificar_memoria();
        if (!errores.empty()) {
            cout << "\n⚠️ Errores corregidos: " << errores.size() << "\n";
            for (const auto& error : errores) {
                cout << "   - " << error << "\n";
            }
        }

        cout << "\n📖 Verificando lectura de datos críticos:\n";
        try {
            auto datos = sistema.leer_dato_critico("parametros_vida");
            cout << "   ✓ parametros_vida: ";
            for (auto byte : datos) cout << hex << setw(2) << setfill('0') << (int)byte << " ";
            cout << dec << "\n";
        } catch (const exception& e) {
            cout << "   ✗ Error: " << e.what() << "\n";
        }
    }

    sistema.mostrar_estadisticas();
    sistema.diagnostico_completo();

    cout << "\n" << string(60, '=') << "\n";
    cout << "✓ Sistema de protección finalizado\n";
    cout << string(60, '=') << "\n";

    return 0;
}

// Made with Bob
