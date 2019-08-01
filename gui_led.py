# -*- coding: utf-8 -*-
from threading import Thread

import tkMessageBox as mb
from Tkinter import *
from neopixel import Color
from tkColorChooser import askcolor

from animations import Animation
from strip_config import strip


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
        self.effect = None  # Active animation effect from listBox

        # Widgets
        # ///////////////////////////////////////////////////////////////////

        self.labelColor = Label(master, text="Wybierz kolor podświetlenia: ")
        self.labelEffect = Label(master, text="Wybierz efekt")
        self.labelBrightness = Label(
            master, text="Ustaw intensywność podświetlenia: ")
        self.labelOff = Label(master, text="Kliknij jeśli chcesz wyłączyć: ")
        self.labelRainbowAll = Label(master, text="Efekt tęczy prosty")

        self.btnGetColor = Button(
            master, text="Paleta kolorów:", command=self.get_color)
        self.btnSetColor = Button(
            master, text="Ustaw", command=self.set_color)
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
        self.listBox.insert(3, "Efekt point")
        self.listBox.insert(4, "Efekt random point")
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
        self.btnGetColor.grid(column=1, row=3, sticky='we')
        self.btnSetColor.grid(column=2, row=3, sticky='we')
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
            self.btnSetColor['state'] = 'normal'
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
        self.btnGetColor['state'] = 'disabled'
        self.btnSetColor['state'] = 'disabled'
        self.btnOff['state'] = 'disabled'
        if animation == 0:
            Animation.start_animation()
            Animation.rainbow_cycle(strip)
        elif animation == 1:
            Animation.start_animation()
            Animation.rainbow(strip)
        elif animation == 2:
            Animation.start_animation()
            Animation.flowing_point(strip, Color(self.r, self.g, self.b))
        elif animation == 3:
            Animation.start_animation()
            Animation.random_color_flowing_point(strip)
        else:
            return

    def change_brightness(self):
        """Change pixel shine between 0-min and 255-max"""
        self.shine = self.scale.get()
        strip.setBrightness(self.shine)
        strip.show()
        # print("Ustawienie podświetlenia")

    def get_color(self):
        """Get colour using tkinter color chooser."""
        color = askcolor(color=(self.g, self.r, self.b))
        grb = color[0]
        if grb != None:
            self.g = grb[0]
            self.r = grb[1]
            self.b = grb[2]

    def set_color(self):
        Animation.color_wipe(strip, Color(self.r, self.g, self.b))

    def off_leds(self):
        """Power off leds."""
        Animation.color_wipe(strip, Color(0, 0, 0))
        # print("Wyłączenie ledów")


if __name__ == '__main__':
    root = Tk()
    my_gui = GraphicalUserInterface(root)
    root.mainloop()
