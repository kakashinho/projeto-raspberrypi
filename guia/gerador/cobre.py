"""Vista do lado do cobre (espelhada, como página de livro), a lista de materiais e as ligações da placa.

Tudo sai de kicad_hat/gerador/design.py, a mesma fonte do projeto da placa.
"""
import csv
import io

import desenhos as dz
from desenhos import D, X, Y, MM, MX, MY, VB_W, VB_H, esc

FIXAS = {"+5V": "#d64541", "+5V_RPI": "#f09a82", "+5V_EXT": "#9c2230", "GND": "#2b302d", "+3V3": "#e8892b"}
PALETA = ["#2f5fc4", "#0b7d71", "#7a5ad6", "#b0307f", "#3f7d14", "#c28f00", "#0e86c9", "#8a5a3a",
          "#d1498f", "#5a7d9a", "#9a4bd1", "#12a594", "#c4562a", "#4a8f2a"]

def cores_redes():
    c = dict(FIXAS)
    outras = sorted({n for n in D.TRACKS if n not in c} | {p for part in D.PARTS for (_, p) in part["pads"].values() if p and p not in c})
    for i, n in enumerate(outras):
        c[n] = PALETA[i % len(PALETA)]
    return c

def xm(c):
    return X(D.NCOLS + 1 - c)

def pt(h):
    c, r = D.rc(h)
    return xm(c), Y(r)

def cobre_svg():
    cor = cores_redes()
    o = [f'<rect class="pcb" x="{MX}" y="{MY}" width="{100 * MM:.1f}" height="{50 * MM:.1f}" rx="7"/>']
    for r in range(1, D.NROWS + 1):
        for c in range(1, D.NCOLS + 1):
            o.append(f'<circle class="furo" cx="{xm(c):.1f}" cy="{Y(r):.1f}" r="2.3"/>')
    for c in range(1, D.NCOLS + 1):
        for yy in (Y(1) - 17, Y(15) + 24):
            o.append(f'<text class="num" x="{xm(c):.1f}" y="{yy:.1f}" text-anchor="middle">{c}</text>')
    for r in range(1, D.NROWS + 1):
        for xx in (xm(34) - 20, xm(1) + 20):
            o.append(f'<text class="num" x="{xx:.1f}" y="{Y(r) + 3:.1f}" text-anchor="middle">{D.ROWS[r - 1]}</text>')
    x1, x2 = xm(34.5), xm(14.5)
    o.append(f'<rect class="j1" x="{min(x1, x2):.1f}" y="{Y(1.5):.1f}" width="{abs(x2 - x1):.1f}" height="{Y(3.5) - Y(1.5):.1f}" rx="3"/>')
    o.append(f'<text class="rot-j1" x="{(x1 + x2) / 2:.1f}" y="{MY + 20:.1f}" text-anchor="middle">J1 · corpo da barra 2×20 (por este lado)</text>')
    for net, paths in D.TRACKS.items():
        for pth in paths:
            pts = " ".join(f"{pt(h)[0]:.1f},{pt(h)[1]:.1f}" for h in pth)
            o.append(f'<polyline class="trilha" points="{pts}" style="stroke:{cor.get(net, "#666")}"/>')
    for ref, net, a, b, ymm in D.JUMPERS:
        (xa, ya), (xb, yb) = pt(a), pt(b)
        yy = MY + (ymm - D.BOARD_Y) * MM
        o.append(f'<polyline class="fio-enc" points="{xa:.1f},{ya:.1f} {xa:.1f},{yy:.1f} {xb:.1f},{yy:.1f} {xb:.1f},{yb:.1f}"/>')
        o.append(f'<text class="w-rot" x="{xa + 5:.1f}" y="{yy - 3:.1f}" text-anchor="start">{ref}</text>')
    for p in D.PARTS:
        for num, (h, net) in p["pads"].items():
            x, y = pt(h)
            cl = "solda" if p["ref"] != "J1" else "solda j1p"
            o.append(f'<circle class="{cl}" cx="{x:.1f}" cy="{y:.1f}" r="{5.2 if p["ref"] != "J1" else 4.4}"/>')
    for n, (bcm, nome, t) in dz.PINO_TAREFA.items():
        c, r = D.rc(D.pi_hole(n))
        yy = Y(1) + 3 if n % 2 == 0 else Y(4) + 3
        o.append(f'<text class="pino-usado-c" x="{xm(c):.1f}" y="{yy:.1f}" text-anchor="middle">{bcm}</text>')
    c, r = D.rc(D.pi_hole(1))
    o.append(f'<text class="pino-usado-c" x="{xm(c):.1f}" y="{Y(4) + 3:.1f}" text-anchor="middle">pino 1</text>')
    o.append(f'<circle cx="{xm(c):.1f}" cy="{Y(r):.1f}" r="8.5" fill="none" stroke="var(--ink)" stroke-width="1.6"/>')
    return (f'<svg class="placa" viewBox="0 22 {VB_W:.1f} {VB_H - 44:.1f}" role="img" '
            f'aria-label="Lado do cobre da placa, espelhado: trilhas coloridas por rede e fios encapados W1 a W4">{"".join(o)}</svg>')

def legenda_cobre():
    c = cores_redes()
    itens = [("+5V", "+5 V (barramento das cargas)"), ("+5V_RPI", "+5 V do Raspberry"), ("+5V_EXT", "+5 V da fonte externa"),
             ("+3V3", "3,3 V"), ("GND", "GND")]
    html = "".join(f'<span><i style="background:{c[k]}"></i>{t}</span>' for k, t in itens)
    html += '<span><i style="background:#4a4f5a;height:4px;border-radius:2px"></i>fio encapado (W1 a W4)</span>'
    html += '<span><i style="background:linear-gradient(90deg,#2f5fc4,#0b7d71,#b0307f)"></i>sinais (uma cor por rede)</span>'
    return f'<div class="leg-pinos">{html}</div>'

BOM = [
    (1, "Placa ilhada 5 × 10 cm", "fenolite, face simples, ilhas isoladas, 34 × 15 furos e 4 tiras de cobre na borda", "—", "furos a cada 2,54 mm"),
    (1, "Barra fêmea 2 × 20, pinos longos (stacking)", "2,54 mm", "J1", "o corpo fica no lado do cobre e encaixa no Raspberry; os pinos saem por cima"),
    (1, "Barra de pinos macho 1 × 40 (quebrável)", "2,54 mm", "JP1 (1×3), J2 e J3 (1×3 cada), J4 (1×4), J8 (1×2)", "15 pinos no total. O J4 foi projetado macho: o HC-SR04 tem pinos macho, então ligue com cabo dupont fêmea-fêmea, ou use barra fêmea no lugar"),
    (1, "Barra fêmea 1 × 40 (quebrável)", "2,54 mm", "J5 e J6 (1×3 cada)", "6 pinos, para os módulos DHT11 e buzzer"),
    (1, "Jumper (shunt)", "2,54 mm", "JP1", "escolhe a origem do 5 V das cargas"),
    (1, "Borne de parafuso 2 vias", "passo 5,08 mm", "J7", "entrada da fonte externa de 5 V"),
    (3, "Resistor", "330 Ω, 1/4 W", "R3, R4, R5", "R3 e R4 formam o divisor do ECHO; R5 limita o LED"),
    (2, "Resistor", "10 kΩ, 1/4 W", "R1, R2", "circuito do potenciômetro"),
    (1, "Resistor", "1 kΩ, 1/4 W", "R6", "base do transistor do buzzer"),
    (1, "Capacitor cerâmico", "100 nF", "C1", "circuito do potenciômetro"),
    (1, "Capacitor eletrolítico", "470 µF, 25 V", "C2", "marque a polaridade; fica entre o 5 V e o GND"),
    (1, "Potenciômetro linear", "10 kΩ", "RV1", ""),
    (1, "Transistor NPN", "BC337 (TO-92)", "Q1", "face plana para você: C, B, E"),
    (1, "LED RGB 5 mm", "ânodo comum", "D1", "a perna mais comprida é o comum (+)"),
    (1, "Chave táctil", "6 × 6 mm, 4 pinos", "SW1", "use 2 pinos em diagonal"),
    (1, "Fio estanhado grosso e fio encapado fino", "—", "trilhas e W1 a W4", "4 pedaços de fio encapado para W1 a W4"),
]
EXTERNOS = [
    (1, "Raspberry Pi 3 Model B", "com cartão microSD e fonte do próprio Pi"),
    (1, "Sensor ultrassônico HC-SR04", "4 pinos"),
    (2, "Servomotor", "SG90 ou equivalente (3 fios)"),
    (1, "Módulo DHT11", "3 pinos, com resistor de pull-up"),
    (1, "Buzzer", "ligado ao J6 (confira se o seu é ativo ou passivo)"),
    (1, "Fonte de 5 V externa (opcional)", "para os servos, se o Pi reiniciar quando eles se mexem"),
]

def tabela_bom():
    linhas = "".join(
        f"<tr><td>{q}</td><td>{esc(i)}</td><td>{esc(v)}</td><td>{esc(r)}</td><td>{esc(obs)}</td></tr>"
        for q, i, v, r, obs in BOM)
    ext = "".join(f"<tr><td>{q}</td><td>{esc(i)}</td><td colspan='3'>{esc(o)}</td></tr>" for q, i, o in EXTERNOS)
    return ('<div class="tabela"><table><thead><tr><th>Qtd</th><th>Componente</th><th>Valor ou modelo</th><th>Referência na placa</th><th>Observação</th></tr></thead>'
            f'<tbody>{linhas}<tr><th colspan="5">Para usar a placa (não ficam soldados nela)</th></tr>{ext}</tbody></table></div>')

def csv_bom():
    s = io.StringIO()
    w = csv.writer(s, lineterminator="\n")
    w.writerow(["quantidade", "componente", "valor_ou_modelo", "referencia", "observacao"])
    for q, i, v, r, obs in BOM:
        w.writerow([q, i, v, r, obs])
    for q, i, o in EXTERNOS:
        w.writerow([q, i, "", "externo", o])
    return s.getvalue()

def redes():
    out = {}
    for p in D.PARTS:
        for num, (h, net) in p["pads"].items():
            if net:
                out.setdefault(net, []).append((p["ref"], num, h))
    ordem = ["+5V_RPI", "+5V_EXT", "+5V", "+3V3", "GND"]
    chaves = [n for n in ordem if n in out] + sorted(n for n in out if n not in ordem)
    return {n: out[n] for n in chaves}

def tabela_ligacoes():
    cor = cores_redes()
    linhas = []
    for net, pads in redes().items():
        if len(pads) > 14:
            pads = [p for p in pads if p[0] != "J1"] + [("J1", "vários", "")]
        pads_txt = ", ".join(f"{r}.{n}" + (f" ({h})" if h and r != "J1" else "") for r, n, h in pads)
        linhas.append(f'<tr><td><span class="ponto-rede" style="background:{cor.get(net, "#666")}"></span><code>{esc(net)}</code></td><td>{esc(pads_txt)}</td></tr>')
    return ('<div class="tabela"><table><thead><tr><th>Rede</th><th>Pontos que ela liga (peça.pino e furo)</th></tr></thead>'
            f'<tbody>{"".join(linhas)}</tbody></table></div>')

def csv_ligacoes():
    s = io.StringIO()
    w = csv.writer(s, lineterminator="\n")
    w.writerow(["rede", "referencia", "pino", "furo"])
    for net, pads in redes().items():
        for r, n, h in pads:
            w.writerow([net, r, n, h])
    return s.getvalue()
