# main.py (esqueleto: você completa os TODO)
import time
import requests

import cancelas, presenca, sinais   # no começo use versões "falsas" (só print)

API = "http://localhost:3000/api"
TEMPO_FECHAR = 2      # segundos até a cancela fechar


def resumo():
    return requests.get(f"{API}/resumo", timeout=2).json()    # {"dentro": 3, "vagas": 6, ...}


def registrar(tipo):
    requests.post(f"{API}/eventos", json={"tipo": tipo}, timeout=2)


def liberar_entrada():
    # TODO 1: LED amarelo, música "abrindo" e abrir a cancela de entrada
    # TODO 2: esperar o carro passar (presenca.carro_presente() volta a False)
    # TODO 3: esperar TEMPO_FECHAR, fechar a cancela e registrar("entrada")
    pass


def liberar_saida():
    # TODO 4: abrir a cancela de saída, esperar TEMPO_FECHAR, fechar e registrar("saida")
    pass


while True:
    # TODO 5: o painel pediu "abrir saída"? Chame liberar_saida().
    #         Dica: GET /api/comandos/proximo devolve 204 quando não há comando.
    # TODO 6: há um carro na entrada (presenca.carro_presente())?
    #           se dentro >= vagas: LED vermelho, música "lotado" e NÃO abra
    #           senão: liberar_entrada()
    # TODO 7 (depois): modo manual (manual.py) e leitura do DHT11 a cada 30 s
    #         O manual tem prioridade: enquanto ele estiver ativo, ignore o sensor.
    #         Só o main.py move as cancelas (cancelas.angulo), nunca o manual.py.
    time.sleep(0.2)
