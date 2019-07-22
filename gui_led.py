# -*- coding: utf-8 -*-
import time
from neopixel import *


from Tkinter import *
from tkColorChooser import askcolor
import threading


# LED strip configuration:
LED_COUNT = 28  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 128  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53 

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

# Intialize the library (must be called once before other functions).
strip.begin()

flag_animation_run = False  # Global flag- animation run
flag_animation_stop = False  # Global flag  animation stop
#
r = 0;  # Red colour
g = 0;  # Green colour
b = 0;  # Blue colour
shine = 0

class GraphicalUserInterface:    
    
    def __init__(self, master):
        self.master = master
        master.title('LED WS2812 options')
        master.geometry('500x140')
        master.resizable(width=False, height=False)
        
        # Widgets

        self.labelColor = Label(master, text="Wybierz kolor podświetlenia: ")
        self.labelRainbow = Label(master, text="Efekt tęczy")
        self.labelBrightness = Label(master, text="Ustaw intensywność podświetlenia: ")
        self.labelOff = Label(master, text="Kliknij jeśli chcesz wyłączyć: ")

        self.btnColor = Button(master, text="Paleta kolorów:", command=self.getColor)
        self.btnRainbowOn = Button(master, text="     Włącz     ", command=self.startRainbow)
        self.btnRainbowOff = Button(master, text="Wyłącz", command=self.stopAnimation)
        self.btnBrightness = Button(master, text="Ustaw", command=self.changeBrightness)
        self.btnOff = Button(master, text="Wyłacz LED", command=self.offLeds)
        
        self.scale = Scale(master, orient=HORIZONTAL, from_=0, to=255)
        self.scale.set(128)
     
        # Layout
        self.labelColor.grid(column=0, row=0, sticky='w')
        self.labelRainbow.grid(column=0, row=1, sticky='w')
        self.labelBrightness.grid(column=0, row=2, sticky='w')
        self.labelOff.grid(column=0, row=3, sticky='w')

        self.btnColor.grid(column=2, row=0, sticky='e')
        self.btnRainbowOn.grid(column=1, row=1, sticky='we')
        self.btnRainbowOff.grid(column=2, row=1, sticky='we')
        self.btnBrightness.grid(column=1, row=2, sticky='we')
        self.btnOff.grid(column=2, row=3, sticky='we')

        self.scale.grid(column=2, row=2, sticky='we')
    
    def changeBrightness(self):
        global shine
        shine = self.scale.get()
        print('Shine: ', str(shine))
        strip.setBrightness(shine)
        strip.show()

    # Get colour using tkinter color chooser
    def getColor(self):
        global r, g, b
        color = askcolor(color=(g, r, b))
        grb = color[0]
        if grb != None:
            g = grb[0]
            r = grb[1]
            b = grb[2]
            colorWipe(strip, Color(r, g, b))

    # Power off leds
    def offLeds(self):
        colorWipe(strip, Color(0, 0, 0))

    # Run rainbow animation on separate thread
    def startRainbow(self):
        thread = threading.Thread(target=self.onRainbow)
        thread.start()
    
    # Set flags to run animation
    def onRainbow(self):
        global flag_animation_stop
        global flag_animation_run
        flag_animation_stop = False
        flag_animation_run = True
        #rainbow(strip)
        rainbowCycle(strip)
    
    # Set flags to stop animation
    def stopAnimation(self):
        global flag_animation_stop
        flag_animation_stop = True


    # Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    my_gui.changeBrightness()
    for i in range(strip.numPixels()):
        strip.setBrightness(shine)
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)
        
def theaterChase(strip, color, wait_ms=50, iterations=10):
        """Movie theater light style chaser animation."""
        my_gui.changeBrightness()
        for j in range(iterations):
            for q in range(3):
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i + q, color)
                strip.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i + q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)
        
def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    my_gui.changeBrightness()
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def rainbowCycle(strip, wait_ms=20, iterations=1):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    global flag_animation_run
    global flag_animation_stop
    my_gui.changeBrightness()
    while (True):
        if (flag_animation_run == True):
            for j in range(256 * iterations):
                for i in range(strip.numPixels()):
                    strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
                strip.show()
                time.sleep(wait_ms / 1000.0)
        if (flag_animation_stop == True):
            colorWipe(strip, Color(0, 0, 0))
            return
            
            
def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    my_gui.changeBrightness()
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, wheel((i + j) % 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)

if __name__ == '__main__':

    root = Tk()
    my_gui = GraphicalUserInterface(root)
    root.mainloop()
    
        