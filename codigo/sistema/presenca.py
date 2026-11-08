import statistics
import time
from gpiozero import DistanceSensor

from pinos import US_ECHO, US_TRIG

LIMIAR_CARRO_CM = 5.0
TEMPO_CONFIRMACAO_S = 1.0
AMOSTRAS_MEDIANA = 5
INTERVALO_AMOSTRAS_S = 0.02

_sensor = None
_inicio_abaixo = None

def _obter_sensor():
    global _sensor
    if _sensor is None:
        # queue_len=1: sem a fila padrão, que deixa cada leitura lenta
        _sensor = DistanceSensor(echo=US_ECHO, trigger=US_TRIG, max_distance=2, queue_len=1)
    return _sensor

def distancia_cm():
    sensor = _obter_sensor()
    leituras = []
    for i in range(AMOSTRAS_MEDIANA):
        leituras.append(sensor.distance * 100.0)
        if i < AMOSTRAS_MEDIANA - 1:
            time.sleep(INTERVALO_AMOSTRAS_S)
    return statistics.median(leituras)

def carro_presente():
    global _inicio_abaixo
    agora = time.monotonic()
    if distancia_cm() < LIMIAR_CARRO_CM:
        if _inicio_abaixo is None:
            _inicio_abaixo = agora
        return (agora - _inicio_abaixo) >= TEMPO_CONFIRMACAO_S
    else:
        _inicio_abaixo = None
        return False

def encerrar():
    """Libera os pinos do sensor de distância."""
    global _sensor
    if _sensor is not None:
        _sensor.close()
        _sensor = None

if __name__ == "__main__":
    print("Testando sensor de presença (Ctrl+C para parar)...")
    try:
        while True:
            dist = distancia_cm()
            presente = carro_presente()
            status = "CARRO PRESENTE" if presente else "livre"
            print(f"{dist:5.1f} cm | {status}")
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("\nTeste encerrado.")
