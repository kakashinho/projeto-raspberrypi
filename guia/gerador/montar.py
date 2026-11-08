"""Monta guia_equipe/index.html a partir de pagina.html, dos desenhos e dos trechos de código.

Uso:  python montar.py
"""
import os
import re

import desenhos as d
import esquemas as e
import cobre as cb

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, "..", "index.html")

with open(os.path.join(AQUI, "pagina.html"), encoding="utf-8") as f:
    html = f.read()

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def codigo(m):
    arquivo, nome = m.group(1), m.group(2)
    with open(os.path.join(AQUI, "trechos", arquivo), encoding="utf-8") as f:
        txt = re.sub(r"\n{3,}", "\n\n", f.read().rstrip("\n"))
    return ('<div class="codigo"><div class="cod-cab"><span>' + esc(nome) + '</span>'
            '<button class="copiar" type="button">Copiar</button></div>'
            '<pre><code>' + esc(txt) + '</code></pre></div>')

legenda = "".join(
    f'<a class="k{n}" href="#tarefa-{n}"><span class="cr">{n}</span>{d.TAREFAS[n]}</a>' for n in range(1, 9)
)

zooms = {
    "ZOOM_1": (1, (28.3, 10.0, 34.9, 15.6), ""),
    "ZOOM_2": (2, (5.3, 7.9, 12.7, 14.0), ""),
    "ZOOM_3A": (3, (-0.6, 4.8, 7.7, 13.2), ""),
    "ZOOM_3B": (3, (23.3, 3.8, 30.5, 9.0), ""),
    "ZOOM_4A": (4, (13.4, 3.8, 22.2, 9.4), ""),
    "ZOOM_4B": (4, (20.4, 8.8, 30.8, 13.0), ""),
    "ZOOM_5": (5, (22.1, 4.1, 25.9, 9.3), "estreito"),
}

ligacoes = {
    1: ("Servos", [
        ("Servo 1 · sinal", "J2 · S", ("gpio", 13, 33)),
        ("Servo 2 · sinal", "J3 · S", ("gpio", 26, 37)),
        ("Servos · +", "J2 e J3 · +", ("5v",)),
        ("Servos · −", "J2 e J3 · −", ("gnd",)),
    ]),
    2: ("HC-SR04", [
        ("VCC", "J4 · VCC", ("5v",)),
        ("TRIG", "J4 · TRIG", ("gpio", 23, 16)),
        ("ECHO (5 V)", "J4 · ECHO + R3/R4", ("gpio", 24, 18)),
        ("GND", "J4 · GND", ("gnd",)),
    ]),
    3: ("Peça", [
        ("#", "Botão (SW1)"),
        ("SW1 · uma perna", "SW1 (ou J8)", ("gpio", 5, 29, "lê o botão")),
        ("SW1 · perna oposta", "SW1 (ou J8)", ("gnd",)),
        ("#", "Potenciômetro (RV1) e capacitor (C1)"),
        ("RV1 · cursor, ponta 3, C1", "R2 10 kΩ", ("gpio", 12, 32, "carrega")),
        ("RV1 · ponta 1", "R1 10 kΩ", ("gpio", 25, 22, "lê o tempo")),
        ("C1 · outro lado", "direto no GND", ("gnd",)),
    ]),
    4: ("Peça", [
        ("#", "LED RGB (D1)"),
        ("LED · R", "D1 · R", ("gpio", 4, 7)),
        ("LED · G", "D1 · G", ("gpio", 17, 11)),
        ("LED · B", "D1 · B", ("gpio", 27, 13)),
        ("LED · + comum", "R5 330 Ω → D1 +", ("3v3",)),
        ("#", "Buzzer (J6)"),
        ("Buzzer · +", "J6 · 5V", ("5v",)),
        ("Buzzer · −", "J6 · Q1 (transistor)", ("gpio", 6, 31, "liga o Q1")),
    ]),
    5: ("DHT11", [
        ("DHT11 · VCC", "J5 · 3V3", ("3v3",)),
        ("DHT11 · DATA", "J5 · DAT", ("gpio", 22, 15)),
        ("DHT11 · GND", "J5 · GND", ("gnd",)),
    ]),
}

subs = {
    "{{PLACA_DEFS}}": d.placa_defs(),
    "{{SVG_PLACA}}": d.placa_svg(classe="placa"),
    "{{SVG_PLACA_E}}": d.placa_svg(rotulo="Metade esquerda da placa", crop=(-2.4, -1.9, 17.9, 17.9), sem_extras=True, classe="placa"),
    "{{SVG_PLACA_D}}": d.placa_svg(rotulo="Metade direita da placa", crop=(16.1, -1.9, 36.4, 17.9), sem_extras=True, classe="placa"),
    "{{SVG_PINOS}}": d.pinos_svg(),
    "{{SVG_PINOS_E}}": d.pinos_svg(cols=(0, 9)),
    "{{SVG_PINOS_D}}": d.pinos_svg(cols=(10, 19)),
    "{{SVG_SISTEMA}}": d.sistema_svg(),
    "{{SVG_ESTADOS}}": d.estados_svg(),
    "{{SVG_PAINEL}}": d.painel_svg(),
    "{{LEGENDA_TAREFAS}}": legenda,
    "{{SVG_COBRE}}": cb.cobre_svg(),
    "{{LEGENDA_COBRE}}": cb.legenda_cobre(),
    "{{TABELA_BOM}}": cb.tabela_bom(),
    "{{TABELA_LIGACOES}}": cb.tabela_ligacoes(),
}
for nome, fn in d.PECAS_IMG.items():
    svg = fn()
    subs["{{PECA_" + nome + "}}"] = svg
    subs["{{MINI_" + nome + "}}"] = svg.replace('class="peca-img"', 'class="peca-img mini"')
for nome in ("logica", "banco", "web"):
    subs["{{ICONE_" + nome + "}}"] = e.icone(nome)
for nome in ("servo_pwm", "ultrassom", "divisor_echo", "rc_circuito", "rc_curva", "botao_pullup", "led_anodo", "buzzer_circuit",
             "notas", "dht_fluxo", "sequencia", "sequencia_saida", "banco", "matriz_pinos", "servo_malha"):
    subs["{{FIG_" + nome + "}}"] = getattr(e, nome)()
for chave, (foco, crop, extra) in zooms.items():
    svg = d.placa_svg(rotulo="Área da placa em destaque, com fileiras e colunas", classe="zoom" + (" " + extra if extra else ""), foco=foco, crop=crop)
    subs["{{" + chave + "}}"] = svg
for t, (titulo, linhas) in ligacoes.items():
    subs["{{LIG_" + str(t) + "}}"] = e.ligacao(linhas, t, titulo)

for k, v in subs.items():
    html = html.replace(k, v)
html = re.sub(r"\{\{CODE:([^|}]+)\|([^}]+)\}\}", codigo, html)

sobrou = re.findall(r"\{\{[^}]+\}\}", html)
if sobrou:
    raise SystemExit("Marcadores sem troca: " + ", ".join(sorted(set(sobrou))))

with open(SAIDA, "w", encoding="utf-8") as f:
    f.write(html)
print("ok:", os.path.abspath(SAIDA), f"{len(html) / 1024:.0f} KB")
