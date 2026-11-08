from gpiozero import RGBLED, TonalBuzzer
from gpiozero.tones import Tone
from time import sleep

led = RGBLED(red=4, green=17, blue=27, active_high=False)   # ânodo comum
buz = TonalBuzzer(6, octaves=2)

led.color = (0, 1, 0)                  # verde: vaga livre
sleep(1)

for nota in ("C5", "E5", "G5", "C6"):  # musiquinha de 4 notas
    buz.play(Tone(nota))
    sleep(0.2)
buz.stop()

led.off()
