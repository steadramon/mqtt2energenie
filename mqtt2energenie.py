import paho.mqtt.client as mqtt
import json
import time
import energenie

import json

with open('config.json') as json_data_file:
    conf = json.load(json_data_file)

client = mqtt.Client(conf['mqtt_id'])

def on_connect(client, userdata, flags, rc):
  for name in energenie.registry.names():
    print "Subscribing to " + conf['topic_prefix'] + name
    client.subscribe(conf['topic_prefix'] + name)

def on_message(client, userdata, message):
  print("message received " ,str(message.payload.decode("utf-8")))
  print("message topic=",message.topic)
  print("message qos=",message.qos)

  try:
    decoded = json.loads(message.payload.decode("utf-8"))
  except:
    return

  name = message.topic.replace(conf['topic_prefix'], "")

  try:
    switch = energenie.registry.get(name)
  except:
    return

  if 'switch' in decoded:
    if switch.has_switch():
      for i in range(2):
        switch.set_switch(bool(decoded['switch']))

if __name__ == "__main__":
  print "Starting"
  client.connect(conf['mqtt_host'])
  client.on_connect = on_connect
  client.on_message=on_message #attach function to callback

  energenie.init()
  client.loop_start()

  socket_state = False

  try:
    client.loop_start()
    while True:
      time.sleep(0.5)
  finally:
    energenie.finished()

