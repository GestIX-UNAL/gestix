# GestIX - Gesture Interaction for UNIX-based Systems

**Universidad Nacional de Colombia**

![License](https://img.shields.io/github/license/GestIX-UNAL/gestix)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/opencv-4.0+-green.svg)
![MediaPipe](https://img.shields.io/badge/mediapipe-latest-orange.svg)

## 📖 Descripción

GestIX es un sistema avanzado de interacción gestual diseñado específicamente para entornos GNU/Linux que permite el control de funciones básicas del sistema operativo mediante gestos capturados y procesados en tiempo real a través de dispositivos de captura de video estándar.

### 🎯 Características Implementadas

- **Control de brillo de pantalla** mediante gestos naturales
- **Control de aplicaciones** (abrir/cerrar) con gestos de palma
- **Reconocimiento en tiempo real** con MediaPipe
- **Doble modo de ejecución**: Visual (--camera) o silencioso
- **Alta precisión** mediante técnicas avanzadas de visión artificial
- **Sistema modular** fácil de extender con nuevos controladores

## 🔧 Tecnologías

- **Python** - Lenguaje principal de desarrollo
- **OpenCV** - Procesamiento de imágenes y visión artificial
- **MediaPipe** - Reconocimiento gestual de alta precisión
- **GNU/Linux** - Sistema operativo objetivo

## 🚀 Objetivos del Proyecto

### Objetivo Principal
Desarrollo de un sistema de interacción gestual especializado que traduce gestos capturados por cámara a comandos nativos del sistema operativo Linux, garantizando precisión y eficiencia mediante un conjunto optimizado de gestos predefinidos.

### Objetivos Específicos
- ✅ Implementar reconocimiento gestual en tiempo real
- ✅ Integrar control de brillo y aplicaciones del sistema
- ✅ Optimizar la precisión con un conjunto limitado de gestos
- ✅ Crear una interfaz intuitiva y natural para usuarios

## 🎓 Justificación Académica

Este proyecto aplica conceptos avanzados de:
- **Visión artificial aplicada**
- **Reconocimiento de patrones en tiempo real**
- **Procesamiento avanzado de imágenes**
- **Interfaces hombre-máquina**

### Competencias Desarrolladas
- Implementación práctica de algoritmos de visión artificial
- Integración de bibliotecas especializadas (OpenCV, MediaPipe)
- Desarrollo de sistemas interactivos en tiempo real
- Optimización de rendimiento para aplicaciones críticas

## 🌍 Impacto Social

GestIX promueve una nueva forma de interacción con los sistemas operativos, implementando el control mediante gestos naturales. Esto:

- ✨ Fomenta la adopción de tecnologías más intuitivas
- 🔬 Impulsa la investigación en interfaces hombre-máquina
- 🚀 Abre camino a desarrollos transformadores
- 🤝 Mejora la accesibilidad tecnológica
- 🌟 Transforma la relación usuario-dispositivo en la vida cotidiana

## 🛠️ Instalación

```bash
# Clonar el repositorio
git clone https://github.com/GestIX-UNAL/gestix.git
cd gestix

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el sistema (requiere permisos para control de brillo)
sudo .venv/bin/python main.py --camera
```

## 🎮 Gestos Disponibles

### Control de Brillo
- **Mano izquierda**: 1 dedo levantado (activa el modo)
- **Mano derecha abierta** (4+ dedos): Sube el brillo
- **Mano derecha cerrada** (puño): Baja el brillo

### Control de Aplicaciones
- **Mano izquierda**: 3 dedos levantados (activa el modo)
- **Mano derecha palma abierta** (4-5 dedos): Abre aplicación
- **Mano derecha palma cerrada** (puño): Cierra aplicación y reinicia el gesto

## 🖥️ Modos de Ejecución

```bash
# Modo visual (con interfaz de cámara)
sudo .venv/bin/python main.py --camera

# Modo silencioso (solo consola)
sudo .venv/bin/python main.py
```

## 📋 Requisitos del Sistema

- **SO**: GNU/Linux (Ubuntu 20.04+ recomendado)
- **Python**: 3.8 o superior
- **Cámara**: Dispositivo de captura de video compatible (webcam)
- **Permisos**: Acceso sudo para control de brillo del sistema
- **Dependencias del sistema**: `xdg-utils` (para abrir aplicaciones)

## 🤝 Contribución

Este proyecto es parte del trabajo académico de la Universidad Nacional de Colombia. Las contribuciones son bienvenidas siguiendo las directrices del proyecto.

## 📄 Licencia

Este proyecto está bajo la licencia especificada en el archivo [LICENSE](LICENSE).

## 👥 Equipo de Desarrollo

**Universidad Nacional de Colombia**
- Facultad de Ingeniería
- Proyecto de Visión Artificial

---

**GestIX** - Transformando la interacción humano-computador a través de gestos naturales 🤲
