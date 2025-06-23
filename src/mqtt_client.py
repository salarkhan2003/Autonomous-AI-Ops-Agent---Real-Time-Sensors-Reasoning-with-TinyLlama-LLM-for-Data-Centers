import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Connected with result code {rc}")
    client.subscribe("data_center/racks")

def publish_data(topic, data):
    client = mqtt.Client()
    client.connect("localhost", 1883)
    client.publish(topic, json.dumps(data))
    client.disconnect()

def setup_mqtt(on_message_callback):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message_callback
    client.connect("localhost", 1883)
    client.loop_start()
    return client