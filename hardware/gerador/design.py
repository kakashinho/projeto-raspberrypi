"""Projeto (versão 2) da placa de interface em placa ilhada 5x10 (34 colunas x 15 fileiras) para Raspberry Pi 3.

Coordenadas de furo: "C15" = fileira C, coluna 15, sempre vistas pelo lado dos
componentes. Fileiras A..O de cima para baixo, colunas 1..34 da esquerda para a direita.

v2: barra 2x20 de pinos longos (stacking) -> os 40 pinos do Pi ficam disponíveis por
cima; nenhum pino de comunicação (I2C, UART, SPI0, SPI1/I2S, ID) é usado pela placa.
"""
import re

ROWS = "ABCDEFGHIJKLMNO"
NCOLS, NROWS = 34, 15
PITCH = 2.54
BOARD_X, BOARD_Y, BOARD_W, BOARD_H = 100.0, 100.0, 100.0, 50.0
X0 = BOARD_X + (BOARD_W - (NCOLS - 1) * PITCH) / 2
Y0 = BOARD_Y + (BOARD_H - (NROWS - 1) * PITCH) / 2

LABEL_W, LABEL_H = 101.6, 33.9
LABEL_X = BOARD_X + (BOARD_W - LABEL_W) / 2
LABEL_Y = BOARD_Y + (BOARD_H - LABEL_H) / 2
SEAM_Y = BOARD_Y + LABEL_H
LABEL_B_H = BOARD_Y + BOARD_H - SEAM_Y

def rc(h):
    m = re.fullmatch(r"([A-O])(\d+)", h)
    return int(m.group(2)), ROWS.index(m.group(1)) + 1

def xy(h):
    c, r = rc(h)
    return X0 + (c - 1) * PITCH, Y0 + (r - 1) * PITCH

def gxy(c, r):
    """Coordenada em mm de uma posição fracionária da grade (c, r 1-based)."""
    return X0 + (c - 1) * PITCH, Y0 + (r - 1) * PITCH

def hole(c, r):
    return f"{ROWS[r - 1]}{c}"

PI_BCM = {3: 2, 5: 3, 7: 4, 8: 14, 10: 15, 11: 17, 12: 18, 13: 27, 15: 22, 16: 23, 18: 24, 19: 10,
          21: 9, 22: 25, 23: 11, 24: 8, 26: 7, 27: 0, 28: 1, 29: 5, 31: 6, 32: 12, 33: 13, 35: 19,
          36: 16, 37: 26, 38: 20, 40: 21}
PI_POWER = {1: "3V3", 17: "3V3", 2: "5V", 4: "5V", 6: "GND", 9: "GND", 14: "GND", 20: "GND",
            25: "GND", 30: "GND", 34: "GND", 39: "GND"}

PI_PIN_NET = {
    1: "+3V3", 17: "+3V3", 2: "+5V_RPI", 4: "+5V_RPI",
    6: "GND", 9: "GND", 14: "GND", 20: "GND", 25: "GND", 30: "GND", 34: "GND", 39: "GND",
    7: "GPIO4_LED_R", 11: "GPIO17_LED_G", 13: "GPIO27_LED_B", 15: "GPIO22_DHT",
    16: "GPIO23_TRIG", 18: "GPIO24_ECHO", 22: "GPIO25_POT_CARGA", 32: "GPIO12_POT_LEIT",
    29: "GPIO5_BOTAO", 31: "GPIO6_BUZZER", 33: "GPIO13_SERVO1", 37: "GPIO26_SERVO2",
}
PI_JUMPER_GROUPS = [["6", "9", "14", "20", "25", "30", "34", "39"], ["1", "17"], ["2", "4"]]

def pi_hole(n):
    if n % 2:
        return hole(15 + (n - 1) // 2, 3)
    return hole(15 + (n - 2) // 2, 2)

P7 = ("Resistor_THT", "R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
P10 = ("Resistor_THT", "R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal")
HDR2 = ("Connector_PinHeader_2.54mm", "PinHeader_1x02_P2.54mm_Vertical")
HDR3 = ("Connector_PinHeader_2.54mm", "PinHeader_1x03_P2.54mm_Vertical")
HDR4 = ("Connector_PinHeader_2.54mm", "PinHeader_1x04_P2.54mm_Vertical")
SKT3 = ("Connector_PinSocket_2.54mm", "PinSocket_1x03_P2.54mm_Vertical")

PARTS = [
    dict(ref="J1", value="Barra fêmea 2x20 pinos longos (stacking)", side="bottom",
         lib=("Connector_PinSocket_2.54mm", "PinSocket_2x20_P2.54mm_Vertical"),
         pads={str(n): (pi_hole(n), PI_PIN_NET.get(n)) for n in range(1, 41)}),
    dict(ref="J7", value="Borne 5V externa",
         lib=("TerminalBlock_Phoenix", "TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal"),
         pads={"1": ("B4", "+5V_EXT"), "2": ("B2", "GND")}),
    dict(ref="JP1", value="Seletor 5V (jumper)", lib=HDR3,
         pads={"1": ("B13", "+5V_RPI"), "2": ("B12", "+5V"), "3": ("B11", "+5V_EXT")}),
    dict(ref="C2", value="470uF 25V", lib=("Capacitor_THT", "CP_Radial_D10.0mm_P5.00mm"), pitch2=5.08,
         pads={"1": ("L15", "+5V"), "2": ("N15", "GND")}),
    dict(ref="RV1", value="Pot 10k linear", lib=None, kind="pot",
         pads={"1": ("J6", "POT_1"), "2": ("J4", "POT_X"), "3": ("J2", "POT_X")}),
    dict(ref="C1", value="100nF", lib=("Capacitor_THT", "C_Disc_D5.0mm_W2.5mm_P5.00mm"), pitch2=5.08,
         pads={"1": ("I3", "POT_X"), "2": ("I1", "GND")}),
    dict(ref="R2", value="10k", lib=P7, pads={"1": ("I4", "POT_X"), "2": ("F4", "GPIO12_POT_LEIT")}),
    dict(ref="R1", value="10k", lib=P7, pads={"1": ("I6", "POT_1"), "2": ("F6", "GPIO25_POT_CARGA")}),
    dict(ref="J4", value="HC-SR04", lib=HDR4,
         pads={"1": ("J11", "+5V"), "2": ("K11", "GPIO23_TRIG"), "3": ("L11", "ECHO_5V"), "4": ("M11", "GND")}),
    dict(ref="R3", value="330", lib=P7, pads={"1": ("I9", "GPIO24_ECHO"), "2": ("L9", "ECHO_5V")}),
    dict(ref="R4", value="330", lib=P7, pads={"1": ("I7", "GPIO24_ECHO"), "2": ("L7", "GND")}),
    dict(ref="R5", value="330", lib=P10, pads={"1": ("E15", "+3V3"), "2": ("E19", "LED_A")}),
    dict(ref="D1", value="LED RGB anodo comum", lib=None, kind="led",
         pads={"1": ("G18", "GPIO4_LED_R"), "2": ("G19", "LED_A"),
               "3": ("G20", "GPIO17_LED_G"), "4": ("G21", "GPIO27_LED_B")}),
    dict(ref="J5", value="DHT11", lib=SKT3,
         pads={"1": ("F24", "+3V3"), "2": ("G24", "GPIO22_DHT"), "3": ("H24", "GND")}),
    dict(ref="SW1", value="Chave táctil", lib=None, kind="sw",
         pads={"1": ("F25", None), "2": ("F28", "GPIO5_BOTAO"), "3": ("H25", "GND"), "4": ("H28", None)}),
    dict(ref="J8", value="Botão externo", lib=HDR2, pads={"1": ("E28", "GPIO5_BOTAO"), "2": ("E27", "GND")}),
    dict(ref="R6", value="1k", lib=P10, pads={"1": ("J30", "GPIO6_BUZZER"), "2": ("J26", "Q1_BASE")}),
    dict(ref="Q1", value="BC337", lib=("Package_TO_SOT_THT", "TO-92_Inline_Wide"),
         pads={"1": ("L25", "BUZ_NEG"), "2": ("L26", "Q1_BASE"), "3": ("L27", "GND")}),
    dict(ref="J6", value="Buzzer", lib=SKT3,
         pads={"1": ("L22", "+5V"), "2": ("L23", None), "3": ("L24", "BUZ_NEG")}),
    dict(ref="J2", value="Servo 1", lib=HDR3,
         pads={"1": ("N31", "GND"), "2": ("M31", "+5V"), "3": ("L31", "GPIO13_SERVO1")}),
    dict(ref="J3", value="Servo 2", lib=HDR3,
         pads={"1": ("N33", "GND"), "2": ("M33", "+5V"), "3": ("L33", "GPIO26_SERVO2")}),
]

JUMPERS = [
    ("W1", "GPIO23_TRIG", "A22", "K10", 106.3),
    ("W2", "GPIO24_ECHO", "A23", "H8", 105.6),
    ("W3", "GPIO25_POT_CARGA", "A25", "E6", 104.9),
    ("W4", "GPIO12_POT_LEIT", "A30", "E4", 104.2),
]

def run(a, b):
    (c1, r1), (c2, r2) = rc(a), rc(b)
    assert c1 == c2 or r1 == r2, (a, b)
    n = max(abs(c2 - c1), abs(r2 - r1))
    dc = (c2 > c1) - (c2 < c1)
    dr = (r2 > r1) - (r2 < r1)
    return [hole(c1 + dc * i, r1 + dr * i) for i in range(n + 1)]

def path(*corners):
    out = []
    for a, b in zip(corners, corners[1:]):
        seg = run(a, b)
        out += seg if not out else seg[1:]
    return out

TRACKS = {
    "+5V_RPI": [path("B15", "A15", "A13", "B13"), path("B16", "A16", "A15")],
    "+5V_EXT": [path("B4", "B11")],
    "+5V": [path("B12", "M12", "M33"), path("J12", "J11"), path("L15", "M15"), path("L22", "M22")],
    "GND": [path("B2", "B1", "N1", "N34"), path("C34", "N34"), path("L7", "N7"), path("M11", "N11"),
            path("C27", "L27"), path("H27", "H24")],
    "+3V3": [path("C15", "E15"), path("C23", "F23", "F24")],
    "LED_A": [path("E19", "G19")],
    "GPIO4_LED_R": [path("C18", "G18")],
    "GPIO17_LED_G": [path("C20", "G20")],
    "GPIO27_LED_B": [path("C21", "G21")],
    "GPIO22_DHT": [path("C22", "G22", "G24")],
    "GPIO23_TRIG": [path("B22", "A22"), path("K10", "K11")],
    "GPIO24_ECHO": [path("B23", "A23"), path("H8", "I8"), path("I7", "I9")],
    "GPIO25_POT_CARGA": [path("B25", "A25"), path("E6", "F6")],
    "GPIO12_POT_LEIT": [path("B30", "A30"), path("E4", "F4")],
    "POT_X": [path("J2", "J4"), path("I3", "J3"), path("I4", "J4")],
    "POT_1": [path("I6", "J6")],
    "ECHO_5V": [path("L9", "L11")],
    "GPIO5_BOTAO": [path("C29", "F29", "F28"), path("E29", "E28")],
    "GPIO6_BUZZER": [path("C30", "J30")],
    "Q1_BASE": [path("J26", "L26")],
    "BUZ_NEG": [path("L25", "L24")],
    "GPIO13_SERVO1": [path("C31", "L31")],
    "GPIO26_SERVO2": [path("C33", "L33")],
}

POWER_NETS = {"+5V", "+5V_RPI", "+5V_EXT", "GND"}

def check(verbose=True):
    errors = []
    owner = {}

    def claim(h, net, src):
        c, r = rc(h)
        if not (1 <= c <= NCOLS and 1 <= r <= NROWS):
            errors.append(f"{src}: furo {h} fora da placa")
            return
        key = net if net is not None else f"<nc:{src}>"
        if h in owner and owner[h][0] != key:
            errors.append(f"furo {h}: {owner[h][1]} ({owner[h][0]}) x {src} ({key})")
        owner.setdefault(h, (key, src))

    for p in PARTS:
        for num, (h, net) in p["pads"].items():
            claim(h, net, f"{p['ref']}.{num}")
    for ref, net, a, b, _ in JUMPERS:
        claim(a, net, ref + ".a")
        claim(b, net, ref + ".b")
    for net, paths in TRACKS.items():
        for pth in paths:
            for h in pth:
                claim(h, net, "trilha " + net)

    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        parent[find(a)] = find(b)

    for net, paths in TRACKS.items():
        for pth in paths:
            for a, b in zip(pth, pth[1:]):
                union(a, b)
    for ref, net, a, b, _ in JUMPERS:
        union(a, b)
    j1 = PARTS[0]["pads"]
    for g in PI_JUMPER_GROUPS:
        for n in g[1:]:
            union(j1[g[0]][0], j1[n][0])

    netpads = {}
    for p in PARTS:
        for num, (h, net) in p["pads"].items():
            if net:
                netpads.setdefault(net, []).append((f"{p['ref']}.{num}", h))
    for net, lst in netpads.items():
        roots = {find(h) for _, h in lst}
        if len(roots) > 1:
            groups = {}
            for name, h in lst:
                groups.setdefault(find(h), []).append(name)
            errors.append(f"net {net} dividida: {list(groups.values())}")
        if len(lst) == 1:
            errors.append(f"net {net} só tem um pad: {lst}")

    if verbose:
        print("ERROS:" if errors else "Sem erros.")
        for e in errors:
            print("  -", e)
    return errors, owner

def ascii_map(owner):
    abbrev = {}
    lines = ["     " + "".join(f"{c:>3}" for c in range(1, NCOLS + 1))]
    for r in range(1, NROWS + 1):
        row = f"  {ROWS[r-1]}  "
        for c in range(1, NCOLS + 1):
            h = hole(c, r)
            if h in owner:
                net = owner[h][0]
                if net not in abbrev:
                    abbrev[net] = chr(ord("a") + len(abbrev)) if len(abbrev) < 26 else chr(ord("A") + len(abbrev) - 26)
                row += f"{abbrev[net]:>3}"
            else:
                row += "  ."
        lines.append(row)
    lines.append("")
    lines += [f"  {v} = {k}" for k, v in abbrev.items() if not k.startswith("<nc:J1")]
    return "\n".join(lines)

if __name__ == "__main__":
    errs, own = check()
    print(ascii_map(own))
