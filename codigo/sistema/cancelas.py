import RPi.GPIO as GPIO
from time import sleep

PINOS = {
    "entrada": 13,
    "saida": 26
}

FREQUENCIA_PWM = 50

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

_pwms = {}
for nome, pino in PINOS.items():
    GPIO.setup(pino, GPIO.OUT)
    _pwms[nome] = GPIO.PWM(pino, FREQUENCIA_PWM)
    _pwms[nome].start(0)

_limites = {
    "entrada": {"fechado": 0, "aberto": 90},
    # montagem espelhada: aberta em 0°, fechada em 90°
    "saida": {"fechado": 90, "aberto": 0}
}

_angulo_atual = {
    "entrada": 0,
    "saida": 0
}

def _angulo_para_duty(graus):
    """Converte o ângulo (0 a 180°) para o Duty Cycle correspondente (0.5ms a 2.5ms em 50Hz)."""
    pulso_ms = 0.5 + (graus / 180.0) * (2.5 - 0.5)
    duty = (pulso_ms / 20.0) * 100.0
    return duty

def angulo(qual, graus):
    """Move o servo suavemente para o ângulo pedido (de 0 a 180) de 5 em 5 graus."""
    if qual not in PINOS:
        raise ValueError("Cancela inválida! Use 'entrada' ou 'saida'.")
    
    global _angulo_atual
    atual = int(_angulo_atual[qual])
    graus = int(max(0, min(180, graus)))
    
    passo = 5 if graus > atual else -5
    
    if atual == graus:
        _pwms[qual].ChangeDutyCycle(_angulo_para_duty(graus))
        sleep(0.05)
        return

    for ang in range(atual, graus + passo, passo):
        if (passo > 0 and ang > graus) or (passo < 0 and ang < graus):
            ang = graus
        
        _pwms[qual].ChangeDutyCycle(_angulo_para_duty(ang))
        sleep(0.02)
    
    _angulo_atual[qual] = graus

def posicao_para_angulo(qual, pos):
    """Converte a posição do potenciômetro (0 = fechada, 100 = aberta) no ângulo da cancela.

    Usa os limites de cada cancela, então funciona também com servo montado ao contrário.
    """
    fechado = _limites[qual]["fechado"]
    aberto = _limites[qual]["aberto"]
    return round(fechado + (aberto - fechado) * max(0, min(100, pos)) / 100.0)

def abrir(qual):
    """Põe a cancela na posição aberta usando o limite configurado."""
    angulo(qual, _limites[qual]["aberto"])

def fechar(qual):
    """Põe a cancela na posição fechada usando o limite configurado."""
    angulo(qual, _limites[qual]["fechado"])

def soltar(qual=None):
    """Para o sinal PWM do servo (ou dos dois) para pararem de tremer.

    Use depois que a cancela já chegou onde devia. Antes de mover de novo,
    angulo() religa o sinal sozinho.
    """
    alvos = _pwms.values() if qual is None else [_pwms[qual]]
    for pwm in alvos:
        pwm.ChangeDutyCycle(0)

def encerrar():
    """Para os PWM e libera SÓ os pinos dos servos (nunca um cleanup geral)."""
    for pwm in _pwms.values():
        pwm.stop()
    GPIO.cleanup(list(PINOS.values()))
