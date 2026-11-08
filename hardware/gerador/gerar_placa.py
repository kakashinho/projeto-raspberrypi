"""Gera placa_interface.kicad_pcb a partir de design.py. Rodar com o Python do KiCad 10:
   "C:\\Program Files\\KiCad\\10.0\\bin\\python.exe" gerar_placa.py <pasta_saida>
"""
import os
import sys
import json
import pcbnew
import design as D

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
NAME = "placa_interface"
LIBDIR = r"C:\Program Files\KiCad\10.0\share\kicad\footprints"

mm = pcbnew.FromMM
V = lambda x, y: pcbnew.VECTOR2I(mm(x), mm(y))

L_HOLES, L_ILHAS, L_LABEL, L_LABEL_EDGE = pcbnew.User_1, pcbnew.User_2, pcbnew.User_3, pcbnew.User_4

board = pcbnew.BOARD()
ls = board.GetEnabledLayers()
for l in (L_HOLES, L_ILHAS, L_LABEL, L_LABEL_EDGE):
    ls.AddLayer(l)
board.SetEnabledLayers(ls)
board.SetLayerName(L_HOLES, "Furos")
board.SetLayerName(L_ILHAS, "Ilhas")
board.SetLayerName(L_LABEL, "Etiqueta")
board.SetLayerName(L_LABEL_EDGE, "Etiqueta.Contorno")

nets = {}

def net(name):
    if name is None:
        return None
    if name not in nets:
        ni = pcbnew.NETINFO_ITEM(board, name)
        board.Add(ni)
        nets[name] = ni
    return nets[name]

def seg(layer, x1, y1, x2, y2, w=0.15, parent=None):
    s = pcbnew.PCB_SHAPE(parent or board)
    s.SetShape(pcbnew.SHAPE_T_SEGMENT)
    s.SetStart(V(x1, y1)); s.SetEnd(V(x2, y2))
    s.SetLayer(layer); s.SetWidth(mm(w))
    (parent or board).Add(s)
    return s

def poly(layer, pts, w=0.15, parent=None):
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        seg(layer, x1, y1, x2, y2, w, parent)

def circ(layer, x, y, r, w=0.15, fill=False, parent=None):
    s = pcbnew.PCB_SHAPE(parent or board)
    s.SetShape(pcbnew.SHAPE_T_CIRCLE)
    s.SetCenter(V(x, y)); s.SetEnd(V(x + r, y))
    s.SetLayer(layer); s.SetWidth(mm(w))
    if fill:
        s.SetFillMode(pcbnew.FILL_T_FILLED_SHAPE)
    (parent or board).Add(s)
    return s

def rect(layer, x1, y1, x2, y2, w=0.15, parent=None):
    s = pcbnew.PCB_SHAPE(parent or board)
    s.SetShape(pcbnew.SHAPE_T_RECT)
    s.SetStart(V(x1, y1)); s.SetEnd(V(x2, y2))
    s.SetLayer(layer); s.SetWidth(mm(w))
    (parent or board).Add(s)
    return s

def text(layer, s, x, y, h=0.9, angle=0, just="c", bold=False, mirror=False, parent=None):
    t = pcbnew.PCB_TEXT(parent or board)
    t.SetText(s)
    t.SetPosition(V(x, y))
    t.SetLayer(layer)
    t.SetTextSize(V(h * 0.85, h))
    t.SetTextThickness(mm(h * (0.2 if bold else 0.13)))
    t.SetTextAngleDegrees(angle)
    t.SetHorizJustify({"c": pcbnew.GR_TEXT_H_ALIGN_CENTER, "l": pcbnew.GR_TEXT_H_ALIGN_LEFT,
                       "r": pcbnew.GR_TEXT_H_ALIGN_RIGHT}[just])
    t.SetVertJustify(pcbnew.GR_TEXT_V_ALIGN_CENTER)
    if mirror:
        t.SetMirrored(True)
    (parent or board).Add(t)
    return t

g = D.gxy

bx, by, bw, bh = D.BOARD_X, D.BOARD_Y, D.BOARD_W, D.BOARD_H
rect(pcbnew.Edge_Cuts, bx, by, bx + bw, by + bh, 0.1)
for cx, cy in ((bx + 5.5, by + 5.0), (bx + bw - 5.5, by + 5.0), (bx + 5.5, by + bh - 5.0), (bx + bw - 5.5, by + bh - 5.0)):
    circ(pcbnew.Edge_Cuts, cx, cy, 1.5, 0.1)
for x1, y1, x2, y2 in ((bx + 9.5, by + 0.8, bx + bw - 9.5, by + 4.6), (bx + 9.5, by + bh - 4.6, bx + bw - 9.5, by + bh - 0.8),
                       (bx + 0.8, by + 9.0, bx + 4.6, by + bh - 9.0), (bx + bw - 4.6, by + 9.0, bx + bw - 0.8, by + bh - 9.0)):
    rect(L_ILHAS, x1, y1, x2, y2, 0.2)
for c in range(1, D.NCOLS + 1):
    for r in range(1, D.NROWS + 1):
        x, y = g(c, r)
        circ(L_HOLES, x, y, 0.5, 0.1)
        circ(L_ILHAS, x, y, 0.95, 0.1)
for c in range(1, D.NCOLS + 1):
    x, _ = g(c, 1)
    for layer, mir in ((pcbnew.F_Fab, False), (pcbnew.B_Fab, True)):
        text(layer, str(c), x, g(c, 1)[1] - 2.6, 0.9, mirror=mir)
        text(layer, str(c), x, g(c, 15)[1] + 2.6, 0.9, mirror=mir)
for r in range(1, D.NROWS + 1):
    _, y = g(1, r)
    for layer, mir in ((pcbnew.F_Fab, False), (pcbnew.B_Fab, True)):
        text(layer, D.ROWS[r - 1], g(1, r)[0] - 2.8, y, 1.0, mirror=mir)
        text(layer, D.ROWS[r - 1], g(34, r)[0] + 2.8, y, 1.0, mirror=mir)

def load(lib, name):
    return pcbnew.FootprintLoad(os.path.join(LIBDIR, lib + ".pretty"), name)

def pads_by_num(fp):
    out = {}
    for p in fp.Pads():
        out.setdefault(p.GetNumber(), []).append(p)
    return out

def place_lib(part):
    fp = load(*part["lib"])
    board.Add(fp)
    if "pitch2" in part:
        for p in fp.Pads():
            if p.GetNumber() == "2":
                p.SetFPRelativePosition(V(part["pitch2"], 0))
    if part.get("side") == "bottom":
        fp.Flip(fp.GetPosition(), pcbnew.FLIP_DIRECTION_LEFT_RIGHT)
    want = {n: D.xy(h) for n, (h, _) in part["pads"].items()}
    nums = sorted(want, key=lambda n: (len(n), n))
    a, b = nums[0], nums[-1]
    for ang in (0, 90, 180, 270):
        fp.SetOrientationDegrees(ang)
        fp.SetPosition(V(0, 0))
        pa = pads_by_num(fp)[a][0].GetPosition()
        pb = pads_by_num(fp)[b][0].GetPosition()
        vx, vy = pcbnew.ToMM(pb.x - pa.x), pcbnew.ToMM(pb.y - pa.y)
        wx, wy = want[b][0] - want[a][0], want[b][1] - want[a][1]
        if abs(vx - wx) < 0.05 and abs(vy - wy) < 0.05:
            fp.SetPosition(V(want[a][0] - pcbnew.ToMM(pa.x), want[a][1] - pcbnew.ToMM(pa.y)))
            break
    else:
        raise SystemExit(f"{part['ref']}: nenhuma rotação encaixa")
    for n, (h, nn) in part["pads"].items():
        for p in pads_by_num(fp)[n]:
            pos = p.GetPosition()
            if abs(pcbnew.ToMM(pos.x) - want[n][0]) > 0.05 or abs(pcbnew.ToMM(pos.y) - want[n][1]) > 0.05:
                raise SystemExit(f"{part['ref']}.{n} fora do furo {h}")
            if nn:
                p.SetNet(net(nn))
    return fp

def new_fp(ref, value, x, y):
    fp = pcbnew.FOOTPRINT(board)
    board.Add(fp)
    fp.SetReference(ref)
    fp.SetValue(value)
    fp.SetPosition(V(x, y))
    fp.Reference().SetLayer(pcbnew.F_Fab)
    fp.Value().SetLayer(pcbnew.F_Fab)
    fp.Value().SetVisible(False)
    fp.Reference().SetPosition(V(x, y))
    return fp

def add_pad(fp, num, x, y, nn, shape="circle", size=1.7, drill=1.0):
    p = pcbnew.PAD(fp)
    p.SetNumber(num)
    p.SetAttribute(pcbnew.PAD_ATTRIB_PTH)
    p.SetShape(pcbnew.PAD_SHAPE_RECT if shape == "rect" else pcbnew.PAD_SHAPE_CIRCLE)
    p.SetSize(V(size, size))
    p.SetDrillSize(V(drill, drill))
    p.SetLayerSet(pcbnew.PAD.PTHMask())
    p.SetPosition(V(x, y))
    fp.Add(p)
    if nn:
        p.SetNet(net(nn))
    return p

for part in D.PARTS:
    ref = part["ref"]
    if part["lib"]:
        fp = place_lib(part)
        fp.SetReference(ref)
        fp.SetValue(part["value"])
        fp.Reference().SetVisible(False)
        fp.Value().SetVisible(False)
        continue
    first = list(part["pads"].values())[0][0]
    fp = new_fp(ref, part["value"], *D.xy(first))
    for n, (h, nn) in part["pads"].items():
        add_pad(fp, n, *D.xy(h), nn, "rect" if n == "1" else "circle")
    if part["kind"] == "pot":
        px, py = D.xy("J4")
        fp.Reference().SetPosition(V(px, py + 5.0))
    elif part["kind"] == "led":
        cx, cy = g(19.5, 7)
        circ(pcbnew.F_Fab, cx, cy, 2.5, 0.15, parent=fp)
        circ(pcbnew.F_SilkS, cx, cy, 2.95, 0.15, parent=fp)
        fp.Reference().SetPosition(V(cx, cy))
    elif part["kind"] == "sw":
        cx, cy = g(26.5, 7)
        for layer in (pcbnew.F_Fab, pcbnew.F_SilkS):
            rect(layer, cx - 3, cy - 3, cx + 3, cy + 3, 0.15, parent=fp)
        circ(pcbnew.F_Fab, cx, cy, 1.75, 0.15, parent=fp)
        fp.Reference().SetPosition(V(cx, cy))

x1, y1 = g(14.5, 1.5)
x2, y2 = g(34.5, 3.5)
rect(pcbnew.F_Fab, x1, y1, x2, y2, 0.2)
text(pcbnew.F_Fab, "J1: 40 pinos machos por cima (barra de pinos longos)", *g(24.5, 0.35), 0.9)

for ref, nn, a, b, ylev in D.JUMPERS:
    (xa, ya), (xb, yb) = D.xy(a), D.xy(b)
    fp = new_fp(ref, "fio encapado (lado cobre)", xa, ya)
    fp.SetDuplicatePadNumbersAreJumpers(True)
    add_pad(fp, "1", xa, ya, nn)
    add_pad(fp, "1", xb, yb, nn)
    fp.Reference().SetVisible(False)
    poly(pcbnew.B_Fab, [(xa, ya), (xa, ylev), (xb, ylev), (xb, yb)], 0.5, parent=fp)
    text(pcbnew.B_Fab, ref, xb + 0.9, yb - 1.1, 0.8, mirror=True, parent=fp)

SHORT = {"+5V_RPI": "5V Pi", "+5V_EXT": "5V ext", "+5V": "+5V", "GND": "GND", "+3V3": "3V3", "LED_A": "LED+",
         "GPIO4_LED_R": "GPIO4", "GPIO17_LED_G": "GPIO17", "GPIO27_LED_B": "GPIO27", "GPIO22_DHT": "GPIO22",
         "GPIO23_TRIG": "GPIO23", "GPIO24_ECHO": "GPIO24", "GPIO25_POT_CARGA": "GPIO25", "GPIO12_POT_LEIT": "GPIO12",
         "GPIO5_BOTAO": "GPIO5", "GPIO6_BUZZER": "GPIO6", "GPIO13_SERVO1": "GPIO13", "GPIO26_SERVO2": "GPIO26",
         "ECHO_5V": "ECHO 5V", "Q1_BASE": "base", "BUZ_NEG": "buzz-", "POT_X": "POT_X", "POT_1": "POT1"}
for nn, paths in D.TRACKS.items():
    w = 1.2 if nn in D.POWER_NETS else 0.9
    for pth in paths:
        for a, b in zip(pth, pth[1:]):
            t = pcbnew.PCB_TRACK(board)
            t.SetStart(V(*D.xy(a))); t.SetEnd(V(*D.xy(b)))
            t.SetWidth(mm(w)); t.SetLayer(pcbnew.B_Cu); t.SetNet(net(nn))
            board.Add(t)
        best, i = None, 0
        while i < len(pth) - 1:
            j = i + 1
            (c0, r0), (c1, r1) = D.rc(pth[i]), D.rc(pth[j])
            dc, dr = c1 - c0, r1 - r0
            while j + 1 < len(pth) and (D.rc(pth[j + 1])[0] - D.rc(pth[j])[0], D.rc(pth[j + 1])[1] - D.rc(pth[j])[1]) == (dc, dr):
                j += 1
            if best is None or j - i > best[1] - best[0]:
                best = (i, j, dc != 0)
            i = j
        i, j, horiz = best
        if j - i < 2:
            continue
        (xa, ya), (xb, yb) = D.xy(pth[i]), D.xy(pth[j])
        xm, ym = (xa + xb) / 2, (ya + yb) / 2
        if horiz:
            text(pcbnew.B_Fab, SHORT.get(nn, nn), xm, ym + 1.27, 0.75, mirror=True)
        else:
            text(pcbnew.B_Fab, SHORT.get(nn, nn), xm + 1.27, ym, 0.75, angle=90, mirror=True)

LX, LY, LW, LH = D.LABEL_X, D.LABEL_Y, D.LABEL_W, D.LABEL_H
rect(L_LABEL_EDGE, LX, D.BOARD_Y, LX + LW, D.SEAM_Y, 0.1)
rect(L_LABEL_EDGE, LX, D.SEAM_Y, LX + LW, D.BOARD_Y + D.BOARD_H, 0.1)

def in_label(x, y, m=0.6):
    return LX + m <= x <= LX + LW - m and D.BOARD_Y + m <= y <= D.BOARD_Y + D.BOARD_H - m

def grow(x, y):
    """posição fracionária da grade a partir de mm"""
    return (x - D.X0) / D.PITCH + 1, (y - D.Y0) / D.PITCH + 1

TEXTBOXES = []

def T(s, c, r, h=0.6, angle=0, just="c", bold=False):
    x, y = g(c, r)
    text(L_LABEL, s, x, y, h, angle, just, bold)
    w = len(s) * 0.8 * h + 0.3
    x0 = {"c": x - w / 2, "l": x, "r": x - w}[just]
    box = (x0, y - h / 2 - 0.25, x0 + w, y + h / 2 + 0.25)
    if angle in (90, 270):
        box = (x - h / 2 - 0.25, y - w / 2, x + h / 2 + 0.25, y + w / 2)
    TEXTBOXES.append(box)

for n in range(1, 41):
    c, r = D.rc(D.pi_hole(n))
    s = D.PI_POWER.get(n) or str(D.PI_BCM[n])
    used = D.PI_PIN_NET.get(n, "").startswith("GPIO")
    T(s, c, 1.15 if n % 2 == 0 else 3.85, 0.92, bold=used)
T("1", 14.3, 3, 0.9, bold=True); T("2", 14.3, 2, 0.9, bold=True)
T("39", 34.55, 3, 0.9, just="l", bold=True); T("40", 34.55, 2, 0.9, just="l", bold=True)
c0, r0 = grow(164.0, 102.05)
T("RASPBERRY PI (J1): números = GPIO BCM · negrito = usado nesta placa", c0, r0, 0.92, bold=True)
c0, r0 = grow(164.0, 103.75)
T("Livres p/ comunicação: I2C 2,3 · UART 14,15 · SPI0 7,8,9,10,11", c0, r0, 0.8)
c0, r0 = grow(164.0, 105.3)
T("SPI1/I2S 16,18,19,20,21 · ID 0,1 (reservado, não usar)", c0, r0, 0.8)

T("EXT", 11, 2.8, 0.7); T("5V", 12, 2.8, 0.7); T("RPi", 13, 2.8, 0.7)
T("JP1", 10.35, 2, 0.85, just="r", bold=True)
T("GND−  J7  +5V", 3, 4.62, 0.82, bold=True)
T("C2 470µ 25V", 15, 10.5, 0.72, bold=True)

T("C1 100n", 2, 8.0, 0.72)
T("R2 10k", 4, 7.5, 0.78, angle=90); T("R1 10k", 6, 7.5, 0.78, angle=90)
T("G12", 4, 5.4, 0.72, bold=True); T("G25", 6, 5.4, 0.72, bold=True)
for c, s in ((2, "3"), (4, "2"), (6, "1")):
    T(s, c - 0.45, 10.0, 0.72, just="r")
T("RV1 10k", 4, 12.1, 0.85, bold=True)
px, py = D.xy("J4")
sy = py + 2.7
for layer in (L_LABEL, pcbnew.F_Fab):
    rect(layer, px - 2.6, sy - 0.75, px + 2.6, sy + 0.75, 0.13)
    poly(layer, [(px - 2.6, sy), (px - 5.08, sy), (px - 5.08, py + 0.75)], 0.13)
    poly(layer, [(px + 2.6, sy), (px + 5.08, sy), (px + 5.08, py + 0.75)], 0.13)
    seg(layer, px, py + 0.75, px, sy - 0.8, 0.13)
    poly(layer, [(px - 0.45, sy - 1.45), (px, sy - 0.8), (px + 0.45, sy - 1.45)], 0.13)

T("R4 330", 7, 10.5, 0.78, angle=90); T("R3 330", 9, 10.5, 0.78, angle=90)
T("J4 HC-SR04", 11.6, 8.5, 0.8, bold=True)
T("TRIG=G23  ECHO=G24", 11.6, 9.3, 0.6)
for r, s in ((10, "VCC"), (11, "TRIG"), (12, "ECHO"), (13, "GND")):
    T(s, 11.6, r, 0.72, just="l")

T("R5 330", 17, 5, 0.78)
T("D1 RGB", 19.5, 5.52, 0.68, bold=True)
for c, s in ((18, "R"), (19, "+"), (20, "G"), (21, "B")):
    T(s, c, 7.65, 0.7, bold=True)
T("R=G4  G=G17  B=G27", 19.5, 8.5, 0.68)

c0, r0 = grow(150.0, 146.6)
T("Placa de interface Raspberry Pi · etiqueta A (em cima) + B (embaixo)", c0, r0, 0.85, bold=True)

T("J5 DHT11 G22", 23.4, 4.95, 0.68, bold=True)
for r, s in ((6, "3V3"), (7, "DAT"), (8, "GND")):
    T(s, 23.45, r, 0.68, just="r")

T("GND", 26.3, 5, 0.68, just="r"); T("BTN · J8 botão G5", 28.8, 5, 0.72, just="l", bold=True)
T("SW1", 26.5, 7, 1.0, bold=True)
xa, ya = D.xy("F28"); xb, yb = D.xy("H25")
seg(L_LABEL, xa - 0.5, ya + 0.35, xb + 0.5, yb - 0.35, 0.12)

T("R6 1k", 28, 10, 0.78)
T("BUZZER G6", 23, 11.05, 0.68, bold=True)
for c, s in ((22, "5V"), (23, "nc"), (24, "Q1")):
    T(s, c, 12.62, 0.68)
for c, s in ((25, "C"), (26, "B"), (27, "E")):
    T(s, c, 12.62, 0.68, bold=True)
T("Q1 BC337", 28.15, 12, 0.72, just="l", bold=True)

for c, name, gp in ((31, "SERVO1", "G13"), (33, "SERVO2", "G26")):
    T(gp, c, 10.45, 0.72, bold=True)
    T(name, c, 11.05, 0.68, bold=True)
    for r, s in ((12, "S"), (13, "+"), (14, "−")):
        T(s, c + 0.6, r, 0.8, just="l", bold=True)

pierce = set()
for part in D.PARTS:
    for n, (h, nn) in part["pads"].items():
        pierce.add(h)
for c in range(1, D.NCOLS + 1):
    for r in range(1, D.NROWS + 1):
        h = D.hole(c, r)
        x, y = D.xy(h)
        if not in_label(x, y):
            continue
        if h in pierce:
            circ(L_LABEL, x, y, 0.62, 0.12)
            circ(L_LABEL, x, y, 0.12, 0.1, fill=True)

cxm, cym = D.BOARD_X + D.BOARD_W / 2, D.BOARD_Y + D.BOARD_H / 2
y_top, y_bot = D.BOARD_Y, D.BOARD_Y + D.BOARD_H
for x1, y1, x2, y2 in ((cxm, y_top, cxm, y_top + 0.8), (cxm, D.SEAM_Y, cxm, D.SEAM_Y - 1.2),
                       (cxm, D.SEAM_Y, cxm, D.SEAM_Y + 1.2), (cxm, y_bot, cxm, y_bot - 1.5),
                       (LX, cym, LX + 2.2, cym), (LX + LW, cym, LX + LW - 2.2, cym)):
    seg(L_LABEL, x1, y1, x2, y2, 0.2)
for x, just in ((LX + 2.5, "l"), (LX + LW - 2.5, "r")):
    text(L_LABEL, "centro", x, cym, 0.8, 0, just)
for cx, cy in ((bx + 5.5, by + 5.0), (bx + bw - 5.5, by + 5.0), (bx + 5.5, by + bh - 5.0), (bx + bw - 5.5, by + bh - 5.0)):
    circ(L_LABEL, cx, cy, 1.5, 0.12)
_tg = [D.xy(h) for h in pierce]
for i, b1 in enumerate(TEXTBOXES):
    for b2 in TEXTBOXES[i + 1:]:
        if b1[0] < b2[2] and b2[0] < b1[2] and b1[1] < b2[3] and b2[1] < b1[3]:
            print("AVISO: textos sobrepostos em x=%.1f y=%.1f" % (b1[0], b1[1]))
    for (x, y) in _tg:
        if b1[0] - 0.45 < x < b1[2] + 0.45 and b1[1] - 0.45 < y < b1[3] + 0.45:
            print("AVISO: texto sobre furo em (%.1f,%.1f) caixa x=%.1f..%.1f y=%.1f..%.1f" % (x, y, *b1))
for b in TEXTBOXES:
    if b[1] < D.SEAM_Y + 0.2 and b[3] > D.SEAM_Y - 0.2:
        print("AVISO: texto sobre a emenda A/B em y=%.1f..%.1f x=%.1f" % (b[1], b[3], b[0]))

pcb_path = os.path.join(OUT, NAME + ".kicad_pcb")
pcbnew.SaveBoard(pcb_path, board)

txt = open(pcb_path, encoding="utf-8").read()
i = txt.index('(property "Reference" "J1"')
k = txt.index("(duplicate_pad_numbers_are_jumpers", i)
e = txt.index("\n", k)
groups = " ".join("(" + " ".join(f'"{n}"' for n in grp) + ")" for grp in D.PI_JUMPER_GROUPS)
txt = txt[:e + 1] + f"\t\t(jumper_pad_groups {groups})\n" + txt[e + 1:]
open(pcb_path, "w", encoding="utf-8").write(txt)

pro = {
    "board": {"design_settings": {
        "rule_severities": {"silk_over_copper": "ignore", "silk_overlap": "ignore", "silk_edge_clearance": "ignore",
                            "lib_footprint_issues": "ignore", "lib_footprint_mismatch": "ignore",
                            "courtyards_overlap": "warning", "missing_courtyard": "ignore",
                            "text_height": "ignore", "text_thickness": "ignore"},
        "rules": {"min_clearance": 0.2, "min_track_width": 0.2},
    }},
    "meta": {"filename": NAME + ".kicad_pro", "version": 3},
}
json.dump(pro, open(os.path.join(OUT, NAME + ".kicad_pro"), "w", encoding="utf-8"), indent=2)
print("ok:", pcb_path, len(board.GetFootprints()), "footprints,", len(board.GetTracks()), "trilhas")
