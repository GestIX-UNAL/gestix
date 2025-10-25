# 🖐️ Guía de Gestos - GestIX

Esta guía describe todos los gestos disponibles en el sistema GestIX y qué acción realiza cada uno.

---

## 📋 Tabla de Gestos

| Mano Izquierda | Mano Derecha | Acción | Descripción |
|----------------|--------------|--------|-------------|
| 1 dedo 👆 | Abierta (4+ dedos) 🖐️ | **Subir Brillo** | Aumenta el brillo de la pantalla en pasos de 2% |
| 1 dedo 👆 | Cerrada ✊ | **Bajar Brillo** | Disminuye el brillo de la pantalla en pasos de 2% |
| 3 dedos 🤟 | 1 dedo 👆 | **Abrir Firefox** | Abre el navegador Firefox una sola vez |

---

## 🔆 Control de Brillo (BRIGHTNESS)

### Activación del Modo
- **Gesto de activación**: Mano izquierda con 1 dedo levantado 👆
- **Flag**: `BRIGHTNESS`

### Acciones Disponibles

#### Subir Brillo ⬆️
- **Mano izquierda**: 1 dedo levantado 👆
- **Mano derecha**: Mano abierta (4 o más dedos) 🖐️
- **Efecto**: Incrementa el brillo en 2% por frame
- **Rango**: 0% - 100%

#### Bajar Brillo ⬇️
- **Mano izquierda**: 1 dedo levantado 👆
- **Mano derecha**: Mano cerrada (menos de 4 dedos) ✊
- **Efecto**: Disminuye el brillo en 2% por frame
- **Rango**: 0% - 100%

### Características
- El brillo se sincroniza con el sistema operativo
- Cambios en tiempo real
- Barra visual de progreso (en modo visual)
- Soporte para múltiples monitores

---

## 🚀 Control de Aplicaciones (APPLICATION)

### Activación del Modo
- **Gesto de activación**: Mano izquierda con 3 dedos levantados 🤟
- **Flag**: `APPLICATION`

### Acciones Disponibles

#### Abrir Firefox 🦊
- **Mano izquierda**: 3 dedos levantados 🤟
- **Mano derecha**: 1 dedo levantado 👆
- **Efecto**: Abre el navegador Firefox
- **Comportamiento**: Se abre **una sola vez** por gesto
  - El gesto debe completarse y repetirse para abrir otra instancia
  - Evita múltiples aperturas mientras se mantiene el gesto

### Características
- Apertura no bloqueante
- Control de instancia única por gesto
- Reseteo automático al terminar el gesto
- Indicador visual del estado (en modo visual)

---

## 🎯 Cómo Usar el Sistema

### Modo Visual (con ventana)
```bash
python main.py --camera
```
- Muestra la ventana de la cámara
- Visualiza la detección de manos en tiempo real
- Muestra barras de progreso y estado
- Información visual de gestos activos

### Modo Silencioso (sin ventana)
```bash
python main.py
```
- No muestra ventana visual
- Información en consola
- Menor consumo de recursos
- Ideal para uso en segundo plano

### Salir del Sistema
- Presiona `Ctrl+C` en la terminal
- O presiona `q` en la ventana visual (modo --camera)

---

## 📝 Notas Importantes

### Detección de Manos
- El sistema usa MediaPipe para la detección de manos
- Se detectan hasta 2 manos simultáneamente
- La cámara muestra una vista espejo (mano izquierda = izquierda en pantalla)

### Prioridad de Gestos
- Los gestos se detectan por la **mano izquierda** primero
- Solo se puede activar una flag a la vez
- La mano derecha define la acción específica dentro del modo

### Requisitos
- Cámara web funcional
- Buena iluminación
- Manos visibles completamente
- Firefox instalado (para el gesto de aplicaciones)

---

## 🔧 Extensibilidad

El sistema está diseñado para agregar fácilmente nuevos gestos y funcionalidades:

1. **Agregar nueva flag** en `app/utils/flags.py`
2. **Crear controlador** siguiendo el patrón de `BrightnessController` o `ApplicationController`
3. **Registrar gesto** en `Camera.detect_flag()`
4. **Registrar controlador** en `main.py`

### Flags Reservadas
- `WINDOW`: Reservado para control de ventanas
- `CONTROLLER`: Reservado para funcionalidades futuras

---

## 📚 Documentación del Código

Cada módulo está completamente documentado con:
- Docstrings en todas las clases y métodos
- Descripción de parámetros y valores de retorno
- Ejemplos de uso cuando es relevante
- Comentarios explicativos en lógica compleja

Consulta el código fuente para más detalles técnicos.
