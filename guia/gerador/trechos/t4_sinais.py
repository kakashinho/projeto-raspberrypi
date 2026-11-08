import RPi.GPIO as GPIO
from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
from time import sleep

# Mesma base do sinais.py do sistema final
PINOS_LED = [4, 17, 27]              # R, G, B
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PINOS_LED, GPIO.OUT, initial=GPIO.HIGH)
pwms = [GPIO.PWM(p, 1000) for p in PINOS_LED]   # PWM de 1000 Hz
for pwm in pwms:
    pwm.start(100)

buz = TonalBuzzer(6, octaves=3)

def cor(r, g, b):
    # brilho de 0 a 100; ânodo comum: nível baixo acende, por isso 100 - brilho
    for pwm, brilho in zip(pwms, (r, g, b)):
        pwm.ChangeDutyCycle(100.0 - brilho)

cor(0, 100, 0)                       # verde: vaga livre
for nota in ("C5", "E5", "G5", "C6"):
    buz.play(Tone(nota))
    sleep(0.2)
    buz.stop()
    sleep(0.03)

cor(0, 0, 0)                         # apagado
for pwm in pwms:
    pwm.stop()
GPIO.cleanup(PINOS_LED)
buz.close()
