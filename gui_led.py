# -*- coding: utf-8 -*-
import time
from neopixel import *
import argparse

from Tkinter import *
from tkColorChooser import askcolor

# LED strip configuration:
LED_COUNT      = 28      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 128     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

r = 0;
g = 0;
b = 0;

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()
    
# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def getColor():
    global r, g, b
    color = askcolor(color=(g, r, b)) 
    print(color)
    grb = color[0]
    print(grb)
    if grb != None:
        g = grb[0]
        print ('r: ',g)
        r = grb[1]
        print ('g: ',r)
        b = grb[2]
        print ('b: ',b)
        print("set RGB LED")
        colorWipe(strip, Color(r, g, b))

def offLeds():
    colorWipe(strip, Color(0,0,0))
    
def onRainbow():
    rainbow(strip)
    rainbowCycle(strip)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
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
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
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
    window.geometry('400x300')
    lbl = Label(window, text="Wybierz kolor podświetlenia")
    lbl.grid(column=0, row=0)
    btn = Button(window, text="Paleta kolorów", command=getColor)
    btn.grid(column=1, row=0)
    
    lbl = Label(window, text="Efekt tenczy")
    lbl.grid(column=0, row=1)
    btn = Button(window, text="Włącz", command=onRainbow)
    btn.grid(column=1, row=1)
    
    lbl = Label(window, text="Kliknij jeśli chcesz wyłączyć")
    lbl.grid(column=0, row=4)
    btn = Button(window, text="Wyłacz LED", command=offLeds)
    btn.grid(column=1, row=4)
    
    window.mainloop()
    
 

    try:

        while True:
#            print ('Color wipe animations.')
#            colorWipe(strip, Color(255, 0, 0))  # Red wipe
#            colorWipe(strip, Color(0, 255, 0))  # Blue wipe
#            colorWipe(strip, Color(0, 0, 255))  # Green wipe
#            print ('Theater chase animations.')
#            theaterChase(strip, Color(127, 127, 127))  # White theater chase
#            theaterChase(strip, Color(127,   0,   0))  # Red theater chase
#            theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
            print ('Rainbow animations.')
            rainbow(strip)
            print ('Rainbow cycle.')
            rainbowCycle(strip)
            print ('Theater case.')
            theaterChaseRainbow(strip)

    except KeyboardInterrupt:
        colorWipe(strip, Color(0,0,0), 10)
