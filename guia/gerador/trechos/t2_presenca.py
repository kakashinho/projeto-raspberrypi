from gpiozero import DistanceSensor
import statistics
from time import sleep

# Mesma configuração do presenca.py do sistema final
sensor = DistanceSensor(echo=24, trigger=23, max_distance=2, queue_len=1)

def distancia_cm():
    # mediana de 5 leituras: tira os picos falsos
    leituras = []
    for _ in range(5):
        leituras.append(sensor.distance * 100)
        sleep(0.02)
    return statistics.median(leituras)

while True:
    print(f"{distancia_cm():5.1f} cm")
    sleep(0.3)
