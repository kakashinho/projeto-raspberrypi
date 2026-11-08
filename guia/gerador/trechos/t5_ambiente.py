"""Lê o DHT11 no GPIO22. Devolve (temperatura, umidade) ou None."""

import time

import gpiod
from gpiod.line import Bias, Direction, Edge, Value

try:
    from pinos import DHT11
except ImportError:
    DHT11 = 22

TENTATIVAS = 5
PAUSA_ENTRE_TENTATIVAS_S = 1.2
LIMIAR_BIT_US = 50.0

def _abrir_chip():
    """Acha o chip de GPIO do Raspberry (o nome muda entre modelos)."""
    for caminho in ("/dev/gpiochip0", "/dev/gpiochip4"):
        try:
            chip = gpiod.Chip(caminho)
        except OSError:
            continue
        if "bcm2835" in chip.get_info().label or "rp1" in chip.get_info().label:
            return chip
        chip.close()
    raise RuntimeError("Chip de GPIO do Raspberry não encontrado")

def _uma_leitura():
    """Faz uma tentativa. Devolve (temperatura, umidade) ou levanta RuntimeError."""
    chip = _abrir_chip()
    try:
        pedido = chip.request_lines(
            consumer="dht11",
            config={DHT11: gpiod.LineSettings(
                direction=Direction.OUTPUT, output_value=Value.INACTIVE)},
            event_buffer_size=256,
        )
    finally:
        chip.close()

    try:
        entrada = {DHT11: gpiod.LineSettings(
            direction=Direction.INPUT, bias=Bias.PULL_UP,
            edge_detection=Edge.BOTH)}
        reconfigurar = pedido.reconfigure_lines
        time.sleep(0.020)
        reconfigurar(entrada)
        eventos = []
        limite = time.monotonic() + 0.25
        while time.monotonic() < limite and len(eventos) < 90:
            if pedido.wait_edge_events(timeout=0.02):
                eventos.extend(pedido.read_edge_events())
    finally:
        pedido.release()

    larguras = []
    subida = None
    for ev in eventos:
        if ev.event_type == ev.Type.RISING_EDGE:
            subida = ev.timestamp_ns
        elif subida is not None:
            larguras.append((ev.timestamp_ns - subida) / 1000.0)
            subida = None

    bits = [1 if w > LIMIAR_BIT_US else 0 for w in larguras[-40:]]

    # o primeiro bit pode se perder ao soltar a linha; ele é sempre 0 na umidade
    faltam = 40 - len(bits)
    if faltam > 2:
        raise RuntimeError(f"resposta incompleta ({len(bits)} de 40 bits)")
    candidatos = [[0] + [(n >> i) & 1 for i in range(faltam - 1)]
                  for n in range(2 ** max(faltam - 1, 0))] if faltam else [[]]
    erro = None
    for prefixo in candidatos:
        try:
            return _decodificar(prefixo + bits)
        except RuntimeError as e:
            erro = e
    raise erro

def _decodificar(bits):
    """40 bits -> (temperatura, umidade). Levanta RuntimeError se algo não bater."""
    dados = []
    for i in range(5):
        byte = 0
        for b in bits[i * 8:(i + 1) * 8]:
            byte = (byte << 1) | b
        dados.append(byte)
    if (sum(dados[:4]) & 0xFF) != dados[4]:
        raise RuntimeError("soma de conferência não bateu")

    umidade = dados[0] + dados[1] / 10.0
    temperatura = dados[2] + (dados[3] & 0x7F) / 10.0
    if dados[3] & 0x80:
        temperatura = -temperatura
    if not (0 <= umidade <= 100 and -20 <= temperatura <= 60):
        raise RuntimeError(f"valor absurdo ({temperatura} °C, {umidade} %)")
    return temperatura, umidade

def ler():
    """Devolve (temperatura °C, umidade %) ou None se todas as tentativas falharem."""
    for tentativa in range(TENTATIVAS):
        try:
            return _uma_leitura()
        except (RuntimeError, OSError):
            if tentativa < TENTATIVAS - 1:
                time.sleep(PAUSA_ENTRE_TENTATIVAS_S)
    return None

if __name__ == "__main__":
    print(f"Lendo o DHT11 no GPIO{DHT11} (Ctrl+C para parar)...")
    try:
        while True:
            resultado = ler()
            if resultado is None:
                print("sem leitura (confira a ligação do DAT e os 3V3)")
            else:
                print(f"{resultado[0]:.1f} °C | {resultado[1]:.0f} %")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nTeste encerrado.")
