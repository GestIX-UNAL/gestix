import screen_brightness_control as sbc

class Brightness:
    def __init__(self):
        # get the brightness
        self.brightness = sbc.get_brightness(display=0)
        self.monitors = None

    
    def getBrightness(self, monitor=0):
        """Get the current brightness level of the display.
        Args:
            monitor (int): Monitor index (default: 0)
        Returns:
            int: The current brightness level (0-100).
        """
        self.brightness = sbc.get_brightness(display=monitor)
        return self.brightness   
    
    def setBrightness(self, value, monitor=0):
        """Set the brightness level of the display.
        Args:
            value (int): The desired brightness level (0-100).
            monitor (int): Monitor index (default: 0)
        """
        sbc.set_brightness(value, display=monitor)

    def getMonitors(self):
        """Get the list of available monitors.
        Returns:
            list: List of monitor names.
        """
        self.monitors = sbc.list_monitors()
        return self.monitors