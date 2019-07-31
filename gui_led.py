# -*- coding: utf-8 -*-
from neopixel import Adafruit_NeoPixel
from neopixel import Color
from animations import Animation
import tkMessageBox as mb

from Tkinter import *
from tkColorChooser import askcolor
from threading import Thread

# LED strip configuration:
# //////////////////////////////////////////////////////////////////////////

LED_COUNT = 28  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 128  # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ,
                          LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

# Intialize the library (must be called once before other functions).
strip.begin()
# ////////////////////////////////////////////////////////////////////////


class GraphicalUserInterface(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        master.title('LED WS2812 options')
        master.geometry('520x220')
        master.resizable(width=False, height=False)

        # Variables
        # ///////////////////////////////

        self.r = 0  # Red colour
        self.g = 0  # Green colour
        self.b = 0  # Blue colour
        self.shine = 0  # Brightness

        self.work_status = None  # Thread work status
        self.effect = None

        # Widgets
        # ///////////////////////////////////////////////////////////////////

        self.labelColor = Label(master, text="Wybierz kolor podświetlenia: ")
        self.labelEffect = Label(master, text="Wybierz efekt")
        self.labelBrightness = Label(
            master, text="Ustaw intensywność podświetlenia: ")
        self.labelOff = Label(master, text="Kliknij jeśli chcesz wyłączyć: ")
        self.labelRainbowAll = Label(master, text="Efekt tęczy prosty")

        self.btnColor = Button(
            master, text="Paleta kolorów:", command=self.get_color)
        self.btnEffectOn = Button(
            master, text="     Włącz     ", command=self.init_thread)
        self.btnEffectOff = Button(
            master, text="Wyłącz", command=Animation.stop_animation)
        self.btnBrightness = Button(
            master, text="Ustaw", command=self.change_brightness)
        self.btnOff = Button(master, text="Wyłacz LED", command=self.off_leds)

        self.scale = Scale(master, orient=HORIZONTAL, from_=0, to=255)
        self.scale.set(128)

        self.listBox = Listbox(master, selectmode=SINGLE, height=4)
        self.listBox.insert(1, "Efekt tęczy")
        self.listBox.insert(2, "Efekt tęczy prosty")
        self.listBox.bind('<<ListboxSelect>>', self.onselect)

        # Layout
        # ///////////////////////////////////////////////////

        self.labelEffect.grid(column=0, row=0, sticky='w')
        self.labelBrightness.grid(column=0, row=2, sticky='w')
        self.labelColor.grid(column=0, row=3, sticky='w')
        self.labelOff.grid(column=0, row=4, sticky='w')

        self.btnEffectOn.grid(column=1, row=1, sticky='we')
        self.btnEffectOff.grid(column=2, row=0, sticky='we')
        self.btnBrightness.grid(column=2, row=2, sticky='we')
        self.btnColor.grid(column=1, row=3, sticky='we')
        self.btnOff.grid(column=1, row=4, sticky='we')

        self.scale.grid(column=1, row=2, sticky='we')

        self.listBox.grid(column=1, row=0)

    def onselect(self, event):
        """Get selected item index from listBox"""
        w = event.widget
        idx = int(w.curselection()[0])
        self.effect = idx

    def init_thread(self):
        """Initialize new thread with right task"""
        animation = self.effect
        # print(animation)
        self.work_status = Thread(
            target=self.start_animations_effect, args=(animation,))
        self.work_status.start()
        self.check_thread(self.work_status, animation)

    def check_thread(self, pass_thread, thread_name):
        """Check that some thread is active, if not enable all buttons"""
        if pass_thread.isAlive() == False:
            pass_thread = None
            self.btnEffectOn['state'] = 'normal'
            self.btnColor['state'] = 'normal'
            self.btnOff['state'] = 'normal'
            effectName = self.listBox.get(thread_name)
            effectName = effectName.encode("utf-8")
            mb.showinfo("Komunikat", "{} - zakończone".format(effectName))
        else:
            self.after(1000, lambda: self.check_thread(
                pass_thread, thread_name))

    def start_animations_effect(self, animation):
        """Run correct animation on separate thread."""
        self.btnEffectOn['state'] = 'disabled'
        self.btnColor['state'] = 'disabled'
        self.btnOff['state'] = 'disabled'
        if animation == 0:
            Animation.start_animation()
            Animation.rainbow_cycle(strip)
        elif animation == 1:
            Animation.start_animation()
            Animation.rainbow(strip)
        else:
            return

    def change_brightness(self):
        """Change pixel shine between 0-min and 255-max"""
        self.shine = self.scale.get()
        strip.setBrightness(self.shine)
        strip.show()
        #print("Ustawienie podświetlenia")

    def get_color(self):
        """Get colour using tkinter color chooser."""
        color = askcolor(color=(self.g, self.r, self.b))
        grb = color[0]
        if grb != None:
            self.g = grb[0]
            self.r = grb[1]
            self.b = grb[2]
            Animation.color_wipe(strip, Color(self.r, self.g, self.b))

    def off_leds(self):
        """Power off leds."""
        Animation.color_wipe(strip, Color(0, 0, 0))
        #print("Wyłączenie ledów")


if __name__ == '__main__':
    root = Tk()
    my_gui = GraphicalUserInterface(root)
    root.mainloop()
