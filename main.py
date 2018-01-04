import os
import binascii
import yaml
import paho.mqtt.client as mqtt
import time

from lib.display import Display

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.yaml'), 'r') as ymlfile:
    CONFIG = yaml.load(ymlfile)

user = CONFIG['mqtt']['user']
password = CONFIG['mqtt']['password']
host = CONFIG['mqtt']['host']
port = CONFIG['mqtt']['port']
command_topic = CONFIG['mqtt']['command_topic']
state_topic = CONFIG['mqtt']['state_topic']

def update_state(value, topic):
    print "State change triggered: %s -> %s" % (topic, value)

    client.publish(topic, value, retain=True)

def on_connect(client, userdata, rc):
    print "Connected with result code: %s" % mqtt.connack_string(rc)
    print "Listening for commands on %s" % command_topic

    client.subscribe(command_topic)

def execute_command(display, command):
    print "Executing command %s on displays" % command
    if command == "ON" and display.state == 'OFF':
        display.on()
    elif command == "OFF" and display.state == 'ON':
        display.off()
    else:
        print "Invalid command: %s" % command

client = mqtt.Client(client_id="MQTTMacDisplays_" + binascii.b2a_hex(os.urandom(6)), clean_session=True, userdata=None, protocol="MQTTv31")
client.on_connect = on_connect
client.username_pw_set(user, password=password)
client.connect(host, port, 60)

if __name__ == "__main__":
    display = Display()

    def on_message(client, userdata, msg, display=display):
        execute_command(display, str(msg.payload))

    def on_state_change(value, topic=state_topic):
        update_state(value, topic)

    client.message_callback_add(command_topic, on_message)
    display.onStateChange.addHandler(on_state_change)
    client.publish(state_topic, display.state, retain=True)
    client.loop_start()

    initialState = display.state
    lastCheck = time.time()
    while True:
        if (time.time() - lastCheck) > 30:
            newState = display.state

            if (newState != initialState):
                display.onStateChange.fire(newState)

            lastCheck = time.time()
        time.sleep(0.5)
