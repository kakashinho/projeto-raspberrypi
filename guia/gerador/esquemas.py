"""Esquemas e figuras explicativas de cada tarefa (SVG escrito à mão, sem bibliotecas).

Todas usam as classes CSS da página (e-fio, e-txt, ...) e a variável --c da tarefa.
"""
import math

from desenhos import esc

_CONT = [0]

def _svg(vb, rotulo, corpo, cls="esq", extra=""):
    _CONT[0] += 1
    corpo = corpo.replace('id="m', f'id="u{_CONT[0]}m').replace('url(#m', f'url(#u{_CONT[0]}m')
    return f'<svg class="{cls}" viewBox="{vb}" role="img" aria-label="{esc(rotulo)}"{extra}>{corpo}</svg>'

def T(x, y, s, cls="e-txt", anchor="start"):
    return f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}">{esc(s)}</text>'

def fio(*pts, cls="e-fio"):
    d = "M" + " L".join(f"{x},{y}" for x, y in pts)
    return f'<path class="{cls}" d="{d}"/>'

def dot(x, y):
    return f'<circle class="e-dot" cx="{x}" cy="{y}" r="3.4"/>'

def _zz(length, amp, n=3, lead=8):
    """Pontos (u, v) de um resistor em ziguezague: u ao longo do comprimento, v para os lados."""
    zl = length - 2 * lead
    pts = [(0, 0), (lead, 0)]
    for k in range(1, 2 * n):
        pts.append((lead + zl * k / (2 * n), -amp if k % 2 else amp))
    pts += [(length - lead, 0), (length, 0)]
    return pts

def zigzag(x, y, length, amp, vertical=False, cls="e-fio", lead=8):
    """Resistor em ziguezague centrado em (x, y)."""
    if vertical:
        pts = [(x + v, y - length / 2 + u) for u, v in _zz(length, amp, lead=lead)]
    else:
        pts = [(x - length / 2 + u, y + v) for u, v in _zz(length, amp, lead=lead)]
    d = "M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in pts)
    return f'<path class="{cls}" d="{d}"/>'

def res(x, y, w=52, h=18, vertical=False):
    """Resistor como retângulo com terminais curtos (as ligações chegam às bordas)."""
    if vertical:
        w, h = h, w
    return f'<rect class="e-comp" x="{x - w / 2}" y="{y - h / 2}" width="{w}" height="{h}"/>'

def gnd(x, y):
    return (f'<path class="e-fio" d="M{x},{y} v8 M{x - 13},{y + 8} h26 M{x - 8},{y + 13} h16 M{x - 3},{y + 18} h6"/>')

def seta_marker(i):
    return (f'<defs><marker id="m{i}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
            f'orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs>')

def dim(x1, x2, y, rot):
    """cota horizontal com setas nas duas pontas."""
    return (f'<line class="e-eixo" x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" marker-start="url(#m1)" marker-end="url(#m1)"/>'
            + T((x1 + x2) / 2, y - 6, rot, "e-mut", "middle"))

def servo_pwm():
    ESC = 12
    per = 20 * ESC
    x0 = 100
    o = [seta_marker(1)]
    linhas = [(0.5, 0, "0°", "pulso de 0,5 ms"), (1.5, 90, "90°", "pulso de 1,5 ms"), (2.5, 180, "180°", "pulso de 2,5 ms")]
    for i, (ms, ang, nome, txt) in enumerate(linhas):
        yb = 66 + i * 66
        yh = yb - 30
        o.append(T(12, yb - 14, nome, "e-grande"))
        o.append(T(12, yb + 4, txt, "e-mut"))
        d = f"M{x0},{yb}"
        for p in range(2):
            xs = x0 + p * per + 10
            d += f" L{xs},{yb} L{xs},{yh} L{xs + ms * ESC},{yh} L{xs + ms * ESC},{yb}"
        d += f" L{x0 + 2 * per},{yb}"
        o.append(f'<path class="e-pulso" d="{d}"/>')
        cx, cy = 580, yb + 6
        o.append(f'<path class="e-eixo" d="M{cx - 28},{cy} A28 28 0 0 1 {cx + 28},{cy}" fill="none"/>')
        th = math.radians(ang)
        ex, ey = cx + 24 * -math.cos(th), cy - 24 * math.sin(th)
        o.append(f'<line class="e-pulso" x1="{cx}" y1="{cy}" x2="{ex:.1f}" y2="{ey:.1f}"/>')
        o.append(f'<circle class="e-dot" cx="{cx}" cy="{cy}" r="3.5"/>')
    o.append(dim(x0, x0 + per, 232, "período: 20 ms (50 vezes por segundo)"))
    o.append(T(580, 22, "braço do servo", "e-mut", "middle"))
    o.append(T(x0, 22, "sinal no fio laranja (nível alto = linha de cima)", "e-mut"))
    return _svg("0 0 640 250", "Largura do pulso de 0,5, 1,5 e 2,5 milissegundos define o ângulo do servo em 0, 90 e 180 graus", "".join(o))

def ultrassom():
    o = [seta_marker(1)]
    o.append('<rect x="14" y="52" width="100" height="62" rx="5" fill="#1d5088"/>')
    for cx in (42, 86):
        o.append(f'<circle cx="{cx}" cy="83" r="17" fill="#eef2f3"/><circle cx="{cx}" cy="83" r="11" fill="#1b1b1b"/><circle cx="{cx}" cy="83" r="5" fill="#6a6f72"/>')
    o.append(T(64, 138, "HC-SR04", "e-mut", "middle"))
    for r, op in ((46, 1), (84, .7), (122, .45)):
        a = math.radians(32)
        x1, y1 = 114 + r * math.cos(a), 83 - r * math.sin(a)
        x2, y2 = 114 + r * math.cos(a), 83 + r * math.sin(a)
        o.append(f'<path class="e-onda" d="M{x1:.1f},{y1:.1f} A{r} {r} 0 0 1 {x2:.1f},{y2:.1f}" style="opacity:{op}"/>')
    o.append('<rect class="e-carro" x="470" y="54" width="150" height="58" rx="14"/>')
    o.append('<rect x="560" y="62" width="30" height="42" rx="6" class="e-vidro"/>')
    for x in (486, 574):
        o.append(f'<rect class="e-roda" x="{x}" y="48" width="30" height="8" rx="3"/><rect class="e-roda" x="{x}" y="110" width="30" height="8" rx="3"/>')
    o.append(T(545, 136, "carro", "e-mut", "middle"))
    o.append(dim(114, 470, 160, "d  (distância até o carro)"))
    o.append(T(14, 200, "TRIG", "e-mono-b"))
    o.append(f'<path class="e-pulso" d="M80,206 H130 V190 H142 V206 H620"/>')
    o.append(T(150, 188, "pulso de 10 µs: o sensor solta o som", "e-mut"))
    o.append(T(14, 250, "ECHO", "e-mono-b"))
    o.append(f'<path class="e-pulso" d="M80,256 H200 V240 H430 V256 H620"/>')
    o.append(dim(200, 430, 232, ""))
    o.append(T(315, 228, "t: tempo até o eco voltar", "e-mut", "middle"))
    o.append(T(14, 292, "d = t × 343 m/s ÷ 2", "e-grande"))
    o.append(T(260, 292, "Exemplo: t = 0,29 ms  →  d = 5 cm", "e-txt"))
    return _svg("0 0 640 304", "O sensor emite um pulso no TRIG, o som bate no carro e volta; o tempo do eco no pino ECHO dá a distância", "".join(o))

def divisor_echo():
    o = []
    o.append(T(10, 40, "ECHO do sensor", "e-txt"))
    o.append(T(10, 56, "sai com 5 V", "e-mut"))
    o.append(fio((110, 48), (150, 48)))
    o.append(res(176, 48))
    o.append(T(176, 28, "R3 330 Ω", "e-mono", "middle"))
    o.append(fio((202, 48), (270, 48)))
    o.append(dot(270, 48))
    o.append(fio((270, 48), (340, 48)))
    o.append(f'<rect class="e-chip" x="340" y="32" width="112" height="32" rx="16"/>')
    o.append(T(396, 53, "GPIO24", "e-chip-t", "middle"))
    o.append(T(396, 24, "recebe 2,5 V", "e-ok", "middle"))
    o.append(fio((270, 48), (270, 84)))
    o.append(res(270, 110, vertical=True))
    o.append(T(292, 114, "R4 330 Ω", "e-mono"))
    o.append(fio((270, 136), (270, 152)))
    o.append(gnd(270, 152))
    o.append(T(10, 160, "5 V × 330 ÷ (330 + 330) = 2,5 V", "e-txt"))
    o.append(T(10, 180, "O GPIO do Pi aguenta no máximo 3,3 V.", "e-mut"))
    return _svg("0 0 470 196", "Divisor de tensão com dois resistores de 330 ohms reduz o 5 volts do ECHO para 2,5 volts no GPIO24", "".join(o))

def rc_circuito():
    """Circuito do potenciômetro com capacitor. X = ponto onde R2, C1, cursor e ponta 3 se encontram.
    Potenciômetro: retângulo com uma seta curta vinda de cima (o cursor), como no símbolo padrão."""
    marca = ('<defs><marker id="m8" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
             'orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs>')
    o = [marca]
    o.append(T(8, 64, "GPIO12", "e-gpio"))
    o.append(T(8, 81, "carrega", "e-mut"))
    o.append(fio((64, 70), (88, 70)))
    o.append(res(120, 70, 64, 24))
    o.append(T(120, 46, "R2  10 kΩ", "e-mono", "middle"))
    o.append(fio((152, 70), (402, 70), (402, 130), (386, 130)))
    o.append(dot(190, 70))
    o.append(dot(345, 70))
    o.append(T(190, 58, "X", "e-ponto-x", "middle"))
    o.append(fio((190, 70), (190, 112)))
    o.append('<path class="e-fio" d="M168,112 H212 M168,123 H212"/>')
    o.append(fio((190, 123), (190, 152)))
    o.append(gnd(190, 152))
    o.append(T(158, 122, "C1  100 nF", "e-mono", "end"))
    o.append(res(345, 130, 82, 28))
    o.append('<line class="e-fio" x1="345" y1="70" x2="345" y2="114" marker-end="url(#m8)"/>')
    o.append(T(334, 98, "2 · cursor", "e-mono", "end"))
    o.append(T(295, 121, "1", "e-pino-pot", "middle"))
    o.append(T(394, 121, "3", "e-pino-pot", "middle"))
    o.append(T(302, 170, "POTENCIÔMETRO  10 kΩ", "e-mono", "start"))
    o.append(fio((304, 130), (288, 130), (288, 222), (202, 222)))
    o.append(res(170, 222, 64, 24))
    o.append(T(170, 198, "R1  10 kΩ", "e-mono", "middle"))
    o.append(fio((138, 222), (64, 222)))
    o.append(T(8, 216, "GPIO25", "e-gpio"))
    o.append(T(8, 233, "lê o tempo", "e-mut"))
    return _svg("0 0 470 250", "Circuito: o GPIO12 carrega o capacitor C1 por R2; o potenciômetro, desenhado como retângulo com seta, liga o cursor e a ponta 3 ao ponto X e a ponta 1 ao GPIO25 por R1",
                "".join(o), cls="esq rc")

def rc_curva():
    """Como a tensão em X sobe com o tempo e o que o código cronometra."""
    ox, oy, W, Hh = 56, 206, 380, 168
    o = [seta_marker(9)]
    o.append(f'<path class="e-eixo" d="M{ox},{oy - Hh - 8} V{oy} H{ox + W + 8}" fill="none"/>')
    o.append(T(ox - 8, oy - Hh + 2, "tensão no ponto X", "e-mut", "start"))
    o.append(T(ox + W + 8, oy + 18, "tempo", "e-mut", "end"))
    o.append(T(ox - 8, oy + 4, "0", "e-mut", "end"))
    o.append(T(ox - 8, oy - Hh + 20, "3,3 V", "e-mut", "end"))
    ylim = oy - Hh / 2
    o.append(f'<line class="e-lim" x1="{ox}" y1="{ylim}" x2="{ox + W}" y2="{ylim}"/>')
    o.append(T(ox + W, ylim + 20, "limiar: acima daqui o GPIO lê “1”", "e-mut", "end"))

    def curva(tau):
        pts = []
        for x in range(0, W + 1, 5):
            pts.append(f"{ox + x},{oy - Hh * (1 - math.exp(-x / tau)):.1f}")
        return "M" + " L".join(pts)

    ta, tb = 85, 170
    o.append(f'<path class="e-pulso" d="{curva(ta)}"/>')
    o.append(f'<path class="e-curva2" d="{curva(tb)}"/>')
    xa, xb = ox + 0.693 * ta, ox + 0.693 * tb
    for xx, nm in ((xa, "t1"), (xb, "t2")):
        o.append(f'<line class="e-lim" x1="{xx:.1f}" y1="{ylim}" x2="{xx:.1f}" y2="{oy}"/>')
        o.append(T(f"{xx:.1f}", oy + 17, nm, "e-mono-b", "middle"))
    o.append(f'<line class="e-fio" x1="{xa:.1f}" y1="{oy + 30}" x2="{xb:.1f}" y2="{oy + 30}" marker-start="url(#m9)" marker-end="url(#m9)"/>')
    o.append(T((xa + xb) / 2, oy + 46, "o pot muda esse intervalo", "e-txt", "middle"))
    lx, ly = ox + 190, oy - 52
    o.append(f'<line class="e-pulso" x1="{lx}" y1="{ly}" x2="{lx + 34}" y2="{ly}"/>')
    o.append(T(lx + 42, ly + 4, "pot em um extremo", "e-txt"))
    o.append(f'<line class="e-curva2" x1="{lx}" y1="{ly + 20}" x2="{lx + 34}" y2="{ly + 20}"/>')
    o.append(T(lx + 42, ly + 24, "pot no outro extremo", "e-txt"))
    return _svg("0 0 470 270", "A tensão no ponto X sobe com o tempo; o potenciômetro muda quanto tempo ela leva para cruzar o limiar do GPIO",
                "".join(o), cls="esq rc")

def botao_pullup():
    o = []
    o.append('<rect class="e-caixa" x="6" y="10" width="244" height="108" rx="8"/>')
    o.append(T(16, 28, "dentro do Raspberry", "e-mut"))
    o.append(T(66, 52, "3V3", "e-mono-b", "middle"))
    o.append(fio((66, 52), (66, 60)))
    o.append(res(66, 78, 36, 16, True))
    o.append(T(84, 82, "pull-up interno", "e-mut"))
    o.append(fio((66, 96), (66, 140)))
    o.append(dot(66, 118))
    o.append(fio((66, 118), (150, 118)))
    o.append('<rect class="e-chip" x="150" y="102" width="86" height="32" rx="16"/>')
    o.append(T(193, 123, "GPIO5", "e-chip-t", "middle"))
    o.append(fio((66, 140), (66, 156)))
    o.append('<path class="e-fio" d="M66,156 L86,182"/>')
    o.append('<circle class="e-dot" cx="66" cy="156" r="3.4"/><circle class="e-dot" cx="66" cy="190" r="3.4"/>')
    o.append(fio((66, 190), (66, 204)))
    o.append(gnd(66, 204))
    o.append(T(104, 178, "botão (aberto)", "e-mut"))
    o.append(T(272, 28, "O que o código lê", "e-grande"))
    o.append('<rect class="e-est1" x="262" y="46" width="230" height="52" rx="8"/>')
    o.append(T(276, 68, "solto", "e-txt-b"))
    o.append(T(276, 88, "o resistor puxa o pino para cima", "e-mut"))
    o.append(T(478, 80, "1", "e-grande", "end"))
    o.append('<rect class="e-est0" x="262" y="110" width="230" height="52" rx="8"/>')
    o.append(T(276, 132, "apertado", "e-txt-b"))
    o.append(T(276, 152, "o botão liga o pino ao GND", "e-mut"))
    o.append(T(478, 144, "0", "e-grande", "end"))
    return _svg("0 0 500 240", "O botão usa o resistor pull-up interno do GPIO5: solto lê 1, apertado lê 0", "".join(o))

def led_anodo():
    o = []
    o.append(T(280, 18, "3V3", "e-mono-b", "middle"))
    o.append(fio((280, 24), (280, 34)))
    o.append(res(280, 58, vertical=True, w=52, h=18))
    o.append(T(304, 62, "R5 330 Ω", "e-mono"))
    o.append(fio((280, 84), (280, 112)))
    o.append('<rect class="e-led" x="172" y="112" width="216" height="64" rx="10"/>')
    o.append(T(280, 134, "LED RGB", "e-txt-b", "middle"))
    o.append(T(280, 128 - 22, "+", "e-mono-b", "middle"))
    o.append(T(280, 152, "ânodo comum", "e-mut", "middle"))
    for x, cor, nome, gp in ((214, "#e0302a", "R", "GPIO4"), (280, "#2fb344", "G", "GPIO17"), (346, "#2f6fe0", "B", "GPIO27")):
        o.append(fio((x, 176), (x, 212)))
        o.append(f'<circle cx="{x}" cy="164" r="6" fill="{cor}" stroke="var(--ink)" stroke-width="1"/>')
        o.append(f'<rect class="e-chip" x="{x - 31}" y="212" width="62" height="26" rx="13"/>')
        o.append(T(x, 230, gp, "e-chip-t", "middle"))
    o.append(T(8, 150, "pino em nível", "e-mut"))
    o.append(T(8, 168, "BAIXO (0) = acende", "e-ok-b"))
    o.append(T(8, 186, "ALTO (1) = apaga", "e-mut"))
    o.append(T(8, 210, "por isso:", "e-mut"))
    o.append(T(8, 228, "active_high=False", "e-mono-b"))
    o.append(T(420, 30, "led.color = (R, G, B)", "e-txt-b"))
    sw = [("#e0302a", "(1, 0, 0)", "vermelho"), ("#2fb344", "(0, 1, 0)", "verde"), ("#2f6fe0", "(0, 0, 1)", "azul"),
          ("#f2c200", "(1, 1, 0)", "amarelo"), ("#ffffff", "(1, 1, 1)", "branco")]
    for i, (cor, tup, nm) in enumerate(sw):
        y = 62 + i * 38
        o.append(f'<circle cx="436" cy="{y}" r="12" fill="{cor}" stroke="var(--ink)" stroke-width="1.2"/>')
        o.append(T(458, y - 2, tup, "e-mono"))
        o.append(T(458, y + 14, nm, "e-mut"))
    return _svg("0 0 640 250", "LED RGB de ânodo comum ligado ao 3V3 por um resistor; cada cor acende quando o GPIO vai a nível baixo", "".join(o))

def buzzer_circuit():
    o = []
    o.append(T(330, 16, "5 V", "e-mono-b", "middle"))
    o.append(fio((330, 22), (330, 38)))
    o.append('<circle class="e-comp" cx="330" cy="64" r="26"/>')
    o.append(T(330, 62, "BUZZER", "e-mut", "middle"))
    o.append(T(330, 76, "J6", "e-mut", "middle"))
    o.append(T(316, 52, "+", "e-mono-b", "middle"))
    o.append(fio((330, 90), (330, 122)))
    o.append('<circle class="e-comp" cx="312" cy="156" r="34"/>')
    o.append('<line class="e-fio" x1="300" y1="134" x2="300" y2="178" style="stroke-width:3.5"/>')
    o.append(fio((300, 148), (330, 126)))
    o.append(fio((330, 126), (330, 122)))
    o.append(fio((300, 166), (330, 186)))
    o.append('<path class="e-dot" d="M322,182 l-9,0 l5,-8 z" transform="rotate(10 322 182)"/>')
    o.append(fio((330, 186), (330, 206)))
    o.append(gnd(330, 206))
    o.append(T(360, 150, "Q1 BC337", "e-mono"))
    o.append(T(340, 128, "coletor", "e-mut"))
    o.append(T(340, 196, "emissor", "e-mut"))
    o.append(fio((72, 156), (162, 156)))
    o.append(res(188, 156, 52, 18))
    o.append(fio((214, 156), (300, 156)))
    o.append(T(188, 138, "R6 1 kΩ", "e-mono", "middle"))
    o.append(T(8, 152, "GPIO6", "e-mono-b"))
    o.append(T(8, 168, "liga o Q1", "e-mut"))
    o.append(T(250, 196, "base", "e-mut", "middle"))
    o.append(T(8, 254, "GPIO6 em nível alto → Q1 conduz → o buzzer recebe 5 V.", "e-txt"))
    return _svg("0 0 500 266", "O GPIO6 aciona a base do transistor Q1 por um resistor de 1 quilo-ohm; o transistor liga o buzzer ao 5 volts", "".join(o))

def notas():
    nomes = ["C5", "D5", "E5", "F5", "G5", "A5", "B5", "C6"]
    freq = [523, 587, 659, 698, 784, 880, 988, 1047]
    usadas = {"C5", "E5", "G5", "C6"}
    o = []
    for i, (n, f) in enumerate(zip(nomes, freq)):
        x = 10 + i * 58
        cls = "e-tecla on" if n in usadas else "e-tecla"
        o.append(f'<rect class="{cls}" x="{x}" y="10" width="54" height="86" rx="4"/>')
        o.append(T(x + 27, 80, n, "e-txt-b" if n in usadas else "e-mut", "middle"))
        o.append(T(x + 27, 114, f"{f} Hz", "e-mut", "middle"))
    o.append(T(10, 140, "Tone(\"C5\") Tone(\"E5\") Tone(\"G5\") Tone(\"C6\")", "e-mono"))
    return _svg("0 0 480 150", "Teclado com as notas C5, E5, G5 e C6 destacadas e suas frequências em hertz", "".join(o))

def dht_fluxo():
    o = [seta_marker(3)]
    o.append('<rect x="14" y="14" width="76" height="62" rx="5" fill="#1f6b52"/><rect x="26" y="20" width="52" height="34" rx="3" fill="#3b82c8"/>')
    for i in range(4):
        o.append(f'<line x1="32" y1="{27 + i * 7}" x2="72" y2="{27 + i * 7}" stroke="#2a64a0" stroke-width="2.4" stroke-linecap="round"/>')
    o.append(T(52, 68, "DHT11", "e-mono-w", "middle"))
    o.append(f'<line class="e-fio" x1="92" y1="44" x2="170" y2="44" marker-end="url(#m3)"/>')
    o.append(T(131, 36, "1 fio (DATA)", "e-mut", "middle"))
    o.append(f'<rect class="e-chip" x="172" y="28" width="92" height="32" rx="16"/>')
    o.append(T(218, 49, "GPIO22", "e-chip-t", "middle"))
    o.append(f'<line class="e-fio" x1="266" y1="44" x2="316" y2="44" marker-end="url(#m3)"/>')
    o.append('<rect class="e-caixa" x="318" y="18" width="150" height="52" rx="8"/>')
    o.append(T(393, 40, "dht.temperature", "e-mono", "middle"))
    o.append(T(393, 58, "dht.humidity", "e-mono", "middle"))
    o.append(f'<line class="e-fio" x1="470" y1="44" x2="500" y2="44" marker-end="url(#m3)"/>')
    o.append('<rect x="502" y="16" width="130" height="56" rx="8" fill="#0f1a14"/>')
    o.append(T(567, 38, "26 °C", "e-mono-w", "middle"))
    o.append(T(567, 58, "58 %", "e-mono-w", "middle"))
    def faixa(y, nome, lo, hi, marca, erro, unidade, passo):
        x0, x1 = 150, 610
        o.append(T(10, y + 4, nome, "e-txt-b"))
        o.append(f'<rect class="e-faixa" x="{x0}" y="{y - 8}" width="{x1 - x0}" height="16" rx="8"/>')
        def px(v):
            return x0 + (v - lo) / (hi - lo) * (x1 - x0)
        o.append(f'<rect class="e-erro" x="{px(marca - erro):.1f}" y="{y - 8}" width="{px(marca + erro) - px(marca - erro):.1f}" height="16" rx="3"/>')
        o.append(f'<path class="e-dot" d="M{px(marca):.1f},{y - 12} l-6,-10 h12 z"/>')
        o.append(T(f"{px(marca):.1f}", y - 28, f"{marca} {unidade}", "e-mono-b", "middle"))
        v = lo
        while v <= hi:
            o.append(T(f"{px(v):.1f}", y + 26, str(v), "e-mut", "middle"))
            v += passo
        o.append(T(x1, y + 44, f"faixa {lo} a {hi} {unidade}, erro de ±{erro}", "e-mut", "end"))
    faixa(150, "Temperatura", 0, 50, 26, 2, "°C", 10)
    faixa(240, "Umidade", 20, 80, 58, 5, "%", 10)
    o.append(T(10, 312, "Leia no máximo 1 vez a cada 2 segundos. Falhar de vez em quando é normal.", "e-txt"))
    return _svg("0 0 640 324", "O DHT11 manda temperatura e umidade por um fio ao GPIO22; faixas de medição e erro do sensor", "".join(o))

def sequencia():
    cols = [(70, "Carro", None), (235, "Sensor", 2), (410, "main.py", 6), (590, "Cancela e sinais", "1 e 4"), (730, "Servidor", 7)]
    o = [seta_marker(4)]
    for x, nome, t in cols:
        o.append(f'<rect class="e-caixa" x="{x - 62}" y="8" width="124" height="34" rx="8"/>')
        o.append(T(x, 30, nome, "e-txt-b", "middle"))
        o.append(f'<line class="e-vida" x1="{x}" y1="42" x2="{x}" y2="392"/>')
    X = {n: x for x, n, _ in cols}
    passos = [
        ("Carro", "Sensor", "chega a menos de 5 cm", False),
        ("Sensor", "main.py", "carro_presente() = True", False),
        ("main.py", "Servidor", "GET /api/resumo: tem vaga?", False),
        ("main.py", "Cancela e sinais", "amarelo, música, abrir", False),
        ("Carro", "Sensor", "passa e se afasta", False),
        ("main.py", "Cancela e sinais", "fechar, verde", False),
        ("main.py", "Servidor", "POST /api/eventos: entrada", False),
    ]
    for i, (a, b, txt, _) in enumerate(passos):
        y = 76 + i * 46
        xa, xb = X[a], X[b]
        o.append(f'<line class="e-fio" x1="{xa}" y1="{y}" x2="{xb}" y2="{y}" marker-end="url(#m4)"/>')
        mid = (xa + xb) / 2
        o.append(T(mid, y - 8, txt, "e-mut e-halo", "middle"))
        o.append(f'<circle class="e-passo" cx="{min(xa, xb) + 14}" cy="{y + 14}" r="9"/>')
        o.append(T(min(xa, xb) + 14, y + 18, str(i + 1), "e-passo-n", "middle"))
    return _svg("0 0 800 400", "Sequência de um carro entrando: sensor detecta, main.py consulta o servidor, abre a cancela, fecha e registra a entrada", "".join(o))

def banco():
    tabelas = [
        ("eventos", ["id", "tipo", "criado_em"], [("1", "entrada", "2026-11-05 08:12"), ("2", "saida", "2026-11-05 08:40")]),
        ("ambiente", ["id", "temperatura", "umidade", "criado_em"], [("1", "26.0", "58", "2026-11-05 08:00")]),
        ("comandos", ["id", "alvo", "acao", "feito"], [("1", "saida", "abrir", "0")]),
    ]
    o = []
    bh = max(62 + len(c) * 20 + 10 + 30 + (len(l) - 1) * 16 + 14 for _, c, l in tabelas) + 10
    for i, (nome, cols, linhas) in enumerate(tabelas):
        x = 8 + i * 232
        w = 220
        o.append(f'<rect class="e-caixa" x="{x}" y="10" width="{w}" height="{bh}" rx="8"/>')
        o.append(f'<rect class="e-cab-tab" x="{x}" y="10" width="{w}" height="30" rx="8"/>')
        o.append(T(x + 12, 31, nome, "e-tab-t"))
        for j, c in enumerate(cols):
            yy = 62 + j * 20
            o.append(T(x + 12, yy, c, "e-mono-b"))
            tipo = {"id": "INTEGER", "tipo": "TEXT", "criado_em": "TEXT", "temperatura": "REAL", "umidade": "REAL",
                    "alvo": "TEXT", "acao": "TEXT", "feito": "INTEGER"}[c]
            o.append(T(x + w - 12, yy, tipo, "e-mut", "end"))
        yl = 62 + len(cols) * 20 + 10
        o.append(f'<line class="e-eixo" x1="{x + 8}" y1="{yl - 6}" x2="{x + w - 8}" y2="{yl - 6}"/>')
        o.append(T(x + 12, yl + 12, "exemplo", "e-mut"))
        for k, ln in enumerate(linhas):
            o.append(T(x + 12, yl + 30 + k * 16, "  ".join(ln), "e-mono-s"))
    o.append(T(8, bh + 36, "eventos: o Python grava cada entrada e saída. ambiente: temperatura e umidade da tarefa 5.", "e-txt"))
    o.append(T(8, bh + 56, "comandos: a página pede “abrir saída”; o Python busca o próximo com feito = 0 e marca feito = 1.", "e-txt"))
    return _svg(f"0 0 700 {bh + 72}", "Três tabelas do SQLite: eventos, ambiente e comandos, com colunas e uma linha de exemplo", "".join(o))

def ligacao(linhas, t, titulo_peca="Peça"):
    """linhas: [(peca, placa, destino)] ou ("#", "título do grupo").
    destino = ('gpio', bcm, pino[, nota]) | ('5v',) | ('3v3',) | ('gnd',)"""
    rowh, gh, top, W = 50, 34, 34, 660
    H = top + sum(gh if l[0] == "#" else rowh for l in linhas) + 6
    o = [T(14, 18, titulo_peca.upper(), "e-cab"), T(262, 18, "CONECTOR DA PLACA", "e-cab"), T(468, 18, "RASPBERRY", "e-cab")]
    cor = {"5v": "#d64541", "3v3": "#e8892b", "gnd": "var(--ink)"}
    nome = {"5v": "+5 V", "3v3": "3,3 V", "gnd": "GND"}
    y = top
    for l in linhas:
        if l[0] == "#":
            o.append(f'<rect class="e-grupo" x="6" y="{y + 4}" width="{W - 12}" height="26" rx="6"/>')
            o.append(T(16, y + 22, l[1], "e-grupo-t"))
            y += gh
            continue
        pe, pl, de = l[0], l[1], l[2]
        nota = de[3] if de[0] == "gpio" and len(de) > 3 else ""
        cy = y + rowh / 2
        c = "var(--c)" if de[0] == "gpio" else cor[de[0]]
        o.append(f'<line x1="186" y1="{cy}" x2="262" y2="{cy}" stroke="{c}" stroke-width="3.2" stroke-linecap="round"/>')
        o.append(f'<line x1="430" y1="{cy}" x2="478" y2="{cy}" stroke="{c}" stroke-width="3.2" stroke-linecap="round"/>')
        o.append(f'<rect class="e-peca-box" x="10" y="{cy - 18}" width="176" height="36" rx="7"/>')
        o.append(T(22, cy + 5, pe, "e-txt"))
        o.append(f'<rect class="e-placa-box" x="262" y="{cy - 18}" width="168" height="36" rx="7"/>')
        o.append(T(274, cy + 5, pl, "e-mono"))
        if de[0] == "gpio":
            bcm, pino = de[1], de[2]
            o.append(f'<circle class="e-pino" cx="496" cy="{cy}" r="16"/>')
            o.append(T(496, cy + 5, str(pino), "e-pino-n", "middle"))
            o.append(T(520, cy - 2, f"GPIO{bcm}", "e-mono-b"))
            o.append(T(520, cy + 14, f"pino {pino}" + (f" · {nota}" if nota else ""), "e-mut"))
        else:
            o.append(f'<rect x="480" y="{cy - 15}" width="30" height="30" rx="5" fill="{cor[de[0]]}" stroke="var(--muted)"/>')
            o.append(T(520, cy + 5, nome[de[0]], "e-mono-b"))
        y += rowh
    return _svg(f"0 0 {W} {H}", "Ligação de cada pino da peça ao conector da placa e ao pino do Raspberry", "".join(o), cls=f"lig k{t}")

def servo_malha():
    o = [seta_marker(7)]

    def caixa(x, y, w, h, a, b=None):
        o.append(f'<rect class="e-caixa" x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/>')
        o.append(T(x + w / 2, y + (22 if b else h / 2 + 5), a, "e-txt-b", "middle"))
        if b:
            o.append(T(x + w / 2, y + 40, b, "e-mut", "middle"))
    caixa(8, 34, 118, 56, "Pulso do Pi", "0,5 a 2,5 ms")
    o.append('<circle class="e-comp" cx="182" cy="62" r="26"/>')
    o.append(T(182, 67, "erro", "e-txt-b", "middle"))
    o.append(T(170, 108, "pedido − posição real", "e-mut", "end"))
    caixa(238, 34, 100, 56, "Motor", "elétrico, CC")
    caixa(358, 34, 100, 56, "Engrenagens", "mais força")
    caixa(478, 34, 150, 56, "Eixo e braço", "a cancela")
    o.append('<line class="e-fio" x1="126" y1="62" x2="154" y2="62" marker-end="url(#m7)"/>')
    o.append('<line class="e-fio" x1="208" y1="62" x2="236" y2="62" marker-end="url(#m7)"/>')
    o.append('<line class="e-fio" x1="338" y1="62" x2="356" y2="62" marker-end="url(#m7)"/>')
    o.append('<line class="e-fio" x1="458" y1="62" x2="476" y2="62" marker-end="url(#m7)"/>')
    caixa(478, 150, 150, 56, "Potenciômetro", "lê o ângulo do eixo")
    o.append('<line class="e-fio" x1="553" y1="90" x2="553" y2="148" marker-end="url(#m7)"/>')
    o.append(T(561, 124, "gira junto", "e-mut"))
    o.append('<path class="e-fio" d="M478,178 H182 V90" marker-end="url(#m7)"/>')
    o.append(T(330, 170, "realimentação: volta para comparar", "e-txt", "middle"))
    o.append(T(182, 22, "se erro ≠ 0, liga o motor; se erro = 0, para", "e-mut", "middle"))
    return _svg("0 0 640 220", "O servo compara o pulso pedido com a posição real lida por um potenciômetro interno e liga o motor até o erro zerar", "".join(o))

def icone(nome):
    if nome == "logica":
        c = ('<circle cx="22" cy="40" r="10" class="ic-a"/><circle cx="60" cy="18" r="10" class="ic-a"/>'
             '<circle cx="98" cy="40" r="10" class="ic-a"/><path class="ic-l" d="M32,36 L50,23 M70,23 L88,36 M32,44 H88"/>')
        return _svg("0 0 120 60", "Estados do sistema", c, cls="icone")
    if nome == "banco":
        c = ('<path class="ic-a" d="M34 14 v30 a26 8 0 0 0 52 0 v-30 a26 8 0 0 0 -52 0z"/>'
             '<ellipse class="ic-a" cx="60" cy="14" rx="26" ry="8"/><path class="ic-l" d="M34 29 a26 8 0 0 0 52 0"/>')
        return _svg("0 0 120 60", "Banco de dados", c, cls="icone")
    c = ('<rect class="ic-a" x="22" y="6" width="76" height="48" rx="5"/><path class="ic-l" d="M22 18 H98"/>'
         '<rect class="ic-f" x="30" y="26" width="18" height="20" rx="2"/><rect class="ic-f" x="54" y="32" width="10" height="14" rx="2"/>'
         '<rect class="ic-f" x="70" y="22" width="20" height="24" rx="2"/>')
    return _svg("0 0 120 60", "Página web", c, cls="icone")

def sequencia_saida():
    cols = [(80, "Painel", 8), (300, "Servidor", 7), (480, "main.py", 6), (700, "Cancela de saída", 1)]
    o = [seta_marker(5)]
    for x, nome, t in cols:
        o.append(f'<rect class="e-caixa" x="{x - 68}" y="8" width="136" height="34" rx="8"/>')
        o.append(T(x, 30, nome, "e-txt-b", "middle"))
        o.append(f'<line class="e-vida" x1="{x}" y1="42" x2="{x}" y2="332"/>')
    X = {n: x for x, n, _ in cols}
    passos = [
        ("Painel", "Servidor", "POST /api/comandos: saída, abrir"),
        ("main.py", "Servidor", "GET /api/comandos/proximo"),
        ("main.py", "Cancela de saída", "abrir(\"saida\")"),
        (None, None, "espera 2 segundos (o carro sai)"),
        ("main.py", "Cancela de saída", "fechar(\"saida\")"),
        ("main.py", "Servidor", "POST /api/eventos: saída"),
    ]
    for i, (a, b, txt) in enumerate(passos):
        y = 76 + i * 46
        if a is None:
            o.append(f'<rect class="e-espera" x="{X["main.py"] - 130}" y="{y - 18}" width="260" height="30" rx="15"/>')
            o.append(T(X["main.py"], y + 2, txt, "e-txt-b", "middle"))
            o.append(f'<circle class="e-passo" cx="{X["main.py"] - 146}" cy="{y - 3}" r="9"/>')
            o.append(T(X["main.py"] - 146, y + 1, str(i + 1), "e-passo-n", "middle"))
            continue
        xa, xb = X[a], X[b]
        o.append(f'<line class="e-fio" x1="{xa}" y1="{y}" x2="{xb}" y2="{y}" marker-end="url(#m5)"/>')
        o.append(T((xa + xb) / 2, y - 8, txt, "e-mut e-halo", "middle"))
        o.append(f'<circle class="e-passo" cx="{min(xa, xb) + 14}" cy="{y + 14}" r="9"/>')
        o.append(T(min(xa, xb) + 14, y + 18, str(i + 1), "e-passo-n", "middle"))
    return _svg("0 0 800 348", "Sequência da saída: o porteiro clica no painel, o main.py abre a cancela de saída, espera 2 segundos, fecha e registra a saída", "".join(o))

def matriz_pinos():
    """Quem usa qual pino: duas pessoas no mesmo pino ao mesmo tempo = conflito."""
    cols = [2, 3, 4, 5, 6, 12, 13, 17, 22, 23, 24, 25, 26, 27]
    tarefas = [
        (1, "Cancelas", [13, 26]),
        (2, "Presença", [23, 24]),
        (3, "Guarita manual", [5, 12, 25]),
        (4, "Sinalização", [4, 6, 17, 27]),
        (5, "Ambiente", [22]),
    ]
    final = (6, "main.py (sistema final)", [4, 5, 6, 12, 13, 17, 22, 23, 24, 25, 26, 27])
    antigos = [("blink.py (antigo)", [17]), ("sensor_distancia.py (antigo)", [2, 23, 24]), ("led_rgb.py (antigo)", [2, 3, 4])]
    pinos_tarefas = {p for _, _, ps in tarefas for p in ps}
    pinos_antigos = {p for _, ps in antigos for p in ps}
    conflito = {c for c in cols if c in pinos_tarefas and c in pinos_antigos}
    x0, dx, rowh, top = 250, 42, 32, 64
    nlin = len(tarefas) + 1 + len(antigos)
    W, H = x0 + len(cols) * dx + 10, top + nlin * rowh + 10
    o = []
    for i, c in enumerate(cols):
        if c in conflito:
            o.append(f'<rect class="e-conflito" x="{x0 + i * dx}" y="20" width="{dx}" height="{H - 24}" rx="6"/>')
    o.append(T(10, 46, "GPIO (BCM)", "e-cab"))
    for i, c in enumerate(cols):
        o.append(T(x0 + i * dx + dx / 2, 48, str(c), "e-mono-b", "middle"))
    linhas = [(t, nome, ps, "t") for t, nome, ps in tarefas] + [(final[0], final[1], final[2], "f")] + [(0, n, ps, "a") for n, ps in antigos]
    for r, (t, nome, ps, tipo) in enumerate(linhas):
        cy = top + r * rowh + rowh / 2
        if r in (len(tarefas), len(tarefas) + 1):
            o.append(f'<line class="e-linha" x1="10" y1="{top + r * rowh}" x2="{W - 10}" y2="{top + r * rowh}"/>')
        if tipo in ("t", "f"):
            o.append(f'<g class="k{t}"><circle class="e-passo" cx="24" cy="{cy}" r="11"/>{T(24, cy + 4, str(t), "e-passo-n", "middle")}</g>')
            o.append(T(44, cy + 4, nome, "e-txt-b" if tipo == "t" else "e-txt"))
        else:
            o.append(T(44, cy + 4, nome, "e-mut"))
        for p in ps:
            i = cols.index(p)
            cls = "e-ponto-ant" if tipo == "a" else "e-ponto"
            o.append(f'<g class="k{t}"><circle class="{cls}" cx="{x0 + i * dx + dx / 2}" cy="{cy}" r="9"/></g>')
    return _svg(f"0 0 {W} {H}", "Tabela de quais pinos cada tarefa usa. As tarefas 1 a 5 não dividem nenhum pino; o main.py usa todos; scripts antigos dividem os pinos 4, 17, 23 e 24 com as tarefas",
                "".join(o), cls="esq matriz")
