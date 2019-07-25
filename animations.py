# -*- coding: utf-8 -*-
import time
from neopixel import Color


class Animation:
    flag_animation_run = False  # Global flag- animation run
    flag_animation_stop = False  # Global flag  animation stop
    def __init__(self):
        self.__class__.flag_animation_run = False 
        self.__class__.flag_animation_stop = False 


    # Set flags to stop animation
    @classmethod
    def stop_animation(self):
        Animation.flag_animation_stop = True
        Animation.flag_animation_run = False
    
    # Set flags to start animation
    @classmethod
    def start_animation(self):
        Animation.flag_animation_stop = False
        Animation.flag_animation_run = True

    @staticmethod
    def colorWipe(strip, color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        for i in range(strip.numPixels()):
            print("Czyszczenie paska")
            strip.setPixelColor(i, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
    
    @staticmethod            
    def theaterChase(strip, color, wait_ms=50, iterations=10):
            """Movie theater light style chaser animation."""
            for j in range(iterations):
                for q in range(3):
                    for i in range(0, strip.numPixels(), 3):
                        strip.setPixelColor(i + q, color)
                    strip.show()
                    time.sleep(wait_ms / 1000.0)
                    for i in range(0, strip.numPixels(), 3):
                        strip.setPixelColor(i + q, 0)
    @staticmethod
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
    
    @staticmethod           
    def rainbow(strip, wait_ms=50, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        while (True):
            if (Animation.flag_animation_stop == True):
                Animation.colorWipe(strip, Color(0, 0, 0))
                return
            if (Animation.flag_animation_run == True):
                for j in range(256 * iterations):
                    for i in range(strip.numPixels()):
                        print("Animacja prostej tęczy")
                        strip.setPixelColor(i, Animation.wheel((i + j) & 255))
                    strip.show()
                    time.sleep(wait_ms / 1000.0)
            
    @staticmethod
    def rainbowCycle(strip, wait_ms=20, iterations=1):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        while (True):
            if (Animation.flag_animation_stop == True):
                Animation.colorWipe(strip, Color(0, 0, 0))
                return
            if (Animation.flag_animation_run == True):
                for j in range(256 * iterations):
                    for i in range(strip.numPixels()):
                        print("Animacja tęczy")
                        strip.setPixelColor(i, Animation.wheel((int(i * 256 / strip.numPixels()) + j) & 255))
                    strip.show()
                    time.sleep(wait_ms / 1000.0)
        
                
    @staticmethod              
    def theaterChaseRainbow(strip, wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
            for q in range(3):
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i + q, Animation.wheel((i + j) % 255))
                strip.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i + q, 0)