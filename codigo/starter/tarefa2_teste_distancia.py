from gpiozero import DistanceSensor
from time import sleep

# Atenção: na nossa placa TRIG = GPIO23 e ECHO = GPIO24
sensor = DistanceSensor(echo=24, trigger=23, max_distance=2)

while True:
    cm = sensor.distance * 100
    print(f"{cm:5.1f} cm")
    sleep(0.3)
