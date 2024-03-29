# -*- coding: utf-8 -*-
import time
from random import randint
from neopixel import Color


class Animation:
    """Class contains various animations displayed on the led strip with the 
    WS2812 driver compatible with the neopixel library."""

    def __init__(self):
        self.__class__.flag_animation_run = False
        self.__class__.flag_animation_stop = False

    @classmethod
    def stop_animation(cls):
        """Set flag to stop animation."""
        cls.flag_animation_stop = True
        cls.flag_animation_run = False

    @classmethod
    def start_animation(cls):
        """Set flag to run animation."""
        cls.flag_animation_stop = False
        cls.flag_animation_run = True
        cls.flag_thread = True

    @staticmethod
    def color_wipe(strip, color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        for i in range(strip.numPixels()):
            # print("Czyszczenie paska")
            strip.setPixelColor(i, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)

    @staticmethod
    def theater_chase(strip, color, wait_ms=50, iterations=10):
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
                Animation.color_wipe(strip, Color(0, 0, 0))
                return
            if (Animation.flag_animation_run == True):
                for j in range(256 * iterations):
                    for i in range(strip.numPixels()):
                        # print("Animacja prostej tęczy")
                        strip.setPixelColor(i, Animation.wheel((i + j) & 255))
                    strip.show()
                    time.sleep(wait_ms / 1000.0)

    @staticmethod
    def rainbow_cycle(strip, wait_ms=20, iterations=1):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        while (True):
            if (Animation.flag_animation_stop == True):
                Animation.color_wipe(strip, Color(0, 0, 0))
                return
            if (Animation.flag_animation_run == True):
                for j in range(256 * iterations):
                    for i in range(strip.numPixels()):
                        #  print("Animacja tęczy")
                        strip.setPixelColor(i, Animation.wheel(
                            (int(i * 256 / strip.numPixels()) + j) & 255))
                    strip.show()
                    time.sleep(wait_ms / 1000.0)

    @staticmethod
    def theater_chase_rainbow(strip, wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
            for q in range(3):
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i + q, Animation.wheel((i + j) % 255))
                strip.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i + q, 0)

    @staticmethod
    def flowing_point(strip, color):
        """Flowing point contains three pixels with given colour."""
        while (True):
            if (Animation.flag_animation_stop == True):
                Animation.color_wipe(strip, Color(0, 0, 0))
                return
            if (Animation.flag_animation_run == True):
                for i in range(strip.numPixels()):
                    # print(i)
                    time.sleep(0.2)
                    strip.setPixelColor(i-1, Color(0, 0, 0))
                    strip.setPixelColor(i, color)
                    strip.setPixelColor(i+1, color)
                    strip.setPixelColor(i+2, color)
                    strip.show()
                for i in range(strip.numPixels(), -1, -1):
                    # print(i)
                    time.sleep(0.2)
                    strip.setPixelColor(i+1, Color(0, 0, 0))
                    strip.setPixelColor(i, color)
                    strip.setPixelColor(i-1, color)
                    strip.setPixelColor(i-2, color)
                    strip.show()

    @staticmethod
    def random_color_flowing_point(strip):
        """Flowing point contains three pixels with random colour."""
        while (True):
            if (Animation.flag_animation_stop == True):
                Animation.color_wipe(strip, Color(0, 0, 0))
                return
            if (Animation.flag_animation_run == True):
                r = randint(0, 255)
                g = randint(0, 255)
                b = randint(0, 255)
                print(r)
                print(g)
                print(b)
                for i in range(strip.numPixels()):
                    # print(i)
                    time.sleep(0.2)
                    strip.setPixelColor(i-1, Color(0, 0, 0))
                    strip.setPixelColor(i, Color(r, g, b))
                    strip.setPixelColor(i+1, Color(r, g, b))
                    strip.setPixelColor(i+2, Color(r, g, b))
                    strip.show()
                for i in range(strip.numPixels(), -1, -1):
                    # print(i)
                    time.sleep(0.2)
                    strip.setPixelColor(i+1, Color(0, 0, 0))
                    strip.setPixelColor(i, Color(r, g, b))
                    strip.setPixelColor(i-1, Color(r, g, b))
                    strip.setPixelColor(i-2, Color(r, g, b))
                    strip.show()

    @staticmethod
    def twinkle_random(strip, count):
        """Random pixels with random colour."""
        while (True):
            if (Animation.flag_animation_stop == True):
                Animation.color_wipe(strip, Color(0, 0, 0))
                return
            if (Animation.flag_animation_run == True):
                for i in range(strip.numPixels()):
                    print("Czyszczenie paska")
                    strip.setPixelColor(i, Color(0,0,0))
                    strip.show()
    
                for i in range(count):
                    a=randint(0,strip.numPixels())
                    strip.setPixelColor(a ,Color(randint(0,255),randint(0,255),randint(0,255)))
                    strip.show()
                    print(a)
                    time.sleep(0.2)
