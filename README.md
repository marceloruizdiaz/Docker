docker run -it --name mos2 -p 1883:1883  -v /home/MQTT/mosquitto:/mosquitto/ -v /home/MQTT/mosquitto/log:/mosquitto/log -v /home/MQTT/mosquitto/data:/mosquitto/data  eclipse-mosquitto
