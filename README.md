# Smartie

```sh
# Installing on Ubuntu/Debian derivates

sudo apt -y update; sudo apt -y install python3 python3-pip python3-venv
```

```sh
# Setup venv
python3 -m venv /opt/smartie-mqtt
```

```sh
# Install packages 

. /opt/smartie-mqtt/bin/activate
pip3 install -r requirements.py
```

```sh
# Setup the config

cp config.py{.example,}
# Add your variables to the config file
```
```
The messages via MQTT are expacted to be semicolon separated. 
So far implemented
screen;(on|off)
msg;line1;line2
```
