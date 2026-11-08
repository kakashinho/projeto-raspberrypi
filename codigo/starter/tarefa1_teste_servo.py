from gpiozero import AngularServo
from time import sleep


def novo_servo(gpio):
    # SG90: pulso de 0,5 a 2,5 ms cobre os 180 graus
    return AngularServo(gpio, min_angle=0, max_angle=180,
                        min_pulse_width=0.0005, max_pulse_width=0.0025)


entrada = novo_servo(13)   # J2
saida = novo_servo(26)     # J3

entrada.angle = 0          # cancela fechada
sleep(1)
entrada.angle = 90         # cancela aberta
sleep(1)
entrada.angle = 0
sleep(1)
entrada.detach()           # solta o servo: ele para de tremer
