
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

pin_a = 14
pin_b = 15

def analog_read():
    GPIO.setup(pin_a, GPIO.IN)
    GPIO.setup(pin_b, GPIO.OUT)
    GPIO.output(pin_b, False)
    time.sleep(0.00182)

    GPIO.setup(pin_b, GPIO.IN)
    GPIO.setup(pin_a, GPIO.OUT)
    GPIO.output(pin_a, True)

    inicio = time.perf_counter()

    while not GPIO.input(pin_b):
        if time.perf_counter() - inicio > 0.01:
            GPIO.output(pin_a, False)
            return None

    tempo = (time.perf_counter() - inicio) * 1000
    GPIO.output(pin_a, False)

    return tempo

try:
    while True:
        tempo = analog_read()

        if tempo is not None:
            porcentagem = (tempo - 0.428) / (0.907 - 0.428) * 100
            porcentagem = max(0, min(100, porcentagem))
            print(f"Potenciômetro: {porcentagem:.1f}%")

        time.sleep(0.05)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()

