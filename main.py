from smartie import Smartie
from paho.mqtt import client as mqc
import random
import pickle
import config

# MQTT configs
broker = config.broker
port = config.port
topic = config.topic
client_id = config.client_id
username = config.username
password = config.password
DEBUG = config.DEBUG

s = Smartie()

s.clear_screen()

cucumber = {}

def store_last(data):
    with open('last.pkl', 'wb') as f:
        pickle.dump(data, f)

def load_last():
    with open('last.pkl', 'rb') as f:
        return pickle.load(f)

def write_to_smartie(data):
    s.clear_screen()
    s.write_line(data[1],1)
    s.write_line(data[2],2)
    if DEBUG:
        print(f"Wrote to screen\n{data[1]}\n{data[2]}")

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT")
        else:
            print(f"Failed to connect\n{rc}")
    client = mqc.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqc):
    def on_message(client, userdata, msg):
        global cucumber
        topic = msg.topic
        data = msg.payload.decode().split(";")
        if len(cucumber) < 1:
            try:
                cucumber = load_last()
            except Exception as e:
                print("Couldn't load cucumber from file")
        if DEBUG:
            print(f'Received this a message from {topic}')
            print(f'lenght: {len(data)}, content: {data}')
        if data[0] == "msg":
            write_to_smartie(data)
            cucumber['msg'] = data
        elif data[0] == "screen":
            if data[1] in ["on", "off"]:
                cucumber['screen'] = data
                if data[1] == "on":
                    s.backlight_on()
                    try:
                        cucumber = load_last()
                        write_to_smartie(cucumber['msg'])
                    except:
                        pass
                    
                else:
                    s.backlight_off()
        store_last(cucumber)

    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        print("Killed by keyboard warrior")
