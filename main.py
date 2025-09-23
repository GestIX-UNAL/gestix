from core.modules.brightness.brightness import Brightness
def main():

    brightness = Brightness()
    print("Brillo actual: ", brightness.getBrightness())
    brightness.setBrightness(65)
    print("Brillo seteado a: ", brightness.getBrightness())
    
if __name__ == "__main__":
    main()