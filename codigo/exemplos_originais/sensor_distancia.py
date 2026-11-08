from gpiozero import DistanceSensor, LED
from time import sleep
 
sensor = DistanceSensor(
    echo=23,
    trigger=24,
    max_distance=2,
    threshold_distance=0.2
)
 
led = LED(2)
 
while True:
    distancia = sensor.distance
    print(f"Distância: {distancia:.2f} m")
 
    if distancia < 0.2:
        led.on()
        print("Objeto próximo: LED LIGADO")
    else:
        led.off()
        print("Objeto distante: LED DESLIGADO")
 
    sleep(0.5)
