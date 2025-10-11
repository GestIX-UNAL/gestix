# Instructions

## Requisitos mínimos seguros

- **Python**: versión ≥ 3.9 y ≤ 3.12
  - MediaPipe en su guía oficial indica que las versiones compatibles para Python son 3.9 a 3.12. :contentReference[oaicite:0]{index=0}
  - Además, hay reportes de que en Python 3.12/3.13 la instalación de MediaPipe falla debido a ausencia de ruedas compatibles. :contentReference[oaicite:1]{index=1}
- pip (versión moderna, por lo menos ≥ 20.3)
- virtualenv
- Dependencias del sistema (Debian / Parrot / Ubuntu ejemplo):
  ```bash
  sudo apt update
  sudo apt install python3-venv python3-dev protobuf-compiler
  ```

* Cámara funcional y permisos sobre `/dev/video*`
* Permisos para modificar brillo (o acceso mediante utilitarios compatibles)
* Recursos mínimos: CPU decente y al menos 2 GB de RAM libres

---

## Setup

1. Crear entorno virtual:

   ```bash
   python3 -m venv .venv
   ```

2. Activar entorno:

   ```bash
   source .venv/bin/activate
   ```

3. Instalar dependencias Python:

   ```bash
   pip install -r requirements.txt
   ```

---

## Ejecutar PoC

```bash
python main.py --camera
```

Si hay errores por permisos o acceso a cámara:

```bash
sudo .venv/bin/python main.py --camera
```

Si la cámara aún no puede accederse:

```bash
sudo chmod 666 /dev/video0
```

---

## Requisitos de librerías con versiones seguras

En `requirements.txt` se recomienda usar rangos de versiones que han demostrado funcionar bien y ser compatibles entre sí. Por ejemplo:

```
numpy>=1.22,<1.27
opencv-python>=4.5,<5.0
mediapipe>=0.10,<0.13
screen-brightness-control>=0.24.0,<1.0
```

### Explicación de esos rangos

| Paquete                                  | Rango sugerido                                                                                                                                                | Motivo |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| `numpy>=1.22,<1.27`                      | Evitas versiones muy antiguas (faltas de funciones), y versiones demasiado nuevas que podrían romper compatibilidad con MediaPipe o OpenCV                    |        |
| `opencv-python>=4.5,<5.0`                | OpenCV 4.x es ampliamente usado con MediaPipe, evita la versión 5.x que podría introducir rupturas                                                            |        |
| `mediapipe>=0.10,<0.13`                  | Las versiones modernas de MediaPipe 0.10+ son las más estables al momento; versiones mayores podrían cambiar APIs o romper compatibilidad con ruedas binarias |        |
| `screen-brightness-control>=0.24.0,<1.0` | La versión 0.24.2 es actual estable en PyPI. ([PyPI][1]) Evitas versiones 1.x que puedan introducir rupturas                                                  |        |

---

## Compatibilidad, riesgos y notas

- Si usas Python fuera del rango (por ejemplo 3.8 o 3.13), `pip install mediapipe` puede fallar por falta de rueda compatible. ([MediaPipe][2])
- `screen-brightness-control` puede no funcionar en todos los hardware o entornos (especialmente en Wayland). En Linux puede depender de utilidades como `xbacklight`, `ddcutil`, `xrandr`, etc. ([PyPI][3])
- Tu código debe manejar casos como: `get_brightness()` devuelve lista (multimonitor) o falla por permisos.
- En Wayland, métodos de control de ventana o brillo pueden tener restricciones fuertes, por lo que para el PoC es más seguro usar X11.
- Usar resolución baja (640×480) y debouncing reduce latencia y falsos positivos.

---

## Troubleshooting

- **No módulo `mediapipe` o instalación fallida** → revisar versión de Python, usar 3.9–3.12
- **Permiso denegado (cámara)** → usar `sudo` o cambiar permisos del dispositivo
- **Brillo no cambia** → probar `brightnessctl set +10` en terminal, usar fallback
- **Lento / frames saltados** → reducir resolución / FPS

---

## Ciclo de vida de desarrollo

- Estrategia de branching: [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
- Gestión de issues: [GitHub Issues](https://docs.github.com/es/issues)
- Gestión de versiones: [GitHub Releases](https://docs.github.com/es/repositories/releasing-projects-on-github/about-releases)
- Estrategia de versiones: [SemVer](https://semver.org/)
- Formato de changelog: [Keep a Changelog](https://keepachangelog.com/)
- Convención de commits: [Conventional Commits](https://www.conventionalcommits.org/)

[1]: https://pypi.org/project/screen-brightness-control/?utm_source=chatgpt.com "screen-brightness-control"
[2]: https://mediapipe.readthedocs.io/en/latest/getting_started/troubleshooting.html?utm_source=chatgpt.com "Missing Python binary path - MediaPipe"
[3]: https://pypi.org/project/screen-brightness-control/0.11.4/?utm_source=chatgpt.com "pip install screen-brightness-control==0.11.4"
