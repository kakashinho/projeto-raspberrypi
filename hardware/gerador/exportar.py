"""Exporta as vistas do KiCad e monta: folha PIMACO 6282 e PDF de montagem.
Uso: python exportar.py <pasta_com_placa_interface.kicad_pcb>   (precisa de PyMuPDF)
"""
import os
import sys
import subprocess
import pymupdf
import design as D

OUT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "out")
PCB = os.path.join(OUT, "placa_interface.kicad_pcb")
CLI = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
K = 72 / 25.4

def kpdf(name, layers, *extra):
    path = os.path.join(OUT, name)
    subprocess.run([CLI, "pcb", "export", "pdf", "--mode-single", "-l", layers, *extra, "-o", path, PCB],
                   check=True, capture_output=True)
    return path

label_src = kpdf("_etiqueta.pdf", "User.3,F.SilkS", "--black-and-white", "--drill-shape-opt", "0")
top_src = kpdf("_top.pdf", "Edge.Cuts,User.1,F.Cu,F.Fab,F.SilkS,User.3", "--drill-shape-opt", "0")
bot_src = kpdf("_bottom.pdf", "Edge.Cuts,User.2,User.1,B.Cu,B.Fab,B.SilkS", "--mirror", "--drill-shape-opt", "0")
thru_src = kpdf("_thru.pdf", "Edge.Cuts,User.2,User.1,B.Cu,F.Fab", "--drill-shape-opt", "0")

LBL_A = pymupdf.Rect(D.LABEL_X * K, D.BOARD_Y * K, (D.LABEL_X + D.LABEL_W) * K, D.SEAM_Y * K)
LBL_B = pymupdf.Rect(D.LABEL_X * K, D.SEAM_Y * K, (D.LABEL_X + D.LABEL_W) * K, (D.BOARD_Y + D.BOARD_H) * K)
LBL = pymupdf.Rect(D.LABEL_X * K, D.BOARD_Y * K, (D.LABEL_X + D.LABEL_W) * K, (D.BOARD_Y + D.BOARD_H) * K)

SHEET_W, SHEET_H = 215.9, 279.4
TOP, LEFT, LW, LH = 21.2, 4.0, 101.6, 33.9
GAP = SHEET_W - 2 * LEFT - 2 * LW

def slot(i, j):
    x, y = LEFT + j * (LW + GAP), TOP + i * LH
    return pymupdf.Rect(x * K, y * K, (x + LW) * K, (y + LH) * K)

src = pymupdf.open(label_src)

def sheet(fname, positions, outlines=False, note=None):
    """positions: {(linha, coluna): 'A' ou 'B'}"""
    doc = pymupdf.open()
    pg = doc.new_page(width=SHEET_W * K, height=SHEET_H * K)
    for i in range(7):
        for j in range(2):
            r = slot(i, j)
            kind = positions.get((i, j))
            if kind == "A":
                pg.show_pdf_page(r, src, 0, clip=LBL_A)
            elif kind == "B":
                hb = D.LABEL_B_H * K
                pg.show_pdf_page(pymupdf.Rect(r.x0, r.y0, r.x1, r.y0 + hb), src, 0, clip=LBL_B)
                pg.draw_line((r.x0, r.y0 + hb), (r.x1, r.y0 + hb), color=(0, 0, 0), width=0.5, dashes="[3 2] 0")
                pg.insert_text((r.x0 + 3 * K, r.y0 + hb + 5 * K),
                               "B (base) - CORTE na linha tracejada e descarte esta parte.", fontsize=7)
                pg.insert_text((r.x0 + 3 * K, r.y0 + hb + 9 * K),
                               "Cole com a linha cortada encostada na etiqueta A e a outra borda na borda de baixo da placa.",
                               fontsize=6)
            if outlines:
                pg.draw_rect(r, color=(0.6, 0.6, 0.6), width=0.4)
    if note:
        pg.insert_text((LEFT * K, (TOP - 6) * K), note, fontsize=8, color=(0.3, 0.3, 0.3))
    doc.save(os.path.join(OUT, fname))
    return doc

sheet("etiquetas_A_B_pimaco6282.pdf", {(1, 0): "A", (1, 1): "B"})
sheet("etiquetas_A_B_folha_cheia.pdf", {(i, j): "AB"[j] for i in range(7) for j in range(2)})
sheet("etiquetas_teste_papel_comum.pdf", {(1, 0): "A", (1, 1): "B"}, outlines=True,
      note="TESTE: imprima em papel comum a 100% (tamanho real), sobreponha à folha PIMACO 6282 contra a luz e confira o alinhamento.")

A4W, A4H = 297 * K, 210 * K
OPEN = {}
mont = pymupdf.open()
BOARD = pymupdf.Rect(97 * K, 99 * K, 203 * K, 151 * K)

def page_with(src_path, clip, title, lines):
    pg = mont.new_page(width=A4W, height=A4H)
    pg.insert_text((14 * K, 14 * K), title, fontsize=15, fontname="hebo")
    y = 20 * K
    for ln in lines:
        pg.insert_text((14 * K, y), ln, fontsize=8.5)
        y += 4.2 * K
    s = OPEN.setdefault(src_path, pymupdf.open(src_path))
    target = pymupdf.Rect(14 * K, y + 2 * K, A4W - 14 * K, A4H - 8 * K)
    pg.show_pdf_page(target, s, 0, clip=clip, keep_proportion=True)
    return pg

page_with(top_src, BOARD, "1) Lado dos componentes (visto de cima)",
          ["Coordenadas: colunas 1-34 e fileiras A-O, iguais às da etiqueta. J1 = barra fêmea 2x20 de PINOS LONGOS: o corpo fica por baixo (encaixa no Pi)",
           "e os 40 pinos machos saem por cima, na mesma ordem do Raspberry (pino 1 = C15). Placa por cima do Pi; colunas 1-14 ficam em balanço.",
           "JP1: jumper em RPi|5V = cargas no 5V do Raspberry; jumper em 5V|EXT = cargas na fonte do borne J7. Nunca os dois. C2 fica em paralelo com o 5V escolhido.",
           "Ilhas vermelhas sem componente (A22, A23, A25, A30, E4, E6, H8, K10) = pontas dos fios W1-W4, soldados pelo lado do cobre (ver página 2)."])
bot_doc = pymupdf.open(bot_src)
bb = None
for dr in bot_doc[0].get_drawings():
    bb = dr["rect"] if bb is None else bb | dr["rect"]
page_with(bot_src, pymupdf.Rect(bb.x0 - 2 * K, bb.y0 - 1 * K, bb.x1 + 2 * K, bb.y1 + 1 * K),
          "2) Lado do cobre (placa virada como página de livro: coluna 1 à direita)",
          ["Trilhas azuis = pontes de solda / fio estanhado. Linhas cinzas W1-W4 = fios ENCAPADOS por este lado (do furo da fileira A até o destino, rente à borda).",
           "Retângulo J1 = corpo da barra 2x20: solde com o plástico afastado ~3 mm da placa (os pinos longos atravessam e sobram por cima).",
           "Barramentos: fileira M = +5V (saída do JP1), fileira N = GND. Fileira O e tiras de cobre da borda: não usadas."])

pg = mont.new_page(width=A4W, height=A4H)
pg.insert_text((14 * K, 14 * K), "3) Etiquetas A + B PIMACO 6282 (ampliadas; imprima o arquivo das etiquetas em tamanho real)", fontsize=14, fontname="hebo")
for k, ln in enumerate(["Etiqueta A: borda de cima encostada na borda da placa do lado do J1, centralizada pelo risco de 50 mm (marca de centro).",
                        "Etiqueta B: corte na linha tracejada, encoste o corte na etiqueta A (emenda entre as fileiras K e L) e a outra borda na borda de baixo.",
                        "Fure só os círculos (terminais e os 40 pinos do J1), de baixo para cima, pelos furos. As etiquetas têm 101,6 mm: apare 0,8 mm de cada lado."]):
    pg.insert_text((14 * K, (20 + 4.2 * k) * K), ln, fontsize=8.5)
tgt = pymupdf.Rect(14 * K, 36 * K, A4W - 14 * K, A4H - 10 * K)
pg.show_pdf_page(tgt, src, 0, clip=LBL)
sc = min(tgt.width / LBL.width, tgt.height / LBL.height)
x0 = tgt.x0 + (tgt.width - LBL.width * sc) / 2
ys = tgt.y0 + (tgt.height - LBL.height * sc) / 2 + (LBL_A.height * sc)
pg.draw_line((x0, ys), (x0 + LBL.width * sc, ys), color=(0.85, 0.1, 0.1), width=1, dashes="[4 3] 0")
pg.insert_text((x0 + LBL.width * sc - 40, ys - 3), "emenda A/B", fontsize=7, color=(0.85, 0.1, 0.1))

pg = mont.new_page(width=A4W, height=A4H)
pg.insert_text((14 * K, 14 * K), "4) Lista de montagem", fontsize=15, fontname="hebo")
lines = ["COMPONENTES (furos no lado dos componentes):"]
for p in D.PARTS:
    pads = ", ".join(f"{n}:{h}" + (f" {nn}" if nn and p['ref'] != 'J1' else "") for n, (h, nn) in p["pads"].items()) \
        if p["ref"] != "J1" else "pino 1 = C15, pino 2 = B15 ... pino 39 = C34, pino 40 = B34 (lado cobre)"
    lines.append(f"  {p['ref']:<4} {p['value']:<30} {pads}")
lines.append("")
lines.append("FIOS ENCAPADOS pelo lado do cobre (passe rente à borda de cima):")
for ref, nn, a, b, _ in D.JUMPERS:
    lines.append(f"  {ref}: {a} -> {b}   ({nn})")
lines.append("")
lines.append("PONTES no lado cobre (cada sequência = ilhas unidas em linha reta, na ordem):")
for nn, paths in D.TRACKS.items():
    for pth in paths:
        corners = [pth[0]]
        for a, b, c in zip(pth, pth[1:], pth[2:]):
            (ca, ra), (cb, rb), (cc, rcc) = D.rc(a), D.rc(b), D.rc(c)
            if (cb - ca, rb - ra) != (cc - cb, rcc - rb):
                corners.append(b)
        corners.append(pth[-1])
        lines.append(f"  {nn:<17} " + " - ".join(corners))
y = 22 * K
col_x = 14 * K
for ln in lines:
    if y > A4H - 10 * K:
        y = 22 * K
        col_x += 178 * K
    pg.insert_text((col_x, y), ln, fontsize=6.6, fontname="cour")
    y += 3.05 * K
mont.save(os.path.join(OUT, "montagem_placa_interface.pdf"))

tr = pymupdf.open()
pg = tr.new_page(width=210 * K, height=297 * K)
pg.insert_text((14 * K, 14 * K), "Trilhas em TAMANHO REAL (1:1) - placa 100 x 50 mm", fontsize=14, fontname="hebo")
for k, ln in enumerate(["Imprima em 100% / 'Tamanho real' (desmarque 'Ajustar à página'). Confira a régua de 50 mm com uma régua de verdade.",
                        "Azul = pontes de solda / fio estanhado ligando ilhas vizinhas. Cinza escuro (W1-W4) = fios encapados pelo lado do cobre.",
                        "Vire a placa com o cobre para cima e apoie sobre a vista 1: cada furo deve cair sobre um círculo do desenho."]):
    pg.insert_text((14 * K, (20 + 4.2 * k) * K), ln, fontsize=8)
BW, BH = D.BOARD_W, D.BOARD_H
X0P = (210 - BW) / 2

def place_1x1(src_path, x0_src, title, ytop):
    pg.insert_text((X0P * K, (ytop - 2) * K), title, fontsize=9.5, fontname="hebo")
    s = OPEN.setdefault(src_path, pymupdf.open(src_path))
    clip = pymupdf.Rect(x0_src * K, D.BOARD_Y * K, (x0_src + BW) * K, (D.BOARD_Y + BH) * K)
    pg.show_pdf_page(pymupdf.Rect(X0P * K, ytop * K, (X0P + BW) * K, (ytop + BH) * K), s, 0, clip=clip, keep_proportion=False)
    pg.draw_rect(pymupdf.Rect(X0P * K, ytop * K, (X0P + BW) * K, (ytop + BH) * K), color=(0, 0, 0), width=0.6)

def ruler(y):
    x0 = X0P
    pg.draw_line((x0 * K, y * K), ((x0 + 50) * K, y * K), color=(0, 0, 0), width=0.8)
    for i in range(0, 51, 10):
        h = 2.0 if i % 50 == 0 else 1.2
        pg.draw_line(((x0 + i) * K, (y - h) * K), ((x0 + i) * K, y * K), color=(0, 0, 0), width=0.6)
    pg.insert_text(((x0 + 52) * K, (y + 1) * K), "50 mm  (se não medir 50 mm, a impressão foi reduzida)", fontsize=7.5)

page_w = 297.0
place_1x1(bot_src, page_w - (D.BOARD_X + BW), "1) LADO DO COBRE - placa virada como página de livro (coluna 1 à direita)", 40)
ruler(97)
place_1x1(thru_src, D.BOARD_X, "2) Mesmas trilhas vistas POR CIMA (como se a placa fosse transparente) - igual à etiqueta", 112)
ruler(169)
y = 180
pg.insert_text((14 * K, y * K), "Fios encapados (lado do cobre, rente à borda de cima):", fontsize=8.5, fontname="hebo")
for ref, nn, a, b, _ in D.JUMPERS:
    y += 4.2
    pg.insert_text((18 * K, y * K), f"{ref}: ilha {a}  ->  ilha {b}    ({nn})", fontsize=8)
y += 7
pg.insert_text((14 * K, y * K), "Ordem sugerida:", fontsize=8.5, fontname="hebo")
for ln in ("1. Barramentos: GND (coluna 1 e fileira N, colunas 34 e 27) e +5V (coluna 12 e fileira M).",
           "2. Trilhas curtas de cada bloco (LED, DHT, botão, buzzer, servos, pot, HC-SR04).",
           "3. Pontes das fileiras A e D até os pinos do J1 (antes de soldar a barra 2x20).",
           "4. Barra 2x20 de pinos longos (corpo ~3 mm afastado da placa) e depois os fios W1-W4.",
           "5. Teste de continuidade: nenhum curto entre +5V, 3V3 e GND; 5V do Pi e 5V externo só se ligam pelo JP1."):
    y += 4.2
    pg.insert_text((18 * K, y * K), ln, fontsize=8)
tr.save(os.path.join(OUT, "trilhas_tamanho_real_A4.pdf"))
tr[0].get_pixmap(dpi=110).save(os.path.join(OUT, "previa_trilhas.png"))
tr.close()

for name, doc_path, pno in (("previa_montagem_p1.png", "montagem_placa_interface.pdf", 0),
                            ("previa_montagem_p2.png", "montagem_placa_interface.pdf", 1),
                            ("previa_etiqueta.png", "montagem_placa_interface.pdf", 2),
                            ("previa_lista.png", "montagem_placa_interface.pdf", 3),
                            ("previa_folha.png", "etiquetas_A_B_pimaco6282.pdf", 0)):
    d = pymupdf.open(os.path.join(OUT, doc_path))
    d[pno].get_pixmap(dpi=130).save(os.path.join(OUT, name))
src.close()
bot_doc.close()
for d_ in OPEN.values():
    d_.close()
mont.close()
import gc
gc.collect()
for f in ("_etiqueta.pdf", "_top.pdf", "_bottom.pdf", "_thru.pdf"):
    os.remove(os.path.join(OUT, f))
print("ok")
