# -*- coding: utf-8 -*-
import time
from neopixel import *
import argparse

from Tkinter import *
from tkColorChooser import askcolor
import threading 

# LED strip configuration:
LED_COUNT      = 28      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 128     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

r = 0; # Red colour
g = 0; # Green colour
b = 0; # Blue colour

flag_animation_run = False # Global flag- animation run
flag_animation_stop = False # Global flag  animation stop

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

# Intialize the library (must be called once before other functions).
strip.begin()
    
# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    changeBrightness()
    for i in range(strip.numPixels()):
        strip.setBrightness(shine)
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def changeBrightness():
    global shine
    shine = int(var.get())
    strip.setBrightness(shine)
    strip.show()
    
# Get colour using tkinter color chooser
def getColor():
    global r, g, b
    color = askcolor(color=(g, r, b)) 
    grb = color[0]
    if grb != None:
        g = grb[0]
        r = grb[1]
        b = grb[2]
        colorWipe(strip, Color(r, g, b))

# Power off leds
def offLeds():
    colorWipe(strip, Color(0,0,0))
 
# Run rainbow animation on separate thread
def startRainbow():
    thread = threading.Thread(target=onRainbow)
    thread.start()

# Set flags to run animation
def onRainbow():
    global flag_animation_stop
    global flag_animation_run
    flag_animation_stop = False
    flag_animation_run = True
    rainbow(strip)
    rainbowCycle(strip)
 
# Set flags to stop animation
def stopAnimation():
    global flag_animation_stop
    flag_animation_stop = True

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    changeBrightness()
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

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
    changeBrightness()
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=1):
    """Draw rainbow that uniformly distributes itself across all pixels."""   
    global flag_animation_run
    global flag_animation_stop
    changeBrightness()
    while(True):
        if (flag_animation_run == True):
            for j in range(256*iterations):
                for i in range(strip.numPixels()):
                    strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
                strip.show()
                time.sleep(wait_ms/1000.0)
        if (flag_animation_stop == True):
            colorWipe(strip, Color(0,0,0))
            return
    

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    changeBrightness()
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)
                
if __name__ == '__main__':
    window = Tk()
    window.title("LED WS2812 options")
    window.geometry('500x140')
    window.resizable(width=False, height=False)
    
    lblColour = Label(window, text="Wybierz kolor podświetlenia: ")
    lblColour.grid(column=0, row=0, sticky='w')
    btnColour = Button(window, text="Paleta kolorów:", command=getColor)
    btnColour.grid(column=2, row=0, sticky='e')
    
    lblRainbow = Label(window, text="Efekt tęczy")
    lblRainbow.grid(column=0, row=1, sticky='w')
    btnRainbowOn = Button(window, text="     Włącz     ", command=startRainbow)
    btnRainbowOn.grid(column=1, row=1, sticky='we')
    btnRainbowOff = Button(window, text="Wyłącz", command=stopAnimation)
    btnRainbowOff.grid(column=2, row=1, sticky='we')
    
    var = DoubleVar()
    lblBrightness = Label(window, text="Ustaw intensywność podświetlenia: ")
    lblBrightness.grid(column=0, row=2, sticky='w')
    btnBrightness = Button(window, text="Ustaw", command=changeBrightness)
    btnBrightness.grid(column=1, row=2, sticky='we')
    scale = Scale(window, variable=var, orient=HORIZONTAL, from_=0, to=255)
    scale.grid(column=2, row=2, sticky='we')
    scale.set(128)
    
    lblOff = Label(window, text="Kliknij jeśli chcesz wyłączyć: ")
    lblOff.grid(column=0, row=3, sticky='w')
    btnOff = Button(window, text="Wyłacz LED", command=offLeds)
    btnOff.grid(column=2, row=3, sticky='we')
    
    window.mainloop()
 
