import RPi.GPIO as GPIO
from time import sleep

# Mesma base do cancelas.py final: PWM de 50 Hz com RPi.GPIO
PINOS = {"entrada": 13, "saida": 26}   # J2 e J3

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
for pino in PINOS.values():
    GPIO.setup(pino, GPIO.OUT)

pwms = {nome: GPIO.PWM(pino, 50) for nome, pino in PINOS.items()}
for pwm in pwms.values():
    pwm.start(0)


def duty(graus):
    # SG90: pulso de 0,5 a 2,5 ms cobre os 180 graus (20 ms por ciclo)
    pulso_ms = 0.5 + (graus / 180.0) * 2.0
    return pulso_ms / 20.0 * 100.0


def angulo(qual, graus):
    pwms[qual].ChangeDutyCycle(duty(graus))
    sleep(0.5)


angulo("entrada", 0)       # cancela fechada
angulo("entrada", 90)      # cancela aberta
angulo("entrada", 0)
pwms["entrada"].ChangeDutyCycle(0)   # solta o servo: ele para de tremer

for pwm in pwms.values():
    pwm.stop()
GPIO.cleanup(list(PINOS.values()))
