"""Testa UM componente por vez, para achar o que está falhando na placa.

Uso:  python3 teste_isolado.py NOME

  led          LED RGB: vermelho, verde, azul, amarelo, branco (1 s cada)
  buzzer       buzzer: música "abrindo", "lotado" e um bip
  servo_entrada  cancela da entrada: abre e fecha (0 -> 90 -> 0)
  servo_saida    cancela da saída: abre e fecha (0 -> 90 -> 0)
  botao        mostra SOLTOU/APERTOU ao vivo (Ctrl+C para sair)
  pot          mostra a posição do potenciômetro ao vivo (Ctrl+C para sair)
  distancia    mostra a distância ao vivo (Ctrl+C para sair)
  dht          lê o DHT11 cinco vezes

Cada teste libera os próprios pinos no fim. Não mexe nos outros componentes.
"""

import sys
import time

TESTES = {}

def teste(nome):
    def registra(funcao):
        TESTES[nome] = funcao
        return funcao
    return registra

@teste("led")
def led():
    import sinais
    try:
        for cor in ("vermelho", "verde", "azul", "amarelo", "branco"):
            print("LED:", cor, flush=True)
            sinais.cor(cor)
            time.sleep(1)
    finally:
        sinais.cor("apagado")
        sinais.encerrar()

@teste("buzzer")
def buzzer():
    import sinais
    try:
        print("bip", flush=True)
        sinais.bip()
        time.sleep(0.5)
        print("música abrindo", flush=True)
        sinais.musica("abrindo")
        time.sleep(0.5)
        print("música lotado", flush=True)
        sinais.musica("lotado")
    finally:
        sinais.encerrar()

def _servo(qual):
    import cancelas
    try:
        print(f"{qual}: abrindo", flush=True)
        cancelas.abrir(qual)
        time.sleep(1)
        print(f"{qual}: fechando", flush=True)
        cancelas.fechar(qual)
        time.sleep(0.5)
        cancelas.soltar(qual)
        print(f"{qual}: pronto (PWM desligado)", flush=True)
    finally:
        cancelas.encerrar()

@teste("servo_entrada")
def servo_entrada():
    _servo("entrada")

@teste("servo_saida")
def servo_saida():
    _servo("saida")

@teste("botao")
def botao():
    import manual
    print("Aperte e solte o botão da guarita. Ctrl+C para sair.", flush=True)
    anterior = manual.botao_pressionado()
    try:
        while True:
            atual = manual.botao_pressionado()
            if atual and not anterior:
                print("APERTOU", flush=True)
            elif anterior and not atual:
                print("soltou", flush=True)
            anterior = atual
            time.sleep(0.03)
    except KeyboardInterrupt:
        pass
    finally:
        manual.encerrar()

@teste("pot")
def pot():
    import manual
    print("Gire o potenciômetro do mínimo ao máximo. Ctrl+C para sair.", flush=True)
    try:
        while True:
            print("posição:", manual.posicao_pot(), "/100", flush=True)
            time.sleep(0.3)
    except KeyboardInterrupt:
        pass
    finally:
        manual.encerrar()

@teste("distancia")
def distancia():
    import presenca
    print("Passe a mão na frente do sensor. Ctrl+C para sair.", flush=True)
    try:
        while True:
            print(f"{presenca.distancia_cm():6.1f} cm  carro={presenca.carro_presente()}", flush=True)
            time.sleep(0.3)
    except KeyboardInterrupt:
        pass
    finally:
        presenca.encerrar()

@teste("dht")
def dht():
    import ambiente
    for _ in range(5):
        print("DHT11:", ambiente.ler(), flush=True)
        time.sleep(2)

if __name__ == "__main__":
    nome = sys.argv[1] if len(sys.argv) == 2 else ""
    if nome not in TESTES:
        print(__doc__)
        raise SystemExit(2)
    try:
        TESTES[nome]()
    except KeyboardInterrupt:
        print("\ninterrompido")
