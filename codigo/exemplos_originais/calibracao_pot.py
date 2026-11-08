
import RPi.GPIO as GPIO
import time
import statistics

GPIO.setmode(GPIO.BCM)

pin_a = 12
pin_b = 25

DELAY_DESCARGA = 0.00182
TIMEOUT = 0.1

def discharge():
    GPIO.setup(pin_a, GPIO.IN)
    GPIO.setup(pin_b, GPIO.OUT)
    GPIO.output(pin_b, False)
    time.sleep(DELAY_DESCARGA)

def charge_time():
    GPIO.setup(pin_b, GPIO.IN)
    GPIO.setup(pin_a, GPIO.OUT)

    GPIO.output(pin_a, True)
    inicio = time.perf_counter()

    while not GPIO.input(pin_b):
        if time.perf_counter() - inicio > TIMEOUT:
            GPIO.output(pin_a, False)
            return None

    duracao = time.perf_counter() - inicio
    GPIO.output(pin_a, False)

    return duracao * 1000

def analog_read():
    discharge()
    return charge_time()

try:
    while True:
        leituras = []

        for _ in range(9):
            valor = analog_read()
            if valor is not None:
                leituras.append(valor)

        if leituras:
            print(f"Mediana: {statistics.median(leituras):.3f} ms")
        else:
            print("TIMEOUT: nenhuma leitura válida")

        time.sleep(0.2)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()

