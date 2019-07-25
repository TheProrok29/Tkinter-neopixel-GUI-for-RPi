# -*- coding: utf-8 -*-
from neopixel import Adafruit_NeoPixel
from neopixel import Color
from animations import Animation

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



class GraphicalUserInterface:    
    
    def __init__(self, master):
        self.master = master
        master.title('LED WS2812 options')
        master.geometry('500x180')
        master.resizable(width=False, height=False)
#
        self.r = 0;  # Red colour
        self.g = 0;  # Green colour
        self.b = 0;  # Blue colour
        self.shine = 0

        # Widgets

        self.labelColor = Label(master, text="Wybierz kolor podświetlenia: ")
        self.labelRainbow = Label(master, text="Efekt tęczy")
        self.labelBrightness = Label(master, text="Ustaw intensywność podświetlenia: ")
        self.labelOff = Label(master, text="Kliknij jeśli chcesz wyłączyć: ")
        self.labelRainbowAll = Label(master, text="Efekt tęczy prosty")
        
        self.btnColor = Button(master, text="Paleta kolorów:", command=self.get_color)
        self.btnRainbowOn = Button(master, text="     Włącz     ", command=self.start_rainbow)
        self.btnRainbowOff = Button(master, text="Wyłącz", command=Animation.stop_animation)
        self.btnBrightness = Button(master, text="Ustaw", command=self.change_brightness)
        self.btnOff = Button(master, text="Wyłacz LED", command=self.off_leds)
        self.btnRainbowAllOn = Button(master, text="    Włącz    ", command=self.start_rainbow_all)
        self.btnRainbowOff2 = Button(master, text="Wyłącz", command=Animation.stop_animation)
        
        self.scale = Scale(master, orient=HORIZONTAL, from_=0, to=255)
        self.scale.set(128)
     
        # Layout
        self.labelColor.grid(column=0, row=0, sticky='w')
        self.labelRainbow.grid(column=0, row=1, sticky='w')
        self.labelBrightness.grid(column=0, row=2, sticky='w')
        self.labelOff.grid(column=0, row=3, sticky='w')
        self.labelRainbowAll.grid(column=0, row=4, sticky='w')

        self.btnColor.grid(column=2, row=0, sticky='e')
        self.btnRainbowOn.grid(column=1, row=1, sticky='we')
        self.btnRainbowOff.grid(column=2, row=1, sticky='we')
        self.btnBrightness.grid(column=1, row=2, sticky='we')
        self.btnOff.grid(column=2, row=3, sticky='we')
        self.btnRainbowAllOn.grid(column=1, row=4, sticky='we')
        self.btnRainbowOff2.grid(column=2, row=4, sticky='we')
        
        self.scale.grid(column=2, row=2, sticky='we')
    
    def change_brightness(self):
        self.shine = self.scale.get()
        strip.setBrightness(self.shine)
        strip.show()
        print("Ustawienie podświetlenia")

    # Get colour using tkinter color chooser
    def get_color(self):
        color = askcolor(color=(self.g, self.r, self.b))
        grb = color[0]
        if grb != None:
            self.g = grb[0]
            self.r = grb[1]
            self.b = grb[2]
            Animation.colorWipe(strip, Color(self.r, self.g, self.b), self.shine)

    # Power off leds
    def off_leds(self):
        Animation.colorWipe(strip, Color(0, 0, 0))
        print("Wyłączenie ledów")

    # Run rainbow animation on separate thread
    def start_rainbow(self):
        Animation.start_animation()
        thread = threading.Thread(target=Animation.rainbowCycle, args=(strip,))
        thread.start()
    
    # Run rainbow animation on separate thread
    def start_rainbow_all(self):
        Animation.start_animation()
        thread = threading.Thread(target=Animation.rainbow, args=(strip,))
        thread.start()



if __name__ == '__main__':

    root = Tk()
    my_gui = GraphicalUserInterface(root)
    root.mainloop()
    
        