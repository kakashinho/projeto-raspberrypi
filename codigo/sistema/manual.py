"""Potenciômetro e botão da guarita. Quem move a cancela é o main.py."""

import json
import os
import statistics
import time

import RPi.GPIO as GPIO
from gpiozero import Button

try:
    from pinos import BOTAO, POT_CARGA, POT_LE
except ImportError:
    BOTAO, POT_CARGA, POT_LE = 5, 12, 25

ARQ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "calibracao_pot.json")

TIMEOUT = 0.5
NUM_LEITURAS = 3
TEMPO_DESCARGA = 0.02
ALPHA = 0.7
ZONA_MORTA = 0.5

_configurado = False
_botao = None
_valor_filtrado = None
_nivel_exibido = None

def _configurar():
    global _configurado, _botao
    if _configurado:
        return
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(POT_CARGA, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(POT_LE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    _botao = Button(BOTAO)
    _configurado = True

def _medir_uma_vez():
    """Mede o tempo de carga do capacitor, em milissegundos."""
    _configurar()
    GPIO.output(POT_CARGA, GPIO.LOW)
    time.sleep(TEMPO_DESCARGA)
    GPIO.output(POT_CARGA, GPIO.HIGH)
    inicio = time.perf_counter()
    try:
        while not GPIO.input(POT_LE):
            if time.perf_counter() - inicio > TIMEOUT:
                return None
        return (time.perf_counter() - inicio) * 1000.0
    finally:
        GPIO.output(POT_CARGA, GPIO.LOW)

def medir():
    """Faz várias medições e devolve a mediana, ou None se todas falharem."""
    leituras = []
    for _ in range(NUM_LEITURAS):
        valor = _medir_uma_vez()
        if valor is not None:
            leituras.append(valor)
    return statistics.median(leituras) if leituras else None

def calibrar():
    """Calibra os extremos do potenciômetro e grava-os junto deste módulo."""
    _configurar()
    input("Gire o potenciômetro para o MÍNIMO e pressione ENTER...")
    minimo = medir()
    if minimo is None:
        raise RuntimeError("Não foi possível medir o mínimo; confira as ligações.")

    input("Gire o potenciômetro para o MÁXIMO e pressione ENTER...")
    maximo = medir()
    if maximo is None:
        raise RuntimeError("Não foi possível medir o máximo; confira as ligações.")

    inferior, superior = sorted((minimo, maximo))
    if superior - inferior <= 0:
        raise RuntimeError("Intervalo de calibração inválido. Calibre novamente.")

    with open(ARQ, "w", encoding="utf-8") as arquivo:
        json.dump({"min": minimo, "max": maximo}, arquivo, indent=2)
        arquivo.write("\n")
    print("Calibração salva em", ARQ)

def posicao_pot():
    """Devolve a posição filtrada de 0 a 100, ou None se não puder ler."""
    global _valor_filtrado, _nivel_exibido
    _configurar()
    try:
        with open(ARQ, encoding="utf-8") as arquivo:
            calibracao = json.load(arquivo)
        minimo = float(calibracao["min"])
        maximo = float(calibracao["max"])
    except (OSError, ValueError, TypeError, KeyError):
        return None

    # min e max vêm da calibração: a direção entre os dois é a própria medida
    intervalo = maximo - minimo
    if abs(intervalo) < 1e-9:
        return None
    tempo = medir()
    if tempo is None:
        return None

    posicao = max(0.0, min(100.0, (tempo - minimo) / intervalo * 100.0))
    _valor_filtrado = (
        posicao if _valor_filtrado is None
        else ALPHA * posicao + (1.0 - ALPHA) * _valor_filtrado
    )
    _valor_filtrado = max(0.0, min(100.0, _valor_filtrado))

    if _nivel_exibido is None or abs(_valor_filtrado - _nivel_exibido) >= ZONA_MORTA:
        _nivel_exibido = round(_valor_filtrado)
    return int(max(0, min(100, _nivel_exibido)))

def botao_pressionado():
    """Retorna True enquanto o botão (ativo em nível baixo) está apertado."""
    _configurar()
    return _botao.is_pressed

def on_botao(funcao):
    """Registra uma função chamada a cada aperto do botão.

    O callback da GPIO roda em outra thread; use-o apenas para marcar uma
    flag. A lógica principal e o controle da cancela ficam no main.py.
    """
    if not callable(funcao):
        raise TypeError("funcao precisa ser chamável")
    _configurar()
    _botao.when_pressed = funcao

def encerrar():
    """Libera o botão e SÓ os pinos do potenciômetro."""
    global _configurado, _botao
    if _botao is not None:
        _botao.close()
        _botao = None
    if _configurado:
        GPIO.cleanup((POT_CARGA, POT_LE))
        _configurado = False

if __name__ == "__main__":
    try:
        calibrar()
    except KeyboardInterrupt:
        print("Calibração cancelada.")
    finally:
        encerrar()
