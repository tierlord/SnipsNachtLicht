#!/usr/bin/env python3
from hermes_python.hermes import Hermes
import paho.mqtt.client as mqtt

MQTT_ADDR = "localhost"

def nachtlicht_callback(hermes, message):
    request = 0
    anAus = "an"

    client = mqtt.Client()
    client.connect(MQTT_ADDR, 1883, 20)

    if message.slots.minuten:
        request = message.slots.minuten.first().value
    if message.slots.anAus:
        anAus = message.slots.anAus.first().value

    if "an" in anAus or "ein" in anAus:
        if (request > 0):
            if(request == 1):
                hermes.publish_end_session(message.session_id, "Nacht licht für eine Minute an.")
            else:
                hermes.publish_end_session(message.session_id, "Nacht licht für " + str((int)request) + " Minuten an.")
            client.publish("snips/led/an", payload=request)
        else:
            client.publish("snips/led/an")
            hermes.publish_end_session(message.session_id, "")            
    else:
        client.publish("snips/led/aus")
        hermes.publish_end_session(message.session_id, "")
    client.disconnect()

with Hermes("localhost:1883") as h:
    h \
        .subscribe_intent("tierlord:NachtlichtAnAus", nachtlicht_callback) \
        .start()