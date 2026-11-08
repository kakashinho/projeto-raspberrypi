"""Desenhos SVG do guia da equipe.

O mapa da placa é gerado a partir de kicad_hat/gerador/design.py (mesmas coordenadas
de furo da placa de interface), então a posição de cada peça é a da placa de verdade.
"""
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "hardware", "gerador"))
import design as D

P = 24.0
MM = P / D.PITCH
BW, BH = 100 * MM, 50 * MM
MX, MY = 40.0, 46.0
X0MM = (100 - (D.NCOLS - 1) * D.PITCH) / 2
Y0MM = (50 - (D.NROWS - 1) * D.PITCH) / 2
VB_W, VB_H = BW + 2 * MX, BH + 2 * MY

def X(c):
    return MX + (X0MM + (c - 1) * D.PITCH) * MM

def Y(r):
    return MY + (Y0MM + (r - 1) * D.PITCH) * MM

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

TAREFAS = {
    1: "Cancelas",
    2: "Presença",
    3: "Guarita manual",
    4: "Sinalização",
    5: "Ambiente",
    6: "Lógica",
    7: "Backend",
    8: "Frontend",
}

PECAS = [
    ("J7", 0, ("r", 0.9, 0.25, 5.1, 4.0), ("J7 fonte 5 V externa", 3.0, 4.55, "middle")),
    ("JP1", 0, ("r", 10.55, 1.55, 13.45, 2.45), ("JP1 jumper do 5 V", 12.0, 1.2, "middle")),
    ("C2", 0, ("c", 15.0, 13.0, 2.0), ("C2 470 µF", 15.0, 13.1, "middle")),
    ("RV1", 3, ("r", 1.5, 9.7, 6.5, 12.6), ("RV1 pot 10 kΩ", 4.0, 11.5, "middle")),
    ("C1", 3, ("r", 0.6, 8.6, 3.4, 9.4), ("C1", 2.0, 9.12, "middle")),
    ("R2", 3, ("r", 3.6, 5.6, 4.4, 9.4), ("R2", 4.0, 7.6, "middle")),
    ("R1", 3, ("r", 5.6, 5.6, 6.4, 9.4), ("R1", 6.0, 7.6, "middle")),
    ("R4", 2, ("r", 6.6, 8.6, 7.4, 12.4), ("R4", 7.0, 10.6, "middle")),
    ("R3", 2, ("r", 8.6, 8.6, 9.4, 12.4), ("R3", 9.0, 10.6, "middle")),
    ("J4", 2, ("r", 10.6, 9.6, 11.4, 13.4), ("J4 HC-SR04", 11.0, 9.0, "middle")),
    ("R5", 4, ("r", 14.55, 4.55, 19.45, 5.45), ("R5", 17.0, 5.1, "middle")),
    ("D1", 4, ("c", 19.5, 6.95, 1.35), ("D1 LED RGB", 19.5, 8.75, "middle")),
    ("J5", 5, ("r", 23.6, 5.6, 24.4, 8.4), ("J5 DHT11", 24.0, 5.2, "middle")),
    ("SW1", 3, ("r", 24.75, 5.7, 28.25, 8.3), ("SW1", 26.5, 7.12, "middle")),
    ("J8", 3, ("r", 26.55, 4.55, 28.45, 5.45), ("J8", 27.5, 5.1, "middle")),
    ("R6", 4, ("r", 25.55, 9.55, 30.45, 10.45), ("R6", 28.0, 10.1, "middle")),
    ("Q1", 4, ("r", 24.55, 11.45, 27.45, 12.55), ("Q1", 26.0, 11.05, "middle")),
    ("J6", 4, ("r", 21.55, 11.55, 24.45, 12.45), ("J6 buzzer", 23.0, 11.05, "middle")),
    ("J2", 1, ("r", 30.55, 11.55, 31.45, 14.45), ("J2", 31.0, 11.1, "middle")),
    ("J3", 1, ("r", 32.55, 11.55, 33.45, 14.45), ("J3", 33.0, 11.1, "middle")),
]

LEGENDA = {
    "J2": ({"3": "S", "2": "+", "1": "−"}, "esq"),
    "J3": ({"3": "S", "2": "+", "1": "−"}, "esq"),
    "J4": ({"1": "VCC", "2": "TRIG", "3": "ECHO", "4": "GND"}, "esq"),
    "J5": ({"1": "3V3", "2": "DAT", "3": "GND"}, "esq"),
    "J6": ({"1": "5V", "2": "nc", "3": "Q1"}, "baixo"),
    "JP1": ({"1": "RPi", "2": "5V", "3": "EXT"}, "baixo"),
    "D1": ({"1": "R", "2": "+", "3": "G", "4": "B"}, "baixo"),
    "J7": ({"1": "+5V", "2": "GND"}, "baixo"),
    "RV1": ({"1": "1", "2": "2", "3": "3"}, "cima"),
    "Q1": ({"1": "C", "2": "B", "3": "E"}, "baixo"),
    "J8": ({"1": "G5", "2": "GND"}, "baixo"),
}

CRACHAS = [(1, 32.0, 10.55), (2, 11.0, 8.35), (3, 4.0, 13.45), (3, 29.45, 6.95),
           (4, 21.75, 6.95), (4, 20.35, 12.0), (5, 24.0, 9.0)]

PINO_TAREFA = {7: (4, "LED R", 4), 11: (17, "LED G", 4), 13: (27, "LED B", 4), 15: (22, "DHT11", 5),
               16: (23, "TRIG", 2), 18: (24, "ECHO", 2), 22: (25, "Pot lê", 3), 32: (12, "Pot carga", 3),
               29: (5, "Botão", 3), 31: (6, "Buzzer", 4), 33: (13, "Servo 1", 1), 37: (26, "Servo 2", 1)}

def _forma(f, cls):
    if f[0] == "r":
        _, c1, r1, c2, r2 = f
        return (f'<rect class="{cls}" x="{X(c1):.1f}" y="{Y(r1):.1f}" width="{X(c2) - X(c1):.1f}" '
                f'height="{Y(r2) - Y(r1):.1f}" rx="4"/>')
    _, cx, cy, rr = f
    return f'<circle class="{cls}" cx="{X(cx):.1f}" cy="{Y(cy):.1f}" r="{rr * P:.1f}"/>'

def placa_defs():
    """<g id="placa"> com a placa inteira. Cada grupo tem opacity:var(--oN,1) para poder esmaecer."""
    o = []
    o.append(f'<rect class="pcb" x="{MX}" y="{MY}" width="{BW:.1f}" height="{BH:.1f}" rx="7"/>')
    for c, r in ((0, 0), (35, 0), (0, 16), (35, 16)):
        o.append(f'<circle class="furo-fix" cx="{X(c):.1f}" cy="{Y(r):.1f}" r="6"/>')
    for r in range(1, D.NROWS + 1):
        for c in range(1, D.NCOLS + 1):
            o.append(f'<circle class="furo" cx="{X(c):.1f}" cy="{Y(r):.1f}" r="2.3"/>')
    for c in range(1, D.NCOLS + 1):
        o.append(f'<text class="num" x="{X(c):.1f}" y="{Y(1) - 17:.1f}" text-anchor="middle">{c}</text>')
        o.append(f'<text class="num" x="{X(c):.1f}" y="{Y(15) + 24:.1f}" text-anchor="middle">{c}</text>')
    for r in range(1, D.NROWS + 1):
        o.append(f'<text class="num" x="{X(1) - 20:.1f}" y="{Y(r) + 3:.1f}" text-anchor="middle">{D.ROWS[r - 1]}</text>')
        o.append(f'<text class="num" x="{X(34) + 20:.1f}" y="{Y(r) + 3:.1f}" text-anchor="middle">{D.ROWS[r - 1]}</text>')

    o.append(f'<g style="opacity:var(--o0,1)">')
    o.append(f'<rect class="j1" x="{X(14.5):.1f}" y="{Y(1.5):.1f}" width="{X(34.5) - X(14.5):.1f}" '
             f'height="{Y(3.5) - Y(1.5):.1f}" rx="3"/>')
    o.append(f'<text class="rot-j1" x="{(X(14.5) + X(34.5)) / 2:.1f}" y="{MY + 20:.1f}" text-anchor="middle">'
             f'J1 · encaixe do Raspberry (a barra fica por baixo da placa)</text>')
    usados_j1 = []
    for n in range(1, 41):
        h = D.pi_hole(n)
        c, r = D.rc(h)
        cx, cy = X(c), Y(r)
        ty = Y(1) + 3 if n % 2 == 0 else Y(4) + 3
        if n in PINO_TAREFA:
            bcm, _, t = PINO_TAREFA[n]
            usados_j1.append(f'<circle class="k{t} pad-j1" style="opacity:var(--o{t},1)" cx="{cx:.1f}" cy="{cy:.1f}" r="6.2"/>')
            usados_j1.append(f'<text class="pino-usado k{t}" style="opacity:var(--o{t},1)" x="{cx:.1f}" y="{ty:.1f}" text-anchor="middle">{bcm}</text>')
        elif n in D.PI_POWER:
            nome = D.PI_POWER[n]
            cls = {"5V": "p5", "3V3": "p3", "GND": "pg"}[nome]
            o.append(f'<rect class="{cls}" x="{cx - 5.5:.1f}" y="{cy - 5.5:.1f}" width="11" height="11" rx="2"/>')
            o.append(f'<text class="pino-pot" x="{cx:.1f}" y="{ty:.1f}" text-anchor="middle">{nome}</text>')
        else:
            o.append(f'<circle class="pino-livre" cx="{cx:.1f}" cy="{cy:.1f}" r="4"/>')
    o.append('</g>')
    o.extend(usados_j1)

    por_tarefa = {}
    for ref, t, forma, rot in PECAS:
        por_tarefa.setdefault(t, []).append((ref, forma, rot))
    partes = {p["ref"]: p for p in D.PARTS}
    for t, lista in por_tarefa.items():
        o.append(f'<g class="k{t}" style="opacity:var(--o{t},1)">')
        for ref, forma, (txt, lc, lr, anc) in lista:
            o.append(_forma(forma, "peca"))
            p = partes.get(ref)
            if p:
                for num, (h, _net) in p["pads"].items():
                    c, r = D.rc(h)
                    o.append(f'<circle class="pad" cx="{X(c):.1f}" cy="{Y(r):.1f}" r="4.2"/>')
                leg = LEGENDA.get(ref)
                if leg:
                    textos, lado = leg
                    for num, tx in textos.items():
                        c, r = D.rc(p["pads"][num][0])
                        if lado == "esq":
                            o.append(f'<text class="pin" x="{X(c) - 9:.1f}" y="{Y(r) + 3:.1f}" text-anchor="end">{esc(tx)}</text>')
                        elif lado == "baixo":
                            o.append(f'<text class="pin" x="{X(c):.1f}" y="{Y(r) + 15:.1f}" text-anchor="middle">{esc(tx)}</text>')
                        else:
                            o.append(f'<text class="pin" x="{X(c):.1f}" y="{Y(r) - 8:.1f}" text-anchor="middle">{esc(tx)}</text>')
            o.append(f'<text class="rot" x="{X(lc):.1f}" y="{Y(lr) + 3:.1f}" text-anchor="{anc}">{esc(txt)}</text>')
        o.append('</g>')

    for t, c, r in CRACHAS:
        o.append(f'<g class="k{t} cracha-g" style="opacity:var(--o{t},1)"><circle class="cracha" cx="{X(c):.1f}" cy="{Y(r):.1f}" r="10"/>'
                 f'<text class="cracha-n" x="{X(c):.1f}" y="{Y(r) + 4:.1f}" text-anchor="middle">{t}</text></g>')
    return f'<g id="mapa-placa">{"".join(o)}</g>'

def placa_svg(rotulo="Mapa da placa de interface, vista de cima, com a área de cada tarefa colorida", foco=None, crop=None,
              classe="placa", sem_extras=False):
    """SVG visível que referencia #placa. foco: tarefa (esmaece as demais). crop: (c1,r1,c2,r2) em coordenadas de furo."""
    over = ""
    estilo_partes = []
    if crop:
        c1, r1, c2, r2 = crop
        x1, y1, x2, y2 = X(c1), Y(r1), X(c2), Y(r2)
        vb = f"{x1:.1f} {y1:.1f} {x2 - x1:.1f} {y2 - y1:.1f}"
        t = []
        for c in range(max(1, math.ceil(c1)), min(D.NCOLS, math.floor(c2)) + 1):
            if X(c) - x1 < 22:
                continue
            t.append(f'<text class="coord" x="{X(c):.1f}" y="{y1 + 10.5:.1f}" text-anchor="middle">{c}</text>')
        for r in range(max(1, math.ceil(r1)), min(D.NROWS, math.floor(r2)) + 1):
            if Y(r) - y1 < 20:
                continue
            t.append(f'<text class="coord" x="{x1 + 9.5:.1f}" y="{Y(r) + 3.5:.1f}" text-anchor="middle">{D.ROWS[r - 1]}</text>')
        if not sem_extras:
            faixas = (f'<rect class="coord-faixa" x="{x1:.1f}" y="{y1:.1f}" width="{x2 - x1:.1f}" height="14"/>'
                      f'<rect class="coord-faixa" x="{x1:.1f}" y="{y1:.1f}" width="19" height="{y2 - y1:.1f}"/>')
            over = faixas + "".join(t)
            estilo_partes.append("--cracha:none")
    else:
        vb = f"0 22 {VB_W:.1f} {VB_H - 44:.1f}"
    if foco:
        ids = foco if isinstance(foco, (list, tuple)) else [foco]
        estilo_partes += [f"--o{i}:{1 if i in ids else .1}" for i in range(1, 6)]
        estilo_partes.append("--o0:.5")
    estilo = f' style="{";".join(estilo_partes)}"' if estilo_partes else ""
    return (f'<svg class="{classe}" viewBox="{vb}" role="img" aria-label="{esc(rotulo)}"{estilo}>'
            f'<use href="#mapa-placa"/>{over}</svg>')

def pinos_svg(cols=None):
    dx = 49
    x0 = 78
    W = x0 + 19 * dx + 60
    H = 208
    ytop, ybot = 84, 144
    if cols:
        xs = 0 if cols[0] == 0 else x0 + cols[0] * dx - 30
        xe = W if cols[1] == 19 else x0 + cols[1] * dx + 30
    else:
        xs, xe = 0, W
    o = [f'<svg class="pinos" viewBox="{xs} 0 {xe - xs} {H}" role="img" '
         f'aria-label="Os 40 pinos do Raspberry Pi vistos de cima, com os pinos usados coloridos pela tarefa dona">']
    o.append(f'<rect class="j1" x="{x0 - 28}" y="{ytop - 20}" width="{19 * dx + 56}" height="{ybot - ytop + 40}" rx="8"/>')
    o.append(f'<text class="rot" x="8" y="{ybot + 4}" text-anchor="start">pino 1</text>')
    o.append(f'<text class="rot" x="8" y="{ytop + 4}" text-anchor="start">pino 2</text>')
    for n in range(1, 41):
        col = (n - 1) // 2
        cx = x0 + col * dx
        cy = ytop if n % 2 == 0 else ybot
        up = n % 2 == 0
        if n in PINO_TAREFA:
            bcm, nome, t = PINO_TAREFA[n]
            o.append(f'<circle class="k{t} pad-g" cx="{cx}" cy="{cy}" r="15"/>')
            o.append(f'<text class="n-pino-on" x="{cx}" y="{cy + 4}" text-anchor="middle">{n}</text>')
            ya, yb = (cy - 26, cy - 41) if up else (cy + 35, cy + 50)
            o.append(f'<text class="gpio k{t}" x="{cx}" y="{ya}" text-anchor="middle">GPIO{bcm}</text>')
            o.append(f'<text class="func k{t}" x="{cx}" y="{yb}" text-anchor="middle">{nome}</text>')
        elif n in D.PI_POWER:
            nome = D.PI_POWER[n]
            cls = {"5V": "p5", "3V3": "p3", "GND": "pg"}[nome]
            o.append(f'<rect class="{cls}" x="{cx - 14}" y="{cy - 14}" width="28" height="28" rx="5"/>')
            o.append(f'<text class="n-pino-pot" x="{cx}" y="{cy + 4}" text-anchor="middle">{n}</text>')
            ya = cy - 26 if up else cy + 38
            o.append(f'<text class="func" x="{cx}" y="{ya}" text-anchor="middle">{nome}</text>')
        else:
            o.append(f'<circle class="pino-livre-g" cx="{cx}" cy="{cy}" r="14"/>')
            o.append(f'<text class="n-pino-off" x="{cx}" y="{cy + 4}" text-anchor="middle">{n}</text>')
            if n in D.PI_BCM:
                ya = cy - 26 if up else cy + 38
                o.append(f'<text class="gpio-off" x="{cx}" y="{ya}" text-anchor="middle">GPIO{D.PI_BCM[n]}</text>')
    o.append('</svg>')
    return "".join(o)

def _badge(t, x, y):
    return (f'<g class="k{t}"><circle class="cracha" cx="{x}" cy="{y}" r="11"/>'
            f'<text class="cracha-n" x="{x}" y="{y + 4}" text-anchor="middle">{t}</text></g>')

def _seta(x1, y1, x2, y2, rot=None, rx=None, ry=None):
    s = f'<line class="seta" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" marker-end="url(#ponta)"/>'
    if rot:
        s += f'<text class="rot-seta" x="{rx if rx is not None else (x1 + x2) / 2}" y="{ry if ry is not None else y1 - 6}" text-anchor="middle">{esc(rot)}</text>'
    return s

def sistema_svg():
    o = ['<svg class="sistema" viewBox="0 0 1000 470" role="img" aria-label="Fluxo do sistema: sensores e atuadores na placa, '
         'módulos Python, lógica main.py, servidor Node com SQLite e navegador. Cada bloco leva à sua tarefa">']
    o.append('<defs><marker id="ponta" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
             '<path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs>')
    heads = [(104, "NA PLACA"), (323, "PYTHON: UM ARQUIVO POR PEÇA"), (502, "LÓGICA"), (742, "SERVIDOR NO PI"), (939, "NAVEGADOR")]
    for x, t in heads:
        o.append(f'<text class="cab" x="{x}" y="22" text-anchor="middle">{t}</text>')
    linhas = [
        (1, "2 servomotores", "cancela de entrada e de saída", "cancelas.py", "out"),
        (2, "Sensor ultrassônico", "distância até o carro", "presenca.py", "in"),
        (3, "Potenciômetro e botão", "controle manual da guarita", "manual.py", "in"),
        (4, "LED RGB e buzzer", "cor e música", "sinais.py", "out"),
        (5, "Sensor DHT11", "temperatura e umidade", "ambiente.py", "in"),
    ]
    for i, (t, nome, sub, arq, sent) in enumerate(linhas):
        y = 44 + i * 78
        cy = y + 29
        o.append(f'<a class="blk" href="#tarefa-{t}"><title>Abrir a tarefa {t}</title>')
        o.append(f'<g class="k{t}"><rect class="caixa" x="14" y="{y}" width="180" height="58" rx="8"/></g>')
        o.append(f'<text class="tit" x="28" y="{y + 24}">{esc(nome)}</text><text class="sub" x="28" y="{y + 42}">{esc(sub)}</text>')
        o.append(_badge(t, 14, y))
        o.append(f'<g class="k{t}"><rect class="caixa mod" x="238" y="{y}" width="170" height="58" rx="8"/></g>')
        o.append(f'<text class="mono" x="323" y="{cy + 5}" text-anchor="middle">{arq}</text>')
        o.append(_badge(t, 238, y))
        o.append('</a>')
        if sent == "in":
            o.append(_seta(194, cy, 238, cy))
            o.append(_seta(408, cy, 452, cy))
        else:
            o.append(_seta(238, cy, 194, cy))
            o.append(_seta(452, cy, 408, cy))
    o.append('<a class="blk" href="#tarefa-6"><title>Abrir a tarefa 6</title>')
    o.append('<g class="k6"><rect class="caixa" x="452" y="44" width="100" height="370" rx="8"/></g>')
    o.append('<text class="mono" x="502" y="212" text-anchor="middle">main.py</text>')
    o.append('<text class="sub" x="502" y="232" text-anchor="middle">regras do</text>')
    o.append('<text class="sub" x="502" y="246" text-anchor="middle">estacionamento</text>')
    o.append(_badge(6, 452, 44))
    o.append('</a>')
    o.append('<a class="blk" href="#tarefa-7"><title>Abrir a tarefa 7</title>')
    o.append('<g class="k7"><rect class="caixa" x="672" y="110" width="140" height="120" rx="8"/></g>')
    o.append('<text class="tit" x="742" y="158" text-anchor="middle">Node.js</text>')
    o.append('<text class="sub" x="742" y="176" text-anchor="middle">Express, porta 3000</text>')
    o.append('<text class="sub" x="742" y="192" text-anchor="middle">/api/...</text>')
    o.append(_badge(7, 672, 110))
    o.append('<g class="k7"><path class="caixa" d="M682 296 v54 a60 14 0 0 0 120 0 v-54 a60 14 0 0 0 -120 0 z"/>'
             '<ellipse class="caixa" cx="742" cy="296" rx="60" ry="14"/></g>')
    o.append('<text class="tit" x="742" y="338" text-anchor="middle">SQLite</text>')
    o.append('<text class="sub" x="742" y="356" text-anchor="middle">estacionamento.db</text>')
    o.append('</a>')
    o.append(_seta(742, 230, 742, 282, "grava e lê", 790, 262))
    o.append(_seta(742, 282, 742, 230))
    o.append('<a class="blk" href="#tarefa-8"><title>Abrir a tarefa 8</title>')
    o.append('<g class="k8"><rect class="caixa" x="890" y="110" width="98" height="120" rx="8"/></g>')
    o.append('<text class="tit" x="939" y="160" text-anchor="middle">Página</text>')
    o.append('<text class="sub" x="939" y="178" text-anchor="middle">PC ou celular</text>')
    o.append('<text class="sub" x="939" y="194" text-anchor="middle">:3000</text>')
    o.append(_badge(8, 890, 110))
    o.append('</a>')
    o.append(_seta(552, 150, 672, 150, "eventos (POST)", 612, 142))
    o.append(_seta(672, 196, 552, 196, "comandos (GET)", 612, 214))
    o.append(_seta(812, 150, 890, 150, "dados (GET)", 851, 142))
    o.append(_seta(890, 196, 812, 196, "comandos", 851, 214))
    o.append('<text class="sub" x="500" y="456" text-anchor="middle">Seta para a direita: o dado sobe. Seta para a esquerda: o comando desce.</text>')
    o.append('</svg>')
    return "".join(o)

def estados_svg():
    o = ['<svg class="estados" viewBox="0 0 780 400" role="img" aria-label="Estados da entrada, da saída e as interrupções lotado e manual">']
    o.append('<defs><marker id="ponta2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
             '<path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs>')
    W = 128
    xs = (14, 222, 430, 638)

    def linha(y, rotulo, est, trans, yt=None):
        o.append(f'<text class="cab" x="14" y="{y - 24 if yt is None else yt}">{rotulo}</text>')
        for (nome, sub), x in zip(est, xs):
            o.append(f'<rect class="caixa-e" x="{x}" y="{y}" width="{W}" height="62" rx="9"/>')
            o.append(f'<text class="tit" x="{x + W / 2}" y="{y + 27}" text-anchor="middle">{nome}</text>')
            o.append(f'<text class="sub" x="{x + W / 2}" y="{y + 46}" text-anchor="middle">{sub}</text>')
        for k, t in enumerate(trans):
            a, b = xs[k] + W, xs[k + 1]
            o.append(f'<line class="seta" x1="{a}" y1="{y + 31}" x2="{b}" y2="{y + 31}" marker-end="url(#ponta2)"/>')
            o.append(f'<text class="rot-seta" x="{(a + b) / 2}" y="{y + 21}" text-anchor="middle">{t}</text>')

    linha(64, "ENTRADA: automática, pelo sensor",
          [("LIVRE", "LED verde"), ("ABRINDO", "amarelo + música"), ("PASSANDO", "cancela aberta"), ("FECHANDO", "2 s depois")],
          ["carro 1 s + vaga", "cancela aberta", "carro passou"], yt=14)
    o.append('<path class="seta" d="M702 64 V42 H78 V64" fill="none" marker-end="url(#ponta2)"/>')
    o.append('<text class="rot-seta" x="390" y="36" text-anchor="middle">fechou: POST /api/eventos {"tipo":"entrada"}</text>')

    o.append('<rect class="caixa-i" x="14" y="156" width="366" height="70" rx="9"/>')
    o.append('<text class="tit" x="30" y="180">LOTADO (dentro ≥ 6)</text>')
    o.append('<text class="sub" x="30" y="199">A entrada não abre. LED vermelho + 2 bips.</text>')
    o.append('<text class="sub" x="30" y="215">Volta a LIVRE quando sai um carro.</text>')
    o.append('<rect class="caixa-i" x="400" y="156" width="366" height="70" rx="9"/>')
    o.append('<text class="tit" x="416" y="180">MANUAL</text>')
    o.append('<text class="sub" x="416" y="199">Pot ou botão mexeu: a guarita manda no servo 1.</text>')
    o.append('<text class="sub" x="416" y="215">LED azul. Volta ao automático após 10 s parado.</text>')

    linha(290, "SAÍDA: o porteiro libera pelo painel",
          [("COMANDO", "clique em Liberar"), ("ABRINDO", "servo 2 abre"), ("ESPERA", "2 segundos"), ("FECHANDO", "servo 2 fecha")],
          ["main.py recebe", "aberta", "passaram 2 s"])
    o.append('<path class="seta" d="M702 352 V376 H78 V352" fill="none" marker-end="url(#ponta2)"/>')
    o.append('<text class="rot-seta" x="390" y="392" text-anchor="middle">fechou: POST /api/eventos {"tipo":"saida"}</text>')
    o.append('</svg>')
    return "".join(o)

def painel_svg():
    o = ['<svg class="painel" viewBox="0 0 640 380" role="img" aria-label="Esboço do painel web com quatro áreas numeradas: contadores, gráfico, ambiente e liberar saída">']
    o.append('<rect class="jan" x="4" y="4" width="632" height="372" rx="10"/>')
    o.append('<text class="tit" x="24" y="34">Estacionamento · semana atual</text>')
    o.append('<text class="sub" x="616" y="34" text-anchor="end">números de exemplo</text>')
    cards = [("Vagas disponíveis agora", "3", 24, 150), ("Entradas na semana", "42", 184, 124), ("Saídas na semana", "39", 318, 124)]
    for t, v, x, w in cards:
        o.append(f'<rect class="cartao" x="{x}" y="52" width="{w}" height="74" rx="8"/>')
        o.append(f'<text class="sub" x="{x + 12}" y="76">{t}</text>')
        o.append(f'<text class="grande" x="{x + 12}" y="112">{v}</text>')
    o.append('<rect class="cartao" x="452" y="52" width="164" height="74" rx="8"/>')
    o.append('<text class="sub" x="464" y="76">Ambiente</text>')
    o.append('<text class="grande" x="464" y="112">26 °C · 58 %</text>')
    o.append('<rect class="cartao" x="24" y="142" width="408" height="214" rx="8"/>')
    o.append('<text class="sub" x="38" y="164">Entradas e saídas por dia</text>')
    dias = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
    ent = [8, 7, 9, 6, 8, 3, 1]
    sai = [7, 7, 8, 6, 7, 3, 1]
    base, topo = 332, 178
    esc_h = (base - topo) / 10
    for g in (0, 5, 10):
        yy = base - g * esc_h
        o.append(f'<line class="grade" x1="52" y1="{yy}" x2="418" y2="{yy}"/>')
        o.append(f'<text class="sub" x="46" y="{yy + 3}" text-anchor="end">{g}</text>')
    for i, d in enumerate(dias):
        x = 64 + i * 52
        o.append(f'<rect class="b-ent" x="{x}" y="{base - ent[i] * esc_h:.1f}" width="17" height="{ent[i] * esc_h:.1f}" rx="2"/>')
        o.append(f'<rect class="b-sai" x="{x + 19}" y="{base - sai[i] * esc_h:.1f}" width="17" height="{sai[i] * esc_h:.1f}" rx="2"/>')
        o.append(f'<text class="sub" x="{x + 18}" y="{base + 14}" text-anchor="middle">{d}</text>')
    o.append('<rect class="b-ent" x="300" y="152" width="10" height="10" rx="2"/><text class="sub" x="314" y="161">entradas</text>')
    o.append('<rect class="b-sai" x="366" y="152" width="10" height="10" rx="2"/><text class="sub" x="380" y="161">saídas</text>')
    o.append('<rect class="cartao" x="446" y="142" width="170" height="214" rx="8"/>')
    o.append('<text class="sub" x="460" y="164">Guarita</text>')
    o.append('<rect class="botao" x="460" y="180" width="142" height="46" rx="7"/><text class="tit-b" x="531" y="209" text-anchor="middle">Liberar saída</text>')
    o.append('<text class="sub" x="460" y="256">Abre a cancela de saída,</text>')
    o.append('<text class="sub" x="460" y="274">espera 2 s, fecha e</text>')
    o.append('<text class="sub" x="460" y="292">conta uma saída.</text>')
    for n, (cx, cy) in enumerate([(20, 50), (22, 142), (448, 50), (444, 142)], 1):
        o.append(f'<g class="k8"><circle class="cracha" cx="{cx}" cy="{cy}" r="11"/><text class="cracha-n" x="{cx}" y="{cy + 4}" text-anchor="middle">{n}</text></g>')
    o.append('</svg>')
    return "".join(o)

def conexao_svg():
    o = ['<svg class="conexao" viewBox="0 0 760 120" role="img" aria-label="Seu PC e o Raspberry na mesma rede; o PC descobre o IP com ping e entra com ssh">']
    o.append('<defs><marker id="ponta3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
             '<path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs>')
    o.append('<rect class="caixa-e" x="10" y="26" width="170" height="68" rx="9"/>')
    o.append('<text class="tit" x="95" y="55" text-anchor="middle">Seu PC</text><text class="sub" x="95" y="74" text-anchor="middle">PowerShell</text>')
    o.append('<rect class="caixa-e" x="295" y="26" width="170" height="68" rx="9"/>')
    o.append('<text class="tit" x="380" y="55" text-anchor="middle">Roteador</text><text class="sub" x="380" y="74" text-anchor="middle">mesmo Wi-Fi ou cabo</text>')
    o.append('<rect class="caixa-e" x="580" y="26" width="170" height="68" rx="9"/>')
    o.append('<text class="tit" x="665" y="55" text-anchor="middle">Raspberry Pi</text><text class="sub" x="665" y="74" text-anchor="middle">nome: raspberrypi.local</text>')
    o.append('<line class="seta" x1="180" y1="48" x2="295" y2="48" marker-end="url(#ponta3)"/>')
    o.append('<line class="seta" x1="465" y1="48" x2="580" y2="48" marker-end="url(#ponta3)"/>')
    o.append('<text class="rot-seta" x="237" y="40" text-anchor="middle">1. ping</text>')
    o.append('<text class="rot-seta" x="522" y="40" text-anchor="middle">IP de hoje</text>')
    o.append('<line class="seta" x1="580" y1="74" x2="465" y2="74" marker-end="url(#ponta3)"/>')
    o.append('<line class="seta" x1="295" y1="74" x2="180" y2="74" marker-end="url(#ponta3)"/>')
    o.append('<text class="rot-seta" x="237" y="94" text-anchor="middle">2. ssh dsm@IP</text>')
    o.append('</svg>')
    return "".join(o)

def _svg(vb, rotulo, corpo):
    return f'<svg class="peca-img" viewBox="{vb}" role="img" aria-label="{esc(rotulo)}">{corpo}</svg>'

def peca_hcsr04():
    c = ['<rect x="20" y="10" width="220" height="108" rx="5" fill="#1d5088"/>']
    for cx in (66, 194):
        c.append(f'<circle cx="{cx}" cy="60" r="34" fill="#eef2f3"/><circle cx="{cx}" cy="60" r="28" fill="#1b1b1b"/>'
                 f'<circle cx="{cx}" cy="60" r="21" fill="#f4f6f6"/><circle cx="{cx}" cy="60" r="11" fill="#6a6f72"/>')
    c.append('<rect x="105" y="16" width="50" height="17" rx="8.5" fill="#c3c7c9" stroke="#8d9193"/>')
    c.append('<text x="130" y="60" fill="#fff" font-size="10" text-anchor="middle" class="mono-img">HC-SR04</text>')
    for i, (x, t) in enumerate(zip((91, 117, 143, 169), ("VCC", "TRIG", "ECHO", "GND"))):
        c.append(f'<rect x="{x - 5}" y="104" width="10" height="12" fill="#cfcdb0"/>')
        c.append(f'<line x1="{x}" y1="116" x2="{x}" y2="140" stroke="#8a8f93" stroke-width="3"/>')
        c.append(f'<text class="mono-img ink" x="{x}" y="158" font-size="10" text-anchor="middle">{t}</text>')
    return _svg("0 0 260 176", "Sensor ultrassônico HC-SR04 com os pinos VCC, TRIG, ECHO e GND", "".join(c))

def peca_servo():
    c = []
    c.append('<rect x="116" y="44" width="112" height="64" rx="3" fill="#2c62a8"/>')
    c.append('<rect x="100" y="66" width="144" height="14" rx="2" fill="#2c62a8"/>')
    c.append('<circle cx="108" cy="73" r="3.2" fill="#12386a"/><circle cx="236" cy="73" r="3.2" fill="#12386a"/>')
    c.append('<rect x="150" y="30" width="46" height="18" rx="3" fill="#2c62a8"/>')
    c.append('<circle cx="173" cy="26" r="12" fill="#f1f1f1" stroke="#b5b5b5"/>')
    c.append('<rect x="173" y="20" width="62" height="12" rx="6" fill="#f1f1f1" stroke="#b5b5b5"/>')
    c.append('<circle cx="173" cy="26" r="3" fill="#b5b5b5"/><circle cx="228" cy="26" r="2.4" fill="#b5b5b5"/>')
    c.append('<text x="172" y="98" fill="#cfe0f5" font-size="10" text-anchor="middle" class="mono-img">SERVO</text>')
    fios = [("#6b4226", 88, 112, "GND"), ("#d12b2b", 76, 128, "+5V"), ("#f2862b", 100, 144, "SINAL")]
    for cor, y0, y1, t in fios:
        c.append(f'<path d="M116 {y0} C 96 {y0}, 92 {y1}, 64 {y1}" fill="none" stroke="{cor}" stroke-width="5" stroke-linecap="round"/>')
        c.append(f'<rect x="46" y="{y1 - 6}" width="18" height="12" rx="2" fill="#222"/>')
        c.append(f'<text class="mono-img ink" x="40" y="{y1 + 4}" font-size="10" text-anchor="end">{t}</text>')
    return _svg("0 0 260 176", "Servomotor com três fios: marrom é GND, vermelho é 5 V e laranja é o sinal", "".join(c))

def peca_pot():
    c = []
    c.append('<rect x="114" y="8" width="32" height="46" rx="3" fill="#2a2a2a"/>')
    for x in range(118, 146, 5):
        c.append(f'<line x1="{x}" y1="10" x2="{x}" y2="52" stroke="#4a4a4a" stroke-width="1"/>')
    c.append('<rect x="98" y="54" width="64" height="9" rx="2" fill="#7b8084"/>')
    c.append('<rect x="68" y="63" width="124" height="50" rx="5" fill="#2f6ca3"/>')
    c.append('<text x="130" y="94" fill="#fff" font-size="15" font-weight="700" text-anchor="middle" class="mono-img">10K</text>')
    for x, t in ((96, "1"), (130, "2"), (164, "3")):
        c.append(f'<rect x="{x - 3}" y="113" width="6" height="30" fill="#b8bcc0"/>')
        c.append(f'<text class="mono-img ink" x="{x}" y="160" font-size="11" text-anchor="middle">{t}</text>')
    c.append('<text class="mono-img ink" x="130" y="173" font-size="9" text-anchor="middle">2 = cursor (o do meio)</text>')
    return _svg("0 0 260 176", "Potenciômetro de 10 quilo-ohms com três terminais; o do meio é o cursor", "".join(c))

def peca_botao():
    c = []
    c.append('<rect x="92" y="24" width="76" height="76" rx="8" fill="#2b2b2b"/>')
    c.append('<rect x="98" y="30" width="64" height="64" rx="6" fill="#3a3a3a"/>')
    c.append('<circle cx="130" cy="62" r="23" fill="#5a3d34" stroke="#7a5a4e" stroke-width="2"/>')
    for x, y in ((104, 36), (156, 36), (104, 88), (156, 88)):
        c.append(f'<circle cx="{x}" cy="{y}" r="3.5" fill="#8a8a8a"/>')
    pernas = [(80, 38, "livre", False), (168, 38, "GPIO5", True), (80, 78, "GND", True), (168, 78, "livre", False)]
    for x, y, t, usado in pernas:
        cor = "#e0a81c" if usado else "#b8bcc0"
        c.append(f'<rect x="{x}" y="{y}" width="12" height="8" fill="{cor}"/>')
    c.append('<text class="mono-img ink" x="188" y="46" font-size="10" text-anchor="start">GPIO5</text>')
    c.append('<text class="mono-img ink" x="74" y="86" font-size="10" text-anchor="end">GND</text>')
    c.append('<text class="mono-img ink" x="130" y="126" font-size="10" text-anchor="middle">use 2 pernas em diagonal</text>')
    return _svg("0 0 260 176", "Botão táctil de quatro pernas; ligamos GPIO5 e GND em pernas opostas", "".join(c))

def peca_led():
    c = []
    c.append('<path d="M98 76 V44 a32 32 0 0 1 64 0 V76 Z" fill="#f4f1f1" fill-opacity=".75" stroke="#a9a9b4" stroke-width="2"/>')
    c.append('<rect x="92" y="76" width="76" height="8" rx="2" fill="#e8dcdc" stroke="#a9a9b4"/>')
    c.append('<circle cx="116" cy="54" r="6" fill="#e0453d"/><circle cx="130" cy="46" r="6" fill="#3dae4f"/><circle cx="144" cy="54" r="6" fill="#3d6fe0"/>')
    legs = [(106, 130, "R"), (124, 152, "+"), (142, 130, "G"), (160, 130, "B")]
    for x, yf, t in legs:
        c.append(f'<line x1="{x}" y1="84" x2="{x}" y2="{yf}" stroke="#b9bcc0" stroke-width="3.5"/>')
    c.append('<text class="mono-img ink" x="106" y="146" font-size="12" text-anchor="middle">R</text>')
    c.append('<text class="mono-img ink" x="142" y="146" font-size="12" text-anchor="middle">G</text>')
    c.append('<text class="mono-img ink" x="160" y="146" font-size="12" text-anchor="middle">B</text>')
    c.append('<text class="mono-img ink" x="124" y="168" font-size="11" text-anchor="middle">+ comum (a mais comprida)</text>')
    return _svg("0 0 260 176", "LED RGB de ânodo comum: pernas R, mais (a mais comprida), G e B", "".join(c))

def peca_dht11():
    c = []
    c.append('<rect x="62" y="12" width="136" height="112" rx="5" fill="#1f6b52"/>')
    c.append('<rect x="88" y="22" width="84" height="74" rx="4" fill="#3b82c8"/>')
    for i in range(6):
        c.append(f'<line x1="96" y1="{32 + i * 10}" x2="164" y2="{32 + i * 10}" stroke="#2a64a0" stroke-width="3" stroke-linecap="round"/>')
    c.append('<text x="130" y="112" fill="#e6f5ee" font-size="11" font-weight="700" text-anchor="middle" class="mono-img">DHT11</text>')
    for x, t in ((100, "3V3"), (130, "DAT"), (160, "GND")):
        c.append(f'<rect x="{x - 5}" y="116" width="10" height="14" fill="#222"/>')
        c.append(f'<line x1="{x}" y1="130" x2="{x}" y2="144" stroke="#b8bcc0" stroke-width="3"/>')
        c.append(f'<text class="mono-img ink" x="{x}" y="160" font-size="11" text-anchor="middle">{t}</text>')
    c.append('<text class="mono-img ink" x="130" y="173" font-size="9" text-anchor="middle">ordem da NOSSA placa (confira o módulo)</text>')
    return _svg("0 0 260 176", "Módulo DHT11 de três pinos: 3V3, dados e GND", "".join(c))

def peca_buzzer():
    c = []
    c.append('<rect x="62" y="10" width="136" height="112" rx="5" fill="#1d5088"/>')
    c.append('<circle cx="130" cy="64" r="40" fill="#1b1b1b"/><circle cx="130" cy="64" r="33" fill="none" stroke="#3a3a3a" stroke-width="2"/>')
    c.append('<circle cx="130" cy="64" r="8" fill="#000"/>')
    c.append('<text x="96" y="40" fill="#fff" font-size="13" font-weight="700" class="mono-img">+</text>')
    for x, t in ((100, "5V"), (130, "nc"), (160, "Q1")):
        c.append(f'<rect x="{x - 5}" y="114" width="10" height="14" fill="#222"/>')
        c.append(f'<line x1="{x}" y1="128" x2="{x}" y2="142" stroke="#b8bcc0" stroke-width="3"/>')
        c.append(f'<text class="mono-img ink" x="{x}" y="158" font-size="11" text-anchor="middle">{t}</text>')
    c.append('<text class="mono-img ink" x="130" y="173" font-size="9" text-anchor="middle">pinos da NOSSA placa (J6)</text>')
    return _svg("0 0 260 176", "Módulo de buzzer com três pinos: 5 V, sem ligação e coletor do transistor", "".join(c))

PECAS_IMG = {
    "hcsr04": peca_hcsr04, "servo": peca_servo, "pot": peca_pot, "botao": peca_botao,
    "led": peca_led, "dht11": peca_dht11, "buzzer": peca_buzzer,
}
