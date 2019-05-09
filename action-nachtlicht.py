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
    secs = mins * 60
    r = 255
    g = 210
    b = 200
    while r>0:
        set_led([r,g,b])
        if time.time() - start_time > secs - 30:
            time.sleep(1)
        else:
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
        set_led([r,g,b])
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

    if not anAus or "an" in anAus or "ein" in anAus:
        set_led([255,210,200])
        if (request):
            if(int(request) == 1):
                hermes.publish_end_session(message.session_id, "Nachtlicht für eine Minute an.")
            else:
                hermes.publish_end_session(message.session_id, "Nachtlicht für " + str(request) + " Minuten an.")
            fade_slow(int(request))
        else:
            hermes.publish_end_session(message.session_id)
    else:
        hermes.publish_end_session(message.session_id)
        fade_fast()


with Hermes("localhost:1883") as h:
    h \
        .subscribe_intent("tierlord:Nachtlicht", nachtlicht) \
        .start()