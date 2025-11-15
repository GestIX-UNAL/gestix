import subprocess
import platform

class Volume:
    """
    Clase para controlar el volumen del sistema en diferentes plataformas.
    Soporta Linux (PulseAudio/ALSA), Windows y macOS.
    """
    
    def __init__(self):
        """
        Inicializa el controlador de volumen según el sistema operativo.
        """
        self.platform = platform.system()
        self.volume = self.getVolume()
    
    def getVolume(self):
        """
        Obtiene el nivel de volumen actual del sistema.
        
        Returns:
            int: El nivel de volumen actual (0-100).
        """
        try:
            if self.platform == "Linux":
                # Intentar con pactl (PulseAudio)
                try:
                    result = subprocess.run(
                        ["pactl", "get-sink-volume", "@DEFAULT_SINK@"],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    # Parsear la salida para obtener el porcentaje
                    # Ejemplo de salida: "Volume: front-left: 65536 / 100% / 0.00 dB, front-right: 65536 / 100% / 0.00 dB"
                    output = result.stdout
                    if '%' in output:
                        # Extraer el primer porcentaje encontrado
                        volume_str = output.split('%')[0].split()[-1]
                        return int(volume_str)
                except (subprocess.CalledProcessError, FileNotFoundError):
                    # Si pactl no está disponible, intentar con amixer
                    result = subprocess.run(
                        ["amixer", "get", "Master"],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    # Parsear la salida de amixer
                    for line in result.stdout.split('\n'):
                        if 'Playback' in line and '%' in line:
                            volume_str = line.split('[')[1].split('%')[0]
                            return int(volume_str)
                            
            elif self.platform == "Darwin":  # macOS
                result = subprocess.run(
                    ["osascript", "-e", "output volume of (get volume settings)"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                return int(result.stdout.strip())
                
            elif self.platform == "Windows":
                # En Windows usaremos pycaw (si está instalado)
                try:
                    from ctypes import cast, POINTER
                    from comtypes import CLSCTX_ALL
                    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                    
                    devices = AudioUtilities.GetSpeakers()
                    interface = devices.Activate(
                        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                    volume_obj = cast(interface, POINTER(IAudioEndpointVolume))
                    current_volume = volume_obj.GetMasterVolumeLevelScalar()
                    return int(current_volume * 100)
                except ImportError:
                    print("Warning: pycaw no está instalado para Windows")
                    return 50
                    
        except Exception as e:
            print(f"Error al obtener volumen: {e}")
            return 50  # Valor por defecto
    
    def setVolume(self, value):
        """
        Establece el nivel de volumen del sistema.
        
        Args:
            value (int): El nivel de volumen deseado (0-100).
        """
        # Asegurar que el valor esté en el rango válido
        value = max(0, min(100, int(value)))
        
        try:
            if self.platform == "Linux":
                # Intentar con pactl (PulseAudio)
                try:
                    subprocess.run(
                        ["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{value}%"],
                        check=True
                    )
                except (subprocess.CalledProcessError, FileNotFoundError):
                    # Si pactl no está disponible, intentar con amixer
                    subprocess.run(
                        ["amixer", "set", "Master", f"{value}%"],
                        check=True
                    )
                    
            elif self.platform == "Darwin":  # macOS
                subprocess.run(
                    ["osascript", "-e", f"set volume output volume {value}"],
                    check=True
                )
                
            elif self.platform == "Windows":
                try:
                    from ctypes import cast, POINTER
                    from comtypes import CLSCTX_ALL
                    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                    
                    devices = AudioUtilities.GetSpeakers()
                    interface = devices.Activate(
                        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                    volume_obj = cast(interface, POINTER(IAudioEndpointVolume))
                    volume_obj.SetMasterVolumeLevelScalar(value / 100, None)
                except ImportError:
                    print("Warning: pycaw no está instalado para Windows")
                    
            self.volume = value
            
        except Exception as e:
            print(f"Error al establecer volumen: {e}")
    
    def increaseVolume(self, step=5):
        """
        Incrementa el volumen en un paso determinado.
        
        Args:
            step (int): Cantidad a incrementar (default: 5).
        """
        current = self.getVolume()
        new_volume = min(100, current + step)
        self.setVolume(new_volume)
        
    def decreaseVolume(self, step=5):
        """
        Decrementa el volumen en un paso determinado.
        
        Args:
            step (int): Cantidad a decrementar (default: 5).
        """
        current = self.getVolume()
        new_volume = max(0, current - step)
        self.setVolume(new_volume)
    
    def mute(self):
        """
        Silencia el audio del sistema.
        """
        try:
            if self.platform == "Linux":
                try:
                    subprocess.run(
                        ["pactl", "set-sink-mute", "@DEFAULT_SINK@", "1"],
                        check=True
                    )
                except (subprocess.CalledProcessError, FileNotFoundError):
                    subprocess.run(
                        ["amixer", "set", "Master", "mute"],
                        check=True
                    )
                    
            elif self.platform == "Darwin":
                subprocess.run(
                    ["osascript", "-e", "set volume output muted true"],
                    check=True
                )
                
            elif self.platform == "Windows":
                try:
                    from ctypes import cast, POINTER
                    from comtypes import CLSCTX_ALL
                    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                    
                    devices = AudioUtilities.GetSpeakers()
                    interface = devices.Activate(
                        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                    volume_obj = cast(interface, POINTER(IAudioEndpointVolume))
                    volume_obj.SetMute(1, None)
                except ImportError:
                    print("Warning: pycaw no está instalado para Windows")
                    
        except Exception as e:
            print(f"Error al silenciar: {e}")
    
    def unmute(self):
        """
        Desactiva el silencio del audio del sistema.
        """
        try:
            if self.platform == "Linux":
                try:
                    subprocess.run(
                        ["pactl", "set-sink-mute", "@DEFAULT_SINK@", "0"],
                        check=True
                    )
                except (subprocess.CalledProcessError, FileNotFoundError):
                    subprocess.run(
                        ["amixer", "set", "Master", "unmute"],
                        check=True
                    )
                    
            elif self.platform == "Darwin":
                subprocess.run(
                    ["osascript", "-e", "set volume output muted false"],
                    check=True
                )
                
            elif self.platform == "Windows":
                try:
                    from ctypes import cast, POINTER
                    from comtypes import CLSCTX_ALL
                    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                    
                    devices = AudioUtilities.GetSpeakers()
                    interface = devices.Activate(
                        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                    volume_obj = cast(interface, POINTER(IAudioEndpointVolume))
                    volume_obj.SetMute(0, None)
                except ImportError:
                    print("Warning: pycaw no está instalado para Windows")
                    
        except Exception as e:
            print(f"Error al desactivar silencio: {e}")
