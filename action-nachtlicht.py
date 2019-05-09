#!/usr/bin/env python3
from hermes_python.hermes import Hermes
import apa102
import time
from threading import Thread

led = apa102.APA102(num_led=3)

def set_led(color):
    led.set_pixel(0, color[0], color[1], color[2])
    led.show()

def fade_in():
    time.sleep(1)
    r = 100
    g = 75
    b = 55
    while r<255:
        set_led([r,g,b])
        r += 1
        g += 1
        b += 1
        time.sleep(0.02)


def fade_slow(mins):
    fade_in()
    print("Fading slowly")
    start_time = time.time()
    secs = mins * 60
    r = 255
    g = 230
    b = 210
    while r>0:
        set_led([r,g,b])
        if time.time() - start_time < (secs - 30):
            time.sleep(1)
        else:
            r -= 1
            if g > 0:
                g -= 1
            if b > 0:
                b -= 1
            time.sleep(0.115)
    print("Ended fading")

def fade_fast():
    print("Fading fast")
    r = 255
    g = 230
    b = 210
    while r>0:
        set_led([r,g,b])
        if r > 0:
            r -= 1
        if g > 0:
            g -= 1
        if b > 0:
            b -= 1
        time.sleep(0.02)
    print("Ended fading")

def nachtlicht(hermes, message):
    request = 0
    anAus = "an"

    if message.slots.minuten:
        request = message.slots.minuten.first().value
    if message.slots.anAus:
        anAus = message.slots.anAus.first().value

    if "an" in anAus or "ein" in anAus:
        if (request > 0):
            if(request == 1):
                hermes.publish_end_session(message.session_id, "Nacht licht für eine Minute an.")
            else:
                hermes.publish_end_session(message.session_id, "Nacht licht für " + str(request) + " Minuten an.")
            t = Thread(target=fade_slow, args=(request,))
            t.start()
        else:
            hermes.publish_end_session(message.session_id, "")
            t = Thread(target=fade_in)
            t.start()
    else:
        hermes.publish_end_session(message.session_id, "")
        t = Thread(target=fade_fast)
        t.start()


with Hermes("localhost:1883") as h:
    h \
        .subscribe_intent("tierlord:Nachtlicht", nachtlicht) \
        .start()