import numpy as np
from python import led, microphone, dsp, config
import time
import tkinter
from tkinter.colorchooser import askcolor

# ESP8266 uses WiFi communication
if config.DEVICE == 'esp8266':
    import socket
    _sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

_gamma = np.load(config.GAMMA_TABLE_PATH)
"""Gamma lookup table used for nonlinear brightness correction"""

_prev_pixels = np.tile(253, (4, config.N_PIXELS))
"""Pixel values that were most recently displayed on the LED strip"""

# Initialize LEDs
led.pixels *= 0
led.update()
led.pixels = np.tile(1, (4, config.N_PIXELS))
"""Pixel values for the LED strip"""


def roll():
    single_color_full_bri = np.zeros

    # Turn all pixels off
    led.pixels *= 0
    led.pixels[0, 0] = 255  # Set 1st pixel red
    led.pixels[1, 1] = 255  # Set 2nd pixel green
    led.pixels[2, 2] = 255  # Set 3rd pixel blue
    led.pixels[3, 3] = 255  # Set 3rd pixel white
    print('Starting LED strand test')
    while True:
        led.pixels = np.roll(led.pixels, 1, axis=1)
        led.update()
        time.sleep(0.01)

def color_cycle():
    led.pixels *= 0
    #led.pixels = np.stack(np.tile(255, (1, config.N_PIXELS)), np.tile(0, (3, config.N_PIXELS)))
    a = np.zeros(shape=(3, config.N_PIXELS))
    led.pixels = np.append(a, np.tile(255, (1, config.N_PIXELS)), axis=0)
    while True:
        led.pixels = np.roll(led.pixels, 1, axis=0)
        led.update()
        time.sleep(1)

def single_color(color='white'):
    rgb = askcolor(title="Tkinter Color Chooser")

    a = np.empty((0, config.N_PIXELS), int)
    a = np.append(a, np.tile(int(rgb[0][0]), (1, config.N_PIXELS)), axis=0)
    a = np.append(a, np.tile(int(rgb[0][1]), (1, config.N_PIXELS)), axis=0)
    a = np.append(a, np.tile(int(rgb[0][2]), (1, config.N_PIXELS)), axis=0)
    a = np.append(a, np.tile(0, (1, config.N_PIXELS)), axis=0)
    led.pixels = a
    led.update()
    time.sleep(1)
    led.update()


def clear_all():
    led.pixels *= 0
    led.update()

if __name__ == '__main__':
    roll()
    #color_cycle()

