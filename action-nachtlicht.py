#!/usr/bin/env python3
from hermes_python.hermes import Hermes
import apa102
import time

led = apa102.APA102(num_led=3)

def set_led(color):
    led.set_pixel(0, color[0], color[1], color[2])
    led.show()

def fade_slow(mins):
    start_time = time.time()
    secs = min * 60
    r = 255
    g = 210
    b = 200
    while r>0:
        if time.time() - start_time > secs - 30:
            time.sleep(0.9)
        if r > 0:
            r -= 1
        if g > 0:
            g -= 1
        if b > 0:
            b -= 1
        time.sleep(0.115)

def fade_fast():
    r = 255
    g = 210
    b = 200
    while r>0:
        if r > 0:
            r -= 1
        if g > 0:
            g -= 1
        if b > 0:
            b -= 1
        time.sleep(0.02)


def nachtlicht(hermes, message):
    request = message.slots.minuten.first().value
    anAus = message.slots.anAus.first().value

    if "an" in anAus:
        set_led([255,210,200])
        if (request):
            if(int(request) == 1):
                hermes.publish_end_session("Nachtlicht für eine Minute an.")
            else:
                hermes.publish_end_session("Nachtlicht für " + request + " Minuten an.")
            fade_slow(int(request))
        else:
            hermes.publish_end_session("Nachtlicht an")
    else:
        hermes.publish_end_session()
        fade_fast()


with Hermes("localhost:1883") as h:
    h \
        .subscribe_intent("tierlord:Nachtlicht", nachtlicht) \
        .start()