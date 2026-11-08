# -*- coding: utf-8 -*-
"""Etiquetas PIMACO 6282 (faixas, setas, escritas, números, listras das cancelas) e adesivos A4
coloridos (fachadas e telhado da guarita, totem, grama, botão do pot e os 8 carros).

Uso:  python -B gerar_adesivos.py ../impressao
"""
import math
import os
import sys

import pymupdf

import design as d
from folha import A4, CINZA, MARGEM, PRETO, VERMELHO, Folha

BRANCO = (1, 1, 1)


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def escurecer(c, f=0.75):
    return tuple(max(0.0, v * f) for v in c)


def corte(F, pts, w=0.15):
    """Linha de corte do adesivo (fina, cinza escuro)."""
    F.poly(pts, (0.25, 0.25, 0.25), None, w)


def recortar(F, pts=None, circ=None):
    """Parte a recortar do adesivo (tracejado vermelho)."""
    if circ:
        F.circ(circ[0], circ[1], circ[2], VERMELHO, None, 0.25, dashes="[1 0.7] 0")
    else:
        F.poly(pts, VERMELHO, None, 0.25, dashes="[1 0.7] 0")


def R(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


# ================================================================ PIMACO 6282
P = d.PIMACO
LW, LH = P["etiqueta"]
GAP = P["folha"][0] - 2 * P["margem_lat"] - 2 * LW


def celula(k):
    i, j = divmod(k, 2)
    return P["margem_lat"] + j * (LW + GAP), P["margem_sup"] + i * LH


def faixa_etiqueta(F, x, y, comp, cod):
    corte(F, R(x, y, x + comp, y + d.FAIXA))
    F.texto(x + comp + 1.0, y + 3.2, cod, 1.7, CINZA)


def seta_etiqueta(F, x, y, comp, larg, cod):
    pts = d.seta_pts(0, 0, 0, comp, larg)
    corte(F, [(x + comp / 2 + px, y + larg / 2 - py) for px, py in pts])
    F.texto(x + comp + 1.5, y + larg / 2 + 1, cod, 1.7, CINZA)


def preto_com_texto(F, x, y, w, h, txt, tam):
    F.ret(x, y, x + w, y + h, cor=PRETO, fill=PRETO, w=0.1)
    F.texto(x + w / 2, y + h / 2 + tam * 0.48, txt, tam, BRANCO, negrito=True, ancora="c")


def listra_cancela(F, x, y, pivo_direita, comp=None):
    """Adesivo do braço da cancela: blocos vermelhos e brancos a partir da ponta; o lado do eixo fica branco."""
    comp, h = (comp or d.BRACO_E + d.BRACO_ATRAS), d.BRACO_W
    livre = d.BRACO_ATRAS + 8.0            # atrás do eixo + braço plástico do servo
    k = 0
    a = 0.0
    while a < comp - livre:
        b = min(a + 7.0, comp - livre)
        if k % 2 == 0:
            xa, xb = (x + a, x + b) if pivo_direita else (x + comp - b, x + comp - a)
            F.ret(xa, y, xb, y + h, cor=None, fill=(0.85, 0.1, 0.12), w=0)
        a = b
        k += 1
    xp = x + comp - d.BRACO_ATRAS if pivo_direita else x + d.BRACO_ATRAS
    F.circ(xp, y + h / 2, 0.8, PRETO, PRETO, 0.1)
    corte(F, R(x, y, x + comp, y + h))


def etiquetas(saida, teste=False):
    doc = pymupdf.open()
    F = Folha(doc, *P["folha"])
    marcas = {cod: (tipo, dado) for cod, tipo, dado in d.marcas_piso()}

    def comp(cod):
        x0, y0, x1, y1 = marcas[cod][1]
        return max(x1 - x0, y1 - y0)

    linhas_faixas = [["M1", "M2", "C1", "C2", "F1"], ["F2", "F3", "V1", "V2", "V3"], ["V4", "V5", "V6", "V7", "V8"]]
    for k, linha in enumerate(linhas_faixas):
        cx, cy = celula(k)
        for r, cod in enumerate(linha):
            faixa_etiqueta(F, cx + 1.5, cy + 2.0 + r * 6.2, comp(cod), cod)
    # célula 3: setas + ENTRADA / SAÍDA
    cx, cy = celula(3)
    seta_etiqueta(F, cx + 2, cy + 2.5, 18, 8, "A1")
    seta_etiqueta(F, cx + 27, cy + 2.5, 18, 8, "A2")
    seta_etiqueta(F, cx + 52, cy + 3, 14, 7, "A3")
    seta_etiqueta(F, cx + 74, cy + 3, 14, 7, "A4")
    ew, eh = d.ESCRITA
    preto_com_texto(F, cx + 4, cy + 16, ew, eh, "ENTRADA", 3.6)
    F.texto(cx + 4 + ew + 1.5, cy + 20, "T1", 1.7, CINZA)
    preto_com_texto(F, cx + 48, cy + 16, ew, eh, "SAÍDA", 3.6)
    F.texto(cx + 48 + ew + 1.5, cy + 20, "T2", 1.7, CINZA)
    # célula 4: números das vagas
    cx, cy = celula(4)
    n = d.NUMERO
    for k in range(d.N_VAGAS):
        preto_com_texto(F, cx + 3 + k * (n + 4), cy + 4, n, n, str(k + 1), 5.0)
    F.texto(cx + 3, cy + 18, "N1 a N7: números das vagas (pretos, colam no asfalto em frente de cada vaga)", 1.8, CINZA)
    # células 5 e 6: listras das cancelas (frente e verso de cada braço)
    for k, pivo_dir in ((5, True), (6, False)):
        cx, cy = celula(k)
        for r in range(2):
            listra_cancela(F, cx + 3, cy + 3 + r * 13, pivo_dir)
        F.texto(cx + 3, cy + 31.5, "listras da cancela: ● = eixo do servo", 1.7, CINZA)
    # célula 7: faixas de reserva
    cx, cy = celula(7)
    for r in range(5):
        faixa_etiqueta(F, cx + 1.5, cy + 2.0 + r * 6.2, 85.0, "res.")
    if teste:
        for k in range(14):
            x, y = celula(k)
            F.ret(x, y, x + LW, y + LH, cor=(0.6, 0.6, 0.6), w=0.3)
        F.texto(P["margem_lat"] + 3, P["margem_sup"] - 6, "TESTE em papel comum: imprima a 100 % (papel CARTA), ponha sobre a "
                "folha PIMACO 6282 contra a luz e confira.", 2.4, CINZA)
    else:
        F.texto(P["margem_lat"] + 3, P["margem_sup"] - 6, "PIMACO 6282 (folha CARTA): imprimir a 100 %. Faixas brancas: corte "
                "pelas linhas finas. Códigos = gabarito do piso.", 2.4, CINZA)
    F.fim()
    nome = "etiquetas_pimaco6282_teste.pdf" if teste else "etiquetas_pimaco6282.pdf"
    destino = os.path.join(saida, nome)
    doc.subset_fonts()
    doc.save(destino, garbage=3, deflate=True)
    return destino


# ================================================================ adesivos A4
CREME = hexrgb("#ece4cf")
RODAPE = hexrgb("#7f7a6e")
FAIXA_TOPO = hexrgb("#2f5d62")
VIDRO = hexrgb("#2c3e50")
MOLDURA = hexrgb("#f7f3ea")
PAINEL = hexrgb("#3a3f47")


def janela(F, x0, y0, x1, y1):
    F.ret(x0 - 1, y0 - 1, x1 + 1, y1 + 1, cor=None, fill=MOLDURA, w=0)
    F.ret(x0, y0, x1, y1, cor=None, fill=VIDRO, w=0)
    F.linha((x0 + x1) / 2, y0, (x0 + x1) / 2, y1, MOLDURA, 0.6)
    F.linha(x0 + 1.5, y0 + 1.5, x0 + 5, y0 + 1.5, (0.6, 0.7, 0.8), 0.3)


def fachada_base(F, x, y, w, h, titulo=None):
    """Fundo da fachada: parede creme, rodapé e faixa de cima. (x, y) = canto de cima."""
    F.ret(x, y, x + w, y + h, cor=None, fill=CREME, w=0)
    F.ret(x, y + h - 5, x + w, y + h, cor=None, fill=RODAPE, w=0)
    F.ret(x, y, x + w, y + 6, cor=None, fill=FAIXA_TOPO, w=0)
    if titulo:
        F.texto(x + w / 2, y + 4.6, titulo, 3.6, BRANCO, negrito=True, ancora="c")


def adesivo_painel(F, x, y):
    """Fachada da parede da frente (G1), vista de fora. Z sobe; (x, y) = canto de cima."""
    gx = d.GUARITA_X1 - d.GUARITA_X0
    h = d.PAINEL_H
    gx0 = d.GUARITA_X0

    def p(a, z):
        return x + a, y + (h - z)

    fachada_base(F, x, y, gx, h, "GUARITA")
    # placa de controle em volta do pot e do LED
    xp = d.X(d.PECAS["RV1"][0]) - gx0
    lx0, lz0, lx1, lz1 = d.LED_JANELA
    a0, a1 = xp - 16, lx1 - gx0 + 13
    z0, z1 = 25.0, 55.0
    q0, q1 = p(a0, z1), p(a1, z0)
    F.ret(q0[0], q0[1], q1[0], q1[1], cor=None, fill=PAINEL, w=0)
    # escala do botão: 0° (fechada) a 90° (aberta)
    cx, cy = p(xp, d.POT_EIXO_Z)
    for k in range(0, 91, 15):
        ang = math.radians(180 - k * 2)          # 0° à esquerda, 90° em cima-direita (meia volta)
        r0, r1 = 6.5, 8.5 if k % 45 == 0 else 7.6
        F.linha(cx + r0 * math.cos(ang), cy - r0 * math.sin(ang), cx + r1 * math.cos(ang), cy - r1 * math.sin(ang),
                BRANCO, 0.35)
    F.texto(cx - 9.5, cy + 2.5, "0°", 1.8, BRANCO, ancora="d")
    F.texto(cx + 9.5, cy + 2.5, "90°", 1.8, BRANCO)
    F.texto(cx, cy + 10.5, "MANUAL", 2.4, BRANCO, negrito=True, ancora="c")
    recortar(F, circ=(cx, cy, (d.POT_TUBO_D + 1.0) / 2))
    # LED
    l0, l1 = p(lx0 - gx0, lz1), p(lx1 - gx0, lz0)
    F.ret(l0[0] - 0.8, l0[1] - 0.8, l1[0] + 0.8, l1[1] + 0.8, cor=None, fill=(0.1, 0.1, 0.1), w=0)
    recortar(F, R(l0[0], l0[1], l1[0], l1[1]))
    F.texto((l0[0] + l1[0]) / 2, l1[1] + 4.2, "STATUS", 2.4, BRANCO, negrito=True, ancora="c")
    for i, (cor, t) in enumerate((((0.2, 0.85, 0.3), "livre"), ((1.0, 0.8, 0.1), "abrindo"),
                                  ((0.95, 0.15, 0.15), "lotado"))):
        yy = l1[1] + 7.5 + i * 0
        xx = l0[0] - 8 + i * 10
        F.circ(xx, yy, 1.1, None, cor, 0)
        F.texto(xx + 1.6, yy + 0.7, t, 1.5, BRANCO)
    # janelas à direita
    for a in (110.0, 150.0):
        j0, j1 = p(a, 46), p(a + 30, 24)
        janela(F, j0[0], j0[1], j1[0], j1[1])
    # rasgo da energia (aberto embaixo)
    e0, e1 = p(d.ENERGIA_RASGO[0] - gx0, d.ENERGIA_RASGO[3]), p(d.ENERGIA_RASGO[2] - gx0, 0)
    recortar(F, [(e0[0], e1[1]), (e0[0], e0[1]), (e1[0], e0[1]), (e1[0], e1[1])])
    corte(F, R(x, y, x + gx, y + h))
    F.texto(x, y + h + 3.5, "G1 painel: cole na face de FORA. O papel cobre os recortes de cima; recorte o círculo e a",
            2.0, CINZA)
    F.texto(x, y + h + 6.3, "janela do LED (dobre o papel no meio deles e corte) e o recorte de baixo.", 2.0, CINZA)


def adesivo_fundo(F, x, y):
    gx = d.GUARITA_X1 - d.GUARITA_X0
    h = d.GUARITA_H
    fachada_base(F, x, y, gx, h, "ESTACIONAMENTO")
    for a in (40.0, 80.0, 120.0):
        janela(F, x + a, y + 16, x + a + 28, y + 36)
    # furos dos servos (vista de fora: espelhado, mas é simétrico)
    for sx0 in (d.SERVO_E_X0, d.SERVO_S_X0):
        cxs = d.GUARITA_X1 - (sx0 + d.SERVO_CORPO[0] / 2)        # visto de trás
        a0, a1 = cxs - d.SERVO_FURO[0] / 2, cxs + d.SERVO_FURO[0] / 2
        recortar(F, R(x + a0, y + h - d.SERVO_RECORTE_Z, x + a1, y + h))
    corte(F, R(x, y, x + gx, y + h))
    F.texto(x, y + h + 3.5, "G2 fundo: cole na face de FORA (lado das cancelas); corte os 2 recortes de baixo (servos).",
            2.0, CINZA)


def adesivo_lado(F, x, y, porta):
    gl = d.GUARITA_Y1 - d.GUARITA_Y0 - 2 * d.T
    h = d.GUARITA_H
    fachada_base(F, x, y, gl, h)
    if porta:
        F.ret(x + gl / 2 - 9, y + 16, x + gl / 2 + 9, y + h - 5, cor=None, fill=hexrgb("#7a5230"), w=0)
        F.circ(x + gl / 2 + 6, y + 38, 0.9, None, (0.9, 0.8, 0.3), 0)
    else:
        janela(F, x + 14, y + 18, x + gl - 14, y + 38)
    corte(F, R(x, y, x + gl, y + h))
    F.texto(x, y + h + 3.5, "G3 lateral" + (" (porta)" if porta else " (janela)"), 2.0, CINZA)


def adesivo_totem(F, x, y):
    L1 = d.TOTEM_L
    a0, a1 = 0.0, L1
    zb = d.US_Z + d.US_JANELA / 2
    h = d.TOTEM_H - zb
    F.ret(x, y, x + (a1 - a0), y + h, cor=None, fill=hexrgb("#e9c46a"), w=0)
    F.texto(x + (a1 - a0) / 2, y + h / 2 + 1.3, "SENSOR", 3.4, hexrgb("#3a2f0b"), negrito=True, ancora="c")
    corte(F, R(x, y, x + (a1 - a0), y + h))
    F.texto(x, y + h + 3.5, "S1 totem: faixa de cima (acima das janelas)", 2.0, CINZA)


def adesivo_botao(F, x, y):
    b = d.POT_BOTAO
    c = b * 0.29
    octo = [(x + c, y), (x + b - c, y), (x + b, y + c), (x + b, y + b - c), (x + b - c, y + b), (x + c, y + b),
            (x, y + b - c), (x, y + c)]
    F.poly(octo, None, hexrgb("#d23c3c"), 0)
    F.linha(x + b / 2, y + b / 2, x + b / 2, y + 2.2, BRANCO, 1.0)
    corte(F, octo)
    F.texto(x, y + b + 3.5, "K1 botão", 2.0, CINZA)


def adesivo_telhado(F, x, y):
    gx = d.GUARITA_X1 - d.GUARITA_X0 + 6
    gy = d.GUARITA_Y1 - d.GUARITA_Y0 + 6
    F.ret(x, y, x + gx, y + gy, cor=None, fill=hexrgb("#80868f"), w=0)
    F.ret(x + 3, y + 3, x + gx - 3, y + gy - 3, cor=hexrgb("#9aa0a8"), fill=None, w=0.8)
    for k in range(8):
        F.linha(x + 12 + k * 4, y + 12, x + 12 + k * 4, y + 26, hexrgb("#5d636b"), 0.8)
    # placa P de estacionamento
    s = 34.0
    cx, cy = x + gx / 2, y + gy / 2
    F.ret(cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2, cor=BRANCO, fill=hexrgb("#1f5fbf"), w=1.2)
    F.texto(cx, cy + 9.5, "P", 26.0, BRANCO, negrito=True, ancora="c")
    corte(F, R(x, y, x + gx, y + gy))
    F.texto(x, y + gy + 3.5, "G4 telhado: cole por cima (as travas GT ficam por baixo).", 2.0, CINZA)


def adesivo_grama(F, x, y):
    w, h = d.ENTRADA_X0 - d.FAIXA, d.ILHA_Y1
    _, ry0, rx1, ry1 = d.US_RASGO
    contorno = [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y + h - ry0), (x + rx1, y + h - ry0),
                (x + rx1, y + h - ry1), (x, y + h - ry1)]
    F.poly(contorno, None, hexrgb("#5f9c4a"), 0)
    k = 0
    for gy in range(2, int(h) - 1, 3):
        for gxx in range(2 + (k % 2), int(w) - 1, 4):
            F.linha(x + gxx, y + gy + 1.2, x + gxx + 0.6, y + gy, hexrgb("#4a7e39"), 0.3)
        k += 1

    def p(X, Y):
        return x + X, y + (h - Y)

    F.ret(x, y + h - ry1, x + rx1, y + h - ry0, cor=None, fill=BRANCO, w=0)
    corte(F, contorno)
    F.texto(x, y + h + 3.5, "grama da ilha (frente embaixo; recorte do sensor na borda)", 2.0, CINZA)


# ---------------------------------------------------------------- carros
CARROS = [("#d62828", "vermelho"), ("#f2b705", "táxi"), ("#1f5fbf", "azul"), ("#efefef", "branco"),
          ("#f07d1a", "laranja"), ("#2a9d63", "verde"), ("#7b4fc9", "roxo"), ("#9aa3ad", "prata")]


def carro_teto(F, x, y, cor, taxi=False):
    """Teto (24 x 50), frente em cima."""
    W, L = d.CARRO_W, d.CARRO_L
    F.ret(x, y, x + W, y + L, cor=None, fill=cor, w=0)
    esc = escurecer(cor, 0.82)
    F.ret(x + 2.5, y + L - 38, x + W - 2.5, y + L - 15, cor=None, fill=esc, w=0)          # teto
    F.poly([(x + 2.0, y + L - 38), (x + W - 2.0, y + L - 38), (x + W - 3.5, y + L - 31), (x + 3.5, y + L - 31)],
           None, VIDRO, 0)                                                                # para-brisa
    F.poly([(x + 3.0, y + L - 15), (x + W - 3.0, y + L - 15), (x + W - 2.2, y + L - 10), (x + 2.2, y + L - 10)],
           None, VIDRO, 0)                                                                # vidro de trás
    F.linha(x + W / 2, y + 1.5, x + W / 2, y + 10, esc, 0.3)                              # vinco do capô
    for s in (0, 1):
        F.ret(x + 1 + s * (W - 6), y + 0.4, x + 5 + s * (W - 6), y + 1.8, cor=None, fill=hexrgb("#fff3b0"), w=0)
        F.ret(x + 1 + s * (W - 6), y + L - 1.8, x + 5 + s * (W - 6), y + L - 0.4, cor=None, fill=hexrgb("#e0302a"), w=0)
    if taxi:
        F.ret(x + W / 2 - 5, y + L - 27, x + W / 2 + 5, y + L - 23, cor=PRETO, fill=BRANCO, w=0.2)
        F.texto(x + W / 2, y + L - 24.3, "TÁXI", 2.0, PRETO, negrito=True, ancora="c")
    corte(F, R(x, y, x + W, y + L))


def carro_lado(F, x, y, cor, frente_esquerda):
    """Lateral (50 x 15). frente_esquerda: a frente do carro fica à esquerda deste adesivo."""
    L, H = d.CARRO_L, d.CARRO_PAREDE_H

    def a_(a):
        return x + (L - a if frente_esquerda else a)          # a = 0 na traseira

    F.ret(x, y, x + L, y + H, cor=None, fill=cor, w=0)
    F.ret(x, y + H - 3.0, x + L, y + H, cor=None, fill=escurecer(cor, 0.7), w=0)         # saia
    # janelas: traseira (a 13-25) e dianteira com para-brisa inclinado (a 27-39)
    z0, z1 = 8.5, 13.5
    for (aa, ab), incl in (((13.0, 25.5), False), ((27.0, 39.0), True)):
        pts = [(a_(aa), y + H - z0), (a_(ab), y + H - z0), (a_(ab - (2.5 if incl else 0)), y + H - z1),
               (a_(aa), y + H - z1)]
        F.poly(pts, None, VIDRO, 0)
    F.linha(a_(26.2), y + H - 13.8, a_(26.2), y + H - 2.0, escurecer(cor, 0.6), 0.25)    # porta
    for a in (11.0, L - 11.0):
        cx, cy = a_(a), y + H - 4.2
        F.circ(cx, cy, 4.2, None, hexrgb("#151515"), 0)
        F.circ(cx, cy, 1.9, None, hexrgb("#b9bec6"), 0)
    F.ret(a_(L - 1.6), y + H - 8.5, a_(L - 0.2), y + H - 6.5, cor=None, fill=hexrgb("#fff3b0"), w=0)  # farol
    F.ret(a_(1.6), y + H - 8.5, a_(0.2), y + H - 6.5, cor=None, fill=hexrgb("#e0302a"), w=0)        # lanterna
    corte(F, R(x, y, x + L, y + H))


def carro_ponta(F, x, y, cor, frente):
    Wi, H = d.CARRO_W - 2 * d.T, d.CARRO_PAREDE_H
    F.ret(x, y, x + Wi, y + H, cor=None, fill=cor, w=0)
    F.ret(x, y + H - 3.5, x + Wi, y + H, cor=None, fill=escurecer(cor, 0.6), w=0)        # para-choque
    if frente:
        F.ret(x + 5, y + H - 9, x + Wi - 5, y + H - 5.5, cor=None, fill=hexrgb("#222222"), w=0)   # grade
        for s in (0, 1):
            F.ret(x + 1 + s * (Wi - 5), y + H - 9.5, x + 4 + s * (Wi - 5), y + H - 6.5, cor=None,
                  fill=hexrgb("#fff3b0"), w=0)
    else:
        for s in (0, 1):
            F.ret(x + 1 + s * (Wi - 5), y + H - 10, x + 4 + s * (Wi - 5), y + H - 7, cor=None,
                  fill=hexrgb("#e0302a"), w=0)
        F.ret(x + Wi / 2 - 4, y + H - 9.5, x + Wi / 2 + 4, y + H - 6.5, cor=PRETO, fill=BRANCO, w=0.15)
    corte(F, R(x, y, x + Wi, y + H))


def folha_carros(doc):
    F = Folha(doc)
    F.cabecalho("Adesivos dos carros (8)", "Teto, 2 laterais, frente e traseira de cada carro. Cole com cola bastão "
                "em cada peça ANTES de montar.", "adesivos 3/3")
    for k, (hexc, nome) in enumerate(CARROS):
        cor = hexrgb(hexc)
        col, lin = k % 2, k // 2
        x = 10 + col * 97
        y = 26 + lin * 62
        F.texto(x, y - 1.5, f"carro {k + 1}: {nome}", 2.2, PRETO, negrito=True)
        carro_teto(F, x, y + 1, cor, taxi=(nome == "táxi"))
        F.texto(x + 12, y + 55, "teto ↑frente", 1.6, CINZA, ancora="c")
        carro_lado(F, x + 29, y + 1, cor, frente_esquerda=True)
        F.texto(x + 54, y + 20, "lateral ESQUERDA (frente ←)", 1.6, CINZA, ancora="c")
        carro_lado(F, x + 29, y + 23, cor, frente_esquerda=False)
        F.texto(x + 54, y + 42, "lateral DIREITA (frente →)", 1.6, CINZA, ancora="c")
        carro_ponta(F, x + 29, y + 45, cor, frente=True)
        carro_ponta(F, x + 51, y + 45, cor, frente=False)
        F.texto(x + 72, y + 51.5, "← frente (esq.)", 1.6, CINZA)
        F.texto(x + 72, y + 54.5, "   traseira (dir.)", 1.6, CINZA)
    F.regua(MARGEM + 2, A4[1] - 12)
    F.fim()


def adesivos(saida):
    doc = pymupdf.open()
    # folha 1: paredes da guarita, totem e botão
    F = Folha(doc)
    F.cabecalho("Adesivos da guarita", "Imprima colorido, recorte pela linha fina e cole com cola bastão. "
                "Tracejado vermelho = recortar fora.", "adesivos 1/3")
    adesivo_painel(F, 10, 24)
    adesivo_fundo(F, 10, 24 + d.GUARITA_H + 12)
    y3 = 24 + 2 * (d.GUARITA_H + 11)
    gl = d.GUARITA_Y1 - d.GUARITA_Y0 - 2 * d.T
    adesivo_lado(F, 10, y3, porta=True)
    adesivo_lado(F, 10 + gl + 8, y3, porta=False)
    adesivo_totem(F, 10, y3 + d.GUARITA_H + 12)
    adesivo_botao(F, 80, y3 + d.GUARITA_H + 10)
    F.regua(MARGEM + 2, A4[1] - 12)
    F.fim()
    # folha 2: telhado e grama (deitada)
    F = Folha(doc, A4[1], A4[0])
    F.cabecalho("Adesivos: telhado e grama", "Telhado e grama vistos de cima, com a frente embaixo.", "adesivos 2/3")
    adesivo_telhado(F, 10, 24)
    adesivo_grama(F, 10 + d.GUARITA_X1 - d.GUARITA_X0 + 6 + 14, 24)
    F.regua(MARGEM + 2, A4[0] - 10)
    F.fim()
    folha_carros(doc)
    destino = os.path.join(saida, "adesivos_A4.pdf")
    doc.subset_fonts()
    doc.save(destino, garbage=3, deflate=True)
    return destino


def main(saida):
    os.makedirs(saida, exist_ok=True)
    for f in (etiquetas(saida), etiquetas(saida, teste=True), adesivos(saida)):
        print("gerado:", f)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../impressao")
