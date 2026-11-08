"""LED RGB (RPi.GPIO, PWM de 1000 Hz) e buzzer passivo."""

from time import sleep

import RPi.GPIO as GPIO
from gpiozero import TonalBuzzer
from gpiozero.tones import Tone

try:
    from pinos import LED_R, LED_G, LED_B, BUZZER
except ImportError:
    LED_R, LED_G, LED_B, BUZZER = 4, 17, 27, 6

FREQUENCIA_LED = 1000

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
_PINOS_LED = [LED_R, LED_G, LED_B]
GPIO.setup(_PINOS_LED, GPIO.OUT, initial=GPIO.HIGH)
_pwms = [GPIO.PWM(p, FREQUENCIA_LED) for p in _PINOS_LED]
for _pwm in _pwms:
    _pwm.start(100)

BUZZER_PASSIVO = True
buz = TonalBuzzer(BUZZER, octaves=3)

CORES = {
    "verde":    (0.0, 100.0, 0.0),
    "amarelo":  (76.3, 100.0, 0.0),
    "vermelho": (100.0, 0.0, 0.0),
    "azul":     (0.0, 0.0, 100.0),
    "branco":   (80.0, 100.0, 100.0),
    "apagado":  (0.0, 0.0, 0.0),
}

MUSICAS = {
    "abrindo": [("C5", 0.12), ("E5", 0.12), ("G5", 0.12), ("C6", 0.25)],
    "lotado":  [("C4", 0.35), (None, 0.15), ("C4", 0.35)],
    "alerta":  [("A5", 0.15), ("E5", 0.15)] * 3,
}

def _aplicar(r, g, b):
    for pwm, brilho in zip(_pwms, (r, g, b)):
        # ânodo comum: nível baixo acende, por isso 100 - brilho
        pwm.ChangeDutyCycle(100.0 - max(0.0, min(100.0, brilho)))

def cor(nome):
    """Ascende a cor pelo nome: verde, amarelo, vermelho, azul, branco ou apagado."""
    nome = nome.lower()
    if nome not in CORES:
        raise ValueError(f"Cor desconhecida: {nome}. Use: {', '.join(CORES)}")
    _aplicar(*CORES[nome])

def _tocar(nota, duracao):
    if nota is None:
        buz.stop()
    else:
        buz.play(Tone(nota))
    sleep(duracao)
    buz.stop()
    sleep(0.03)

def musica(nome):
    """Toca 'abrindo', 'lotado' ou 'alerta'."""
    nome = nome.lower()
    if nome not in MUSICAS:
        raise ValueError(f"Musica desconhecida: {nome}. Use: {', '.join(MUSICAS)}")
    for nota, dur in MUSICAS[nome]:
        _tocar(nota, dur)

def bip():
    """Um bip curto."""
    _tocar("A5", 0.08)

def encerrar():
    """Apaga o LED, para o buzzer e libera SÓ os pinos do LED e do buzzer."""
    _aplicar(0, 0, 0)
    for pwm in _pwms:
        pwm.stop()
    GPIO.cleanup(_PINOS_LED)
    buz.stop()
    buz.close()

if __name__ == "__main__":
    try:
        for c in ("vermelho", "verde", "azul", "amarelo", "branco"):
            print("Cor:", c)
            cor(c)
            sleep(1)
        for m in ("abrindo", "lotado"):
            print("Musica:", m)
            musica(m)
    except KeyboardInterrupt:
        print("\nEncerrado pelo usuario.")
    finally:
        encerrar()
        print("Pinos liberados.")
