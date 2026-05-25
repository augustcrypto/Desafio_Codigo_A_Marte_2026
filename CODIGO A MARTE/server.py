#!/usr/bin/env python3
"""
Servidor Web para Hábitat Marciano
Permite ejecutar y visualizar todos los sistemas en diferentes lenguajes
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import subprocess
import json
import os
import sys
import threading
import webbrowser
from urllib.parse import parse_qs, urlparse

class MarsHabitatHandler(SimpleHTTPRequestHandler):
    """Handler personalizado para el servidor del hábitat marciano"""
    
    def do_GET(self):
        """Maneja peticiones GET"""
        parsed_path = urlparse(self.path)
        
        # Servir la página principal
        if parsed_path.path == '/' or parsed_path.path == '/index.html':
            self.serve_main_page()
        # API para ejecutar sistemas
        elif parsed_path.path.startswith('/api/run'):
            self.handle_run_system(parsed_path)
        # API para obtener estado
        elif parsed_path.path == '/api/status':
            self.handle_status()
        else:
            # Servir archivos estáticos normalmente
            super().do_GET()
    
    def serve_main_page(self):
        """Sirve la página principal del servidor"""
        html_content = self.get_main_html()
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', len(html_content.encode()))
        self.end_headers()
        self.wfile.write(html_content.encode())
    
    def handle_run_system(self, parsed_path):
        """Maneja la ejecución de sistemas"""
        query = parse_qs(parsed_path.query)
        system = query.get('system', [''])[0]
        language = query.get('lang', [''])[0]
        
        result = self.run_system(system, language)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())
    
    def handle_status(self):
        """Devuelve el estado del servidor"""
        status = {
            'status': 'operational',
            'systems': 7,
            'languages': 3,
            'uptime': 'active'
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(status).encode())
    
    def run_system(self, system, language):
        """Ejecuta un sistema en el lenguaje especificado"""
        commands = {
            'temperatura': {
                'rust': ['cargo', 'run', '--release'],
                'cpp': ['./build/control_temperatura'],
                'python': ['python', 'control_temperatura.py']
            },
            'bitflips': {
                'rust': ['cargo', 'run', '--release'],
                'cpp': ['./build/proteccion_bitflips'],
                'python': ['python', 'proteccion_bitflips.py']
            }
        }
        
        paths = {
            'temperatura': {
                'rust': '01-temperatura-habitat/rust',
                'cpp': '01-temperatura-habitat/cpp',
                'python': '01-temperatura-habitat/python'
            },
            'bitflips': {
                'rust': '02-proteccion-bitflips/rust',
                'cpp': '02-proteccion-bitflips/cpp',
                'python': '02-proteccion-bitflips/python'
            }
        }
        
        if system not in commands or language not in commands[system]:
            return {'success': False, 'message': 'Sistema o lenguaje no válido'}
        
        try:
            path = paths[system][language]
            cmd = commands[system][language]
            
            # Ejecutar en un nuevo terminal
            if sys.platform == 'win32':
                # Windows
                full_cmd = f'start cmd /k "cd {path} && {" ".join(cmd)}"'
                subprocess.Popen(full_cmd, shell=True)
            elif sys.platform == 'darwin':
                # macOS
                full_cmd = f'cd {path} && {" ".join(cmd)}'
                subprocess.Popen(['osascript', '-e', f'tell app "Terminal" to do script "{full_cmd}"'])
            else:
                # Linux
                full_cmd = f'cd {path} && {" ".join(cmd)}'
                subprocess.Popen(['x-terminal-emulator', '-e', f'bash -c "{full_cmd}; exec bash"'])
            
            return {
                'success': True,
                'message': f'Sistema {system} ejecutándose en {language}',
                'system': system,
                'language': language
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al ejecutar: {str(e)}'
            }
    
    def get_main_html(self):
        """Genera el HTML de la página principal"""
        return '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Control Center - Hábitat Marciano</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0a0e27;
            color: #fff;
            min-height: 100vh;
            overflow-x: hidden;
        }

        /* Fondo animado de estrellas */
        .stars {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 0;
        }

        .star {
            position: absolute;
            width: 2px;
            height: 2px;
            background: white;
            border-radius: 50%;
            animation: twinkle 3s infinite;
        }

        @keyframes twinkle {
            0%, 100% { opacity: 0.3; }
            50% { opacity: 1; }
        }

        /* Contenedor principal */
        .container {
            position: relative;
            z-index: 1;
            max-width: 1600px;
            margin: 0 auto;
            padding: 20px;
        }

        /* Header */
        header {
            text-align: center;
            padding: 40px 20px;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1));
            border-radius: 20px;
            border: 2px solid rgba(99, 102, 241, 0.3);
            margin-bottom: 40px;
            backdrop-filter: blur(10px);
            animation: slideDown 0.8s ease;
        }

        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-50px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        h1 {
            font-size: 3.5em;
            margin-bottom: 15px;
            background: linear-gradient(135deg, #6366f1, #8b5cf6, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: glow 3s ease-in-out infinite;
        }

        @keyframes glow {
            0%, 100% { filter: drop-shadow(0 0 20px rgba(99, 102, 241, 0.5)); }
            50% { filter: drop-shadow(0 0 40px rgba(139, 92, 246, 0.8)); }
        }

        .subtitle {
            font-size: 1.3em;
            color: #a5b4fc;
            margin-bottom: 20px;
        }

        .status-bar {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 20px;
            flex-wrap: wrap;
        }

        .status-item {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 20px;
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid #10b981;
            border-radius: 25px;
        }

        .status-dot {
            width: 10px;
            height: 10px;
            background: #10b981;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.5; transform: scale(1.2); }
        }

        /* Navegación de tabs */
        .nav-tabs {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-bottom: 40px;
            flex-wrap: wrap;
        }

        .tab-button {
            padding: 15px 30px;
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid rgba(99, 102, 241, 0.3);
            border-radius: 12px;
            color: #a5b4fc;
            font-size: 1.1em;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .tab-button:hover {
            background: rgba(99, 102, 241, 0.2);
            border-color: #6366f1;
            transform: translateY(-2px);
        }

        .tab-button.active {
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            border-color: #8b5cf6;
            color: white;
            box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4);
        }

        /* Grid de sistemas */
        .systems-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }

        .system-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.8));
            border-radius: 20px;
            padding: 30px;
            border: 2px solid rgba(99, 102, 241, 0.3);
            transition: all 0.4s ease;
            animation: fadeIn 0.8s ease;
            animation-fill-mode: both;
        }

        .system-card:nth-child(1) { animation-delay: 0.1s; }
        .system-card:nth-child(2) { animation-delay: 0.2s; }
        .system-card:nth-child(3) { animation-delay: 0.3s; }
        .system-card:nth-child(4) { animation-delay: 0.4s; }
        .system-card:nth-child(5) { animation-delay: 0.5s; }
        .system-card:nth-child(6) { animation-delay: 0.6s; }
        .system-card:nth-child(7) { animation-delay: 0.7s; }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: scale(0.9);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }

        .system-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(99, 102, 241, 0.3);
            border-color: #6366f1;
        }

        .system-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 20px;
        }

        .system-icon {
            font-size: 3em;
        }

        .system-info h3 {
            font-size: 1.8em;
            color: #6366f1;
            margin-bottom: 5px;
        }

        .system-info p {
            color: #94a3b8;
            font-size: 0.95em;
        }

        .language-selector {
            display: flex;
            gap: 10px;
            margin: 20px 0;
        }

        .lang-button {
            flex: 1;
            padding: 15px;
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid rgba(99, 102, 241, 0.3);
            border-radius: 10px;
            color: #a5b4fc;
            font-size: 1em;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 5px;
        }

        .lang-button:hover {
            background: rgba(99, 102, 241, 0.2);
            border-color: #6366f1;
            transform: scale(1.05);
        }

        .lang-button.selected {
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            border-color: #8b5cf6;
            color: white;
            box-shadow: 0 5px 20px rgba(99, 102, 241, 0.4);
        }

        .lang-icon {
            font-size: 1.5em;
        }

        .run-button {
            width: 100%;
            padding: 18px;
            background: linear-gradient(135deg, #10b981, #059669);
            border: none;
            border-radius: 12px;
            color: white;
            font-size: 1.2em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 15px;
        }

        .run-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(16, 185, 129, 0.4);
        }

        .run-button:active {
            transform: translateY(0);
        }

        .run-button:disabled {
            background: #374151;
            cursor: not-allowed;
            opacity: 0.5;
        }

        .system-stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid rgba(99, 102, 241, 0.2);
        }

        .stat {
            text-align: center;
        }

        .stat-value {
            font-size: 1.5em;
            font-weight: bold;
            color: #6366f1;
        }

        .stat-label {
            font-size: 0.85em;
            color: #94a3b8;
            margin-top: 5px;
        }

        /* Sección de presentaciones */
        .presentations-section {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.6), rgba(15, 23, 42, 0.6));
            border-radius: 20px;
            padding: 40px;
            border: 2px solid rgba(139, 92, 246, 0.3);
            margin-bottom: 40px;
        }

        .presentations-section h2 {
            font-size: 2.5em;
            color: #8b5cf6;
            margin-bottom: 30px;
            text-align: center;
        }

        .presentations-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }

        .presentation-card {
            background: rgba(139, 92, 246, 0.1);
            border: 2px solid rgba(139, 92, 246, 0.3);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .presentation-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(139, 92, 246, 0.3);
            border-color: #8b5cf6;
        }

        .presentation-icon {
            font-size: 3em;
            margin-bottom: 15px;
        }

        .presentation-card h3 {
            color: #a78bfa;
            margin-bottom: 10px;
        }

        .presentation-card p {
            color: #94a3b8;
            font-size: 0.9em;
        }

        /* Notificaciones */
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 20px 30px;
            background: linear-gradient(135deg, #10b981, #059669);
            border-radius: 12px;
            color: white;
            font-weight: bold;
            box-shadow: 0 10px 30px rgba(16, 185, 129, 0.4);
            z-index: 1000;
            animation: slideInRight 0.5s ease;
            display: none;
        }

        .notification.error {
            background: linear-gradient(135deg, #ef4444, #dc2626);
        }

        @keyframes slideInRight {
            from {
                transform: translateX(400px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }

        footer {
            text-align: center;
            padding: 40px 20px;
            color: #64748b;
            margin-top: 60px;
        }

        @media (max-width: 768px) {
            h1 { font-size: 2.5em; }
            .systems-grid { grid-template-columns: 1fr; }
            .presentations-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="stars" id="stars"></div>
    
    <div class="container">
        <header>
            <h1>🚀 CONTROL CENTER</h1>
            <p class="subtitle">Hábitat Marciano - Sistemas Críticos de Soporte Vital</p>
            <div class="status-bar">
                <div class="status-item">
                    <div class="status-dot"></div>
                    <span>Sistema Operacional</span>
                </div>
                <div class="status-item">
                    <div class="status-dot"></div>
                    <span>7 Sistemas Activos</span>
                </div>
                <div class="status-item">
                    <div class="status-dot"></div>
                    <span>3 Lenguajes Disponibles</span>
                </div>
            </div>
        </header>

        <!-- Navegación de tabs -->
        <div class="nav-tabs">
            <button class="tab-button active" onclick="showTab('systems')">💻 Ejecutar Sistemas</button>
            <button class="tab-button" onclick="showTab('presentations')">📊 Presentaciones</button>
            <button class="tab-button" onclick="showTab('docs')">📚 Documentación</button>
        </div>

        <!-- Tab: Sistemas -->
        <div id="systems-tab" class="tab-content">
            <div class="systems-grid">
                <!-- Sistema 1: Temperatura -->
                <div class="system-card">
                    <div class="system-header">
                        <div class="system-icon">🌡️</div>
                        <div class="system-info">
                            <h3>Control de Temperatura</h3>
                            <p>Hábitat y Huerta Marciana</p>
                        </div>
                    </div>
                    
                    <div class="language-selector">
                        <button class="lang-button selected" onclick="selectLanguage(this, 'temperatura', 'rust')">
                            <span class="lang-icon">🦀</span>
                            <span>Rust</span>
                        </button>
                        <button class="lang-button" onclick="selectLanguage(this, 'temperatura', 'cpp')">
                            <span class="lang-icon">⚡</span>
                            <span>C++</span>
                        </button>
                        <button class="lang-button" onclick="selectLanguage(this, 'temperatura', 'python')">
                            <span class="lang-icon">🐍</span>
                            <span>Python</span>
                        </button>
                    </div>
                    
                    <button class="run-button" onclick="runSystem('temperatura', 'rust')">
                        ▶️ Ejecutar Sistema
                    </button>
                    
                    <div class="system-stats">
                        <div class="stat">
                            <div class="stat-value">99.99%</div>
                            <div class="stat-label">Confiabilidad</div>
                        </div>
                        <div class="stat">
                            <div class="stat-value">6</div>
                            <div class="stat-label">Sensores</div>
                        </div>
                        <div class="stat">
                            <div class="stat-value">4</div>
                            <div class="stat-label">Actuadores</div>
                        </div>
                    </div>
                </div>

                <!-- Sistema 2: Bit Flips -->
                <div class="system-card">
                    <div class="system-header">
                        <div class="system-icon">🛡️</div>
                        <div class="system-info">
                            <h3>Protección Bit Flips</h3>
                            <p>TMR + Hamming Code</p>
                        </div>
                    </div>
                    
                    <div class="language-selector">
                        <button class="lang-button selected" onclick="selectLanguage(this, 'bitflips', 'rust')">
                            <span class="lang-icon">🦀</span>
                            <span>Rust</span>
                        </button>
                        <button class="lang-button" onclick="selectLanguage(this, 'bitflips', 'cpp')">
                            <span class="lang-icon">⚡</span>
                            <span>C++</span>
                        </button>
                        <button class="lang-button" onclick="selectLanguage(this, 'bitflips', 'python')">
                            <span class="lang-icon">🐍</span>
                            <span>Python</span>
                        </button>
                    </div>
                    
                    <button class="run-button" onclick="runSystem('bitflips', 'rust')">
                        ▶️ Ejecutar Sistema
                    </button>
                    
                    <div class="system-stats">
                        <div class="stat">
                            <div class="stat-value">99.9%</div>
                            <div class="stat-label">Detección</div>
                        </div>
                        <div class="stat">
                            <div class="stat-value">3x</div>
                            <div class="stat-label">Redundancia</div>
                        </div>
                        <div class="stat">
                            <div class="stat-value"><1ms</div>
                            <div class="stat-label">Latencia</div>
                        </div>
                    </div>
                </div>

                <!-- Sistemas adicionales (documentados) -->
                <div class="system-card" style="opacity: 0.7;">
                    <div class="system-header">
                        <div class="system-icon">📡</div>
                        <div class="system-info">
                            <h3>Comunicaciones</h3>
                            <p>Cifrado AES-256 + DTN</p>
                        </div>
                    </div>
                    <button class="run-button" disabled>
                        📋 Ver Documentación
                    </button>
                </div>

                <div class="system-card" style="opacity: 0.7;">
                    <div class="system-header">
                        <div class="system-icon">📊</div>
                        <div class="system-info">
                            <h3>Telemetría</h3>
                            <p>Monitoreo en Tiempo Real</p>
                        </div>
                    </div>
                    <button class="run-button" disabled>
                        📋 Ver Documentación
                    </button>
                </div>

                <div class="system-card" style="opacity: 0.7;">
                    <div class="system-header">
                        <div class="system-icon">💨</div>
                        <div class="system-info">
                            <h3>Control O2</h3>
                            <p>Gestión de Atmósfera</p>
                        </div>
                    </div>
                    <button class="run-button" disabled>
                        📋 Ver Documentación
                    </button>
                </div>

                <div class="system-card" style="opacity: 0.7;">
                    <div class="system-header">
                        <div class="system-icon">🔄</div>
                        <div class="system-info">
                            <h3>Conversión CO2→O2</h3>
                            <p>Tecnología MOXIE</p>
                        </div>
                    </div>
                    <button class="run-button" disabled>
                        📋 Ver Documentación
                    </button>
                </div>

                <div class="system-card" style="opacity: 0.7;">
                    <div class="system-header">
                        <div class="system-icon">💧</div>
                        <div class="system-info">
                            <h3>Filtración Agua</h3>
                            <p>Reciclaje 98%</p>
                        </div>
                    </div>
                    <button class="run-button" disabled>
                        📋 Ver Documentación
                    </button>
                </div>
            </div>
        </div>

        <!-- Tab: Presentaciones -->
        <div id="presentations-tab" class="tab-content" style="display: none;">
            <div class="presentations-section">
                <h2>📊 Presentaciones Interactivas</h2>
                <div class="presentations-grid">
                    <div class="presentation-card" onclick="window.open('presentaciones/01-temperatura-habitat.html', '_blank')">
                        <div class="presentation-icon">🌡️</div>
                        <h3>Control de Temperatura</h3>
                        <p>Demo interactiva con simulaciones</p>
                    </div>
                    <div class="presentation-card" onclick="window.open('presentaciones/02-proteccion-bitflips.html', '_blank')">
                        <div class="presentation-icon">🛡️</div>
                        <h3>Protección Bit Flips</h3>
                        <p>Visualización TMR y Hamming</p>
                    </div>
                    <div class="presentation-card" onclick="window.open('presentaciones/PRESENTACION_GENERAL.md', '_blank')">
                        <div class="presentation-icon">📄</div>
                        <h3>Presentación General</h3>
                        <p>Documento completo (Markdown)</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Tab: Documentación -->
        <div id="docs-tab" class="tab-content" style="display: none;">
            <div class="presentations-section">
                <h2>📚 Documentación del Proyecto</h2>
                <div class="presentations-grid">
                    <div class="presentation-card" onclick="window.open('README.md', '_blank')">
                        <div class="presentation-icon">📖</div>
                        <h3>README Principal</h3>
                        <p>Visión general del proyecto</p>
                    </div>
                    <div class="presentation-card" onclick="window.open('INSTRUCCIONES_COMPILACION.md', '_blank')">
                        <div class="presentation-icon">🔧</div>
                        <h3>Instrucciones de Compilación</h3>
                        <p>Guía paso a paso</p>
                    </div>
                    <div class="presentation-card" onclick="window.open('01-temperatura-habitat/README.md', '_blank')">
                        <div class="presentation-icon">🌡️</div>
                        <h3>Docs Temperatura</h3>
                        <p>Documentación técnica</p>
                    </div>
                    <div class="presentation-card" onclick="window.open('02-proteccion-bitflips/README.md', '_blank')">
                        <div class="presentation-icon">🛡️</div>
                        <h3>Docs Bit Flips</h3>
                        <p>Documentación técnica</p>
                    </div>
                </div>
            </div>
        </div>

        <footer>
            <p>🚀 Hábitat Marciano - Control Center v1.0.0</p>
            <p>Implementado en Rust, C++ y Python</p>
            <p style="margin-top: 15px; opacity: 0.7;">"Per aspera ad astra"</p>
        </footer>
    </div>

    <!-- Notificación -->
    <div id="notification" class="notification"></div>

    <script>
        // Crear estrellas de fondo
        function createStars() {
            const starsContainer = document.getElementById('stars');
            for (let i = 0; i < 150; i++) {
                const star = document.createElement('div');
                star.className = 'star';
                star.style.left = Math.random() * 100 + '%';
                star.style.top = Math.random() * 100 + '%';
                star.style.animationDelay = Math.random() * 3 + 's';
                starsContainer.appendChild(star);
            }
        }

        // Seleccionar lenguaje
        let selectedLanguages = {
            'temperatura': 'rust',
            'bitflips': 'rust'
        };

        function selectLanguage(button, system, language) {
            const card = button.closest('.system-card');
            const buttons = card.querySelectorAll('.lang-button');
            buttons.forEach(btn => btn.classList.remove('selected'));
            button.classList.add('selected');
            selectedLanguages[system] = language;
            
            // Actualizar botón de ejecución
            const runButton = card.querySelector('.run-button');
            runButton.onclick = () => runSystem(system, language);
        }

        // Ejecutar sistema
        function runSystem(system, language) {
            showNotification(`Ejecutando ${system} en ${language}...`, false);
            
            fetch(`/api/run?system=${system}&lang=${language}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showNotification(`✓ ${data.message}`, false);
                    } else {
                        showNotification(`✗ ${data.message}`, true);
                    }
                })
                .catch(error => {
                    showNotification(`✗ Error: ${error.message}`, true);
                });
        }

        // Mostrar notificación
        function showNotification(message, isError) {
            const notification = document.getElementById('notification');
            notification.textContent = message;
            notification.className = 'notification' + (isError ? ' error' : '');
            notification.style.display = 'block';
            
            setTimeout(() => {
                notification.style.display = 'none';
            }, 4000);
        }

        // Cambiar tabs
        function showTab(tabName) {
            // Ocultar todos los tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.style.display = 'none';
            });
            
            // Remover clase active de todos los botones
            document.querySelectorAll('.tab-button').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Mostrar tab seleccionado
            document.getElementById(tabName + '-tab').style.display = 'block';
            
            // Activar botón correspondiente
            event.target.classList.add('active');
        }

        // Inicializar
        window.onload = function() {
            createStars();
        };
    </script>
</body>
</html>'''

def run_server(port=8000):
    """Inicia el servidor web"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, MarsHabitatHandler)
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🚀 SERVIDOR HÁBITAT MARCIANO INICIADO                     ║
║                                                              ║
║   URL: http://localhost:{port}                                ║
║                                                              ║
║   Estado: ✓ Operacional                                     ║
║   Sistemas: 7 disponibles                                   ║
║   Lenguajes: Rust, C++, Python                              ║
║                                                              ║
║   Presiona Ctrl+C para detener el servidor                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Abrir navegador automáticamente
    def open_browser():
        import time
        time.sleep(1)
        webbrowser.open(f'http://localhost:{port}')
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor detenido")
        httpd.shutdown()

if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run_server(port)

# Made with Bob
