"""Decide quando abrir as cancelas e registra o movimento no servidor."""

import os
import signal
import threading
import time

import requests

import ambiente
import cancelas
import manual
import presenca
import sinais

API = os.environ.get("API_URL", "http://localhost:3000/api")

TEMPO_FECHAR = 2
INTERVALO_DHT = 30
INTERVALO_COMANDOS = 0.5
PERIODO_PRESENCA = 2.0
COOLDOWN_ENTRADA = 6.0
VALIDADE_RESUMO = 3
TEMPO_ASSENTAR = 0.4

modo_manual = False
_cor = None
_resumo = {"dentro": 0, "vagas": 6}
_resumo_em = 0.0
_eventos_pendentes = []
_pediu_alternar = False
_ultimo_alternar = 0.0
_ultimo_batimento = 0.0
_ultimo_angulo = None
_ultima_entrada = -1e9

def log(*partes):
    print(time.strftime("%H:%M:%S"), *partes, flush=True)

def _pedir(metodo, caminho, **kw):
    """Chama a API; devolve a resposta ou None se o servidor não respondeu."""
    try:
        return requests.request(metodo, f"{API}{caminho}", timeout=2, **kw)
    except requests.RequestException:
        return None

def resumo(forcar=False):
    """Contagem atual (dentro/vagas...). Se o servidor falhar, usa a última."""
    global _resumo, _resumo_em
    if forcar or time.monotonic() - _resumo_em > VALIDADE_RESUMO:
        r = _pedir("GET", "/resumo")
        if r is not None and r.ok:
            _resumo, _resumo_em = r.json(), time.monotonic()
    return _resumo

def lotado():
    d = resumo()
    return d["dentro"] >= d["vagas"]

def registrar(tipo):
    """Conta uma entrada/saída. Se o servidor estiver fora, guarda para depois."""
    r = _pedir("POST", "/eventos", json={"tipo": tipo})
    if r is None:
        _eventos_pendentes.append(tipo)
        log(f"servidor fora do ar: {tipo} guardada para enviar depois")
    elif r.status_code == 409:
        log(f"servidor recusou a {tipo} (ninguém dentro)")
    resumo(forcar=True)

def reenviar_pendentes():
    while _eventos_pendentes:
        r = _pedir("POST", "/eventos", json={"tipo": _eventos_pendentes[0]})
        if r is None:
            return
        _eventos_pendentes.pop(0)

def batimento():
    """Avisa o servidor que o main.py está ativo. Usado nas esperas longas."""
    global _ultimo_batimento
    if time.monotonic() - _ultimo_batimento > 3:
        _ultimo_batimento = time.monotonic()
        _pedir("POST", "/controlador/batimento")

def proximo_comando():
    """Devolve o comando do painel ou None (a API responde 204 quando não há)."""
    global _ultimo_batimento
    _ultimo_batimento = time.monotonic()
    r = _pedir("GET", "/comandos/proximo")
    if r is not None and r.status_code == 200:
        return r.json()
    return None

def mostrar(cor, motivo=""):
    global _cor
    if cor != _cor:
        log(f"LED: {_cor} -> {cor} ({motivo})")
        sinais.cor(cor)
        _cor = cor

def led_de_repouso():
    if modo_manual:
        mostrar("azul", "modo manual")
    else:
        d = resumo()
        lot = d["dentro"] >= d["vagas"]
        mostrar("vermelho" if lot else "verde",
                f"repouso: dentro={d['dentro']} de {d['vagas']}")

def _fechar(qual):
    cancelas.fechar(qual)
    time.sleep(TEMPO_ASSENTAR)
    cancelas.soltar(qual)

def liberar_entrada():
    global _ultima_entrada
    log("entrada: carro detectado, abrindo")
    mostrar("amarelo", "abrindo entrada")
    sinais.musica("abrindo")
    cancelas.abrir("entrada")
    while presenca.carro_presente():
        batimento()
        time.sleep(PERIODO_PRESENCA)
    time.sleep(TEMPO_FECHAR)
    _fechar("entrada")
    registrar("entrada")
    _ultima_entrada = time.monotonic()
    log("entrada registrada")

def liberar_saida():
    if resumo(forcar=True)["dentro"] <= 0:
        log("saída pedida, mas não há carros dentro: ignorada")
        return
    log("saída: abrindo")
    mostrar("amarelo", "abrindo saída")
    sinais.musica("abrindo")
    cancelas.abrir("saida")
    time.sleep(TEMPO_FECHAR)
    _fechar("saida")
    registrar("saida")
    log("saída registrada")

def _botao_apertado():
    """Roda em outra thread: só levanta a bandeira. Quem age é o laço principal."""
    global _pediu_alternar
    _pediu_alternar = True

def alternar_manual():
    global modo_manual, _ultimo_angulo
    modo_manual = not modo_manual
    _ultimo_angulo = None
    log("modo manual", "LIGADO (potenciômetro controla a SAÍDA)" if modo_manual else "desligado")
    sinais.bip()
    _fechar("entrada")
    if not modo_manual:
        _fechar("saida")
    led_de_repouso()

def passo_manual():
    """Segue o potenciômetro (0 = fechada, 100 = aberta) com a cancela da SAÍDA."""
    global _ultimo_angulo
    pos = manual.posicao_pot()
    if pos is None:
        return
    alvo = cancelas.posicao_para_angulo("saida", pos)
    if _ultimo_angulo is None or abs(alvo - _ultimo_angulo) >= 2:
        cancelas.angulo("saida", alvo)
        _ultimo_angulo = alvo

_dht_thread = None

def enviar_ambiente_em_segundo_plano():
    """Lê o DHT11 em outra thread, para as tentativas (até ~6 s) não travarem o laço."""
    global _dht_thread
    if _dht_thread is not None and _dht_thread.is_alive():
        return
    _dht_thread = threading.Thread(target=enviar_ambiente, daemon=True)
    _dht_thread.start()

def enviar_ambiente():
    leitura = ambiente.ler()
    if leitura is None:
        log("DHT11: sem leitura desta vez")
        return
    temperatura, umidade = leitura
    _pedir("POST", "/ambiente", json={"temperatura": temperatura, "umidade": umidade})
    log(f"DHT11: {temperatura:.1f} °C, {umidade:.0f} %")

def _sair(signum, frame):
    raise SystemExit(0)

def main():
    global _pediu_alternar, _ultimo_alternar
    signal.signal(signal.SIGTERM, _sair)
    manual.on_botao(_botao_apertado)

    log("iniciando: fechando as duas cancelas")
    _fechar("entrada")
    _fechar("saida")
    led_de_repouso()

    ultima_dht = time.monotonic() - INTERVALO_DHT + 5
    ultima_presenca = 0.0
    carro = False
    ultimo_comando = 0.0
    avisou_lotado = False
    log("pronto")

    while True:
        agora = time.monotonic()
        reenviar_pendentes()

        if _pediu_alternar:
            _pediu_alternar = False
            if agora - _ultimo_alternar > 0.5:
                _ultimo_alternar = agora
                alternar_manual()

        if agora - ultimo_comando >= INTERVALO_COMANDOS:
            ultimo_comando = agora
            comando = proximo_comando()
            if comando and comando.get("alvo") == "saida" and comando.get("acao") == "abrir":
                liberar_saida()
                led_de_repouso()

        if modo_manual:
            passo_manual()
        else:
            if agora - ultima_presenca >= PERIODO_PRESENCA:
                ultima_presenca = agora
                carro = presenca.carro_presente()
            if carro and agora - _ultima_entrada < COOLDOWN_ENTRADA:
                carro = False
            if carro and lotado():
                mostrar("vermelho", "lotado com carro na entrada")
                if not avisou_lotado:
                    avisou_lotado = True
                    log("lotado: entrada negada")
                    sinais.musica("lotado")
            elif carro:
                carro = False
                liberar_entrada()
                led_de_repouso()
            else:
                avisou_lotado = False
                led_de_repouso()
                if agora - ultima_dht >= INTERVALO_DHT:
                    ultima_dht = agora
                    enviar_ambiente_em_segundo_plano()

        time.sleep(0.05 if modo_manual else 0.2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        log("encerrando: soltando os pinos")
        for passo in (cancelas.soltar, sinais.encerrar, presenca.encerrar,
                      manual.encerrar, cancelas.encerrar):
            try:
                passo()
            except Exception as erro:
                log("aviso ao encerrar:", erro)
