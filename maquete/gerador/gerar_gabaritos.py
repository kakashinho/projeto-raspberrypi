# -*- coding: utf-8 -*-
"""Gabaritos de corte em A4, escala 1:1, feitos para TESOURA (versão v5), com as mesmas peças do 3D.

Regra: todo corte começa na borda da peça; nenhum recorte estreito. Encaixes viram dobradiças de
fita crepe ou tiras coladas (guias e travas).

Uso:  python -B gerar_gabaritos.py ../impressao
"""
import os
import sys

import pymupdf

import design as d
import gerar_3d as g
from folha import (A4, AZUL, CINZA, CINZA_CLARO, MARGEM, MARROM, MM, PRETO, ROSA, VERDE, VERMELHO, Folha,
                   caixa_contorno, desenhar_peca)

NOMES = {
    "P1": "Piso", "EF": "Moldura: frente e fundo", "ES": "Moldura: lateral", "EM": "Moldura: painel do meio",
    "G1": "Painel (parede da frente)", "G2": "Parede do fundo", "G3": "Parede lateral", "G4": "Telhado",
    "S1": "Totem: frente", "S2": "Totem: lado", "C1": "Braço da cancela", "K1": "Botão do pot",
    "CL": "Carro: lateral", "CF": "Carro: frente/traseira", "CT": "Carro: teto", "B1": "Batente do Pi",
    "GP": "Guia (colar em cima do piso)", "TP": "Trava (colar embaixo do piso)", "GT": "Trava (colar embaixo do telhado)",
}
TIRAS = ("GP", "TP", "GT")
TOTAL = 8
CREME_COLA = (0.93, 0.85, 0.75)


def mm(v):
    return f"{v:.1f}".replace(".", ",")


def montar():
    g.piso()
    g.elevacao()
    g.guarita()
    g.eletronica()
    g.totem()
    g.cancelas()
    g.carros()
    pecas, qtd, todas = {}, {}, []
    for it in g.ITENS:
        if it["k"] == "placa" and it["cod"] and it["cod"] != "EVA":
            qtd[it["cod"]] = qtd.get(it["cod"], 0) + 1
            pecas.setdefault(it["cod"], it)
            todas.append(it)
    return pecas, qtd, todas


def nome_tira(it):
    n = it["n"].split(": ", 1)[1]
    for a, b in (("guia lateral esquerda", "guia lateral"), ("guia lateral direita", "guia lateral"),
                 ("trava esquerda", "trava lateral"), ("trava direita", "trava lateral"),
                 ("trava da esquerda", "trava lateral"), ("trava da direita", "trava lateral"),
                 (" (esq.)", ""), (" (dir.)", "")):
        n = n.replace(a, b)
    if it["cod"] == "TP":
        n = n.replace("trava da frente", "trava frente/fundo").replace("trava do fundo", "trava frente/fundo")
    return n


def tiras(todas):
    """Tiras distintas: [(cod, nome, comprimento, largura, quantidade)]."""
    vistos = {}
    for it in todas:
        if it["cod"] in TIRAS:
            a0, b0, a1, b1 = caixa_contorno(it["c"])
            k = (it["cod"], nome_tira(it), round(max(a1 - a0, b1 - b0), 1), round(min(a1 - a0, b1 - b0), 1))
            vistos[k] = vistos.get(k, 0) + 1
    return [(c, n, cp, lg, q) for (c, n, cp, lg), q in vistos.items()]


def rotulo(F, cod, qtd, x, y, extra=(), tam=3.0, ancora="c"):
    F.texto(x, y, f"{cod}  {NOMES[cod]}  ×{qtd}", tam, PRETO, negrito=True, ancora=ancora)
    for i, e in enumerate(extra):
        F.texto(x, y + tam * 1.35 * (i + 1), e, tam * 0.75, PRETO, ancora=ancora)


def dobradica(F, M, a0, b0, a1, b1, rotulo_txt="fita", lado=1):
    """Marca de dobradiça (fita crepe) ao longo de uma borda da peça."""
    p, q = M(a0, b0), M(a1, b1)
    F.linha(p[0], p[1], q[0], q[1], VERDE, 0.9, dashes="[2 1.2] 0")
    if rotulo_txt:
        xm, ym = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        F.texto(xm + 1.5 * lado, ym, rotulo_txt, 2.0, VERDE, negrito=True, ancora="e" if lado > 0 else "d")


def medida(it):
    a0, b0, a1, b1 = caixa_contorno(it["c"])
    return f"{mm(a1 - a0)} × {mm(b1 - b0)} mm"


# ---------------------------------------------------------------- folha 1: capa
def folha_capa(doc):
    F = Folha(doc)
    F.cabecalho("Maquete do estacionamento: gabaritos de corte",
                f"Feitos para TESOURA. Papelão de {mm(d.T)} mm, escala 1:1, versão v5", f"folha 1/{TOTAL}")
    y = 26
    F.texto(MARGEM, y, "Legenda", 3.2, PRETO, negrito=True)
    y += 6
    itens = [
        ("corte", "linha de corte: o contorno da peça"),
        ("furo", "recorte (sempre aberto numa borda e largo para a tesoura): corte e tire"),
        ("acesso", "linha de acesso: corte reto por ela, da borda até o furo (só no piso)"),
        ("fita", "dobradiça: junte as 2 peças nesta quina com fita crepe (por fora e por dentro)"),
        ("cola", "tira colada: guia ou trava (use a peça vizinha como espaçador)"),
        ("eva", "só no piso: corte do EVA preto"),
        ("ref", "referência: onde vai cada etiqueta PIMACO, parede ou peça"),
    ]
    for tipo, txt in itens:
        x0, x1 = MARGEM + 2, MARGEM + 22
        if tipo == "corte":
            F.linha(x0, y - 1, x1, y - 1, PRETO, 0.3)
        elif tipo == "furo":
            F.ret(x0, y - 3, x1, y + 1, cor=VERMELHO, fill=ROSA, w=0.3)
        elif tipo == "acesso":
            F.linha(x0, y - 1, x1, y - 1, VERMELHO, 0.45, dashes="[1.5 1] 0")
        elif tipo == "fita":
            F.linha(x0, y - 1, x1, y - 1, VERDE, 0.9, dashes="[2 1.2] 0")
        elif tipo == "cola":
            F.ret(x0, y - 3, x1, y + 1, cor=MARROM, fill=CREME_COLA, w=0.2)
        elif tipo == "eva":
            F.linha(x0, y - 1, x1, y - 1, AZUL, 0.4, dashes="[4 2] 0")
        else:
            F.ret(x0, y - 3, x1, y + 1, cor=CINZA, w=0.2, dashes="[1 1] 0")
        F.texto(x1 + 4, y, txt, 2.6)
        y += 7
    y += 2
    y = F.textos_bloco(MARGEM, y, [
        "**Como usar",
        "1. Imprima TODAS as folhas a 100 % (tamanho real). Em cada folha, meça a régua de 100 mm.",
        "2. Recorte o gabarito com uma sobra, prenda no papelão com fita crepe e corte por cima com a tesoura,",
        "    seguindo a linha. Ou fure os cantos com um alfinete, tire o papel e ligue os pontos a lápis.",
        "3. Não há rasgos estreitos: todo recorte começa numa borda e tem pelo menos 10 mm de largura.",
        "    Recorte largo: corte os 2 lados até o fundo e depois o fundo.",
        "4. Peça com ×N: use o mesmo gabarito N vezes. Tiras de 5 mm: corte uma tira comprida e depois os pedaços.",
        "5. Dobradiças: encoste as 2 peças na quina e passe fita crepe por fora e por dentro. Elas dobram planas.",
        "6. Tiras coladas (guias e travas): cole com cola branca encostando na peça vizinha, que serve de espaçador.",
    ], 2.5)
    y += 4
    F.texto(MARGEM, y, "Teste antes (corte num retalho)", 3.2, PRETO, negrito=True)
    y += 4
    x0, y0 = MARGEM + 2, y + 2
    larg, alt = 70.0, 34.0
    testes_servo = ((14.0, 11.0), (35.0, 11.5), (56.0, 12.0))
    cont = [(0, 0)]
    for xc, fw in testes_servo:
        cont += [(xc - fw / 2, 0), (xc - fw / 2, d.SERVO_RECORTE_Z), (xc + fw / 2, d.SERVO_RECORTE_Z), (xc + fw / 2, 0)]
    cont += [(larg, 0), (larg, alt), (0, alt)]
    F.poly([(x0 + a, y0 + (alt - b)) for a, b in cont], PRETO, None, 0.3)
    for xc, fw in testes_servo:
        F.ret(x0 + xc - fw / 2, y0 + alt - d.SERVO_RECORTE_Z, x0 + xc + fw / 2, y0 + alt, cor=VERMELHO, fill=ROSA, w=0.2)
        F.texto(x0 + xc, y0 + 4.5, mm(fw), 2.4, PRETO, negrito=True, ancora="c")
    F.texto(x0 + larg / 2, y0 + alt + 4, "servo: o corpo deve entrar justo (padrão 11,5)", 2.2, CINZA, ancora="c")
    x1 = x0 + larg + 12
    larg2, alt2 = 60.0, 24.0
    testes_tubo = ((12.0, 9.0), (30.0, 10.0), (48.0, 11.0))
    cont = [(0, 0), (larg2, 0), (larg2, alt2)]
    for xc, fw in sorted(testes_tubo, reverse=True):
        cont += [(xc + fw / 2, alt2), (xc + fw / 2, alt2 - 12), (xc - fw / 2, alt2 - 12), (xc - fw / 2, alt2)]
    cont += [(0, alt2)]
    F.poly([(x1 + a, y0 + (alt2 - b)) for a, b in cont], PRETO, None, 0.3)
    for xc, fw in testes_tubo:
        F.ret(x1 + xc - fw / 2, y0, x1 + xc + fw / 2, y0 + 12, cor=VERMELHO, fill=ROSA, w=0.2)
        F.texto(x1 + xc, y0 + 20, mm(fw), 2.4, PRETO, negrito=True, ancora="c")
    F.texto(x1 + larg2 / 2, y0 + alt + 4, "tubinho do pot (Ø 8,5): padrão 10", 2.2, CINZA, ancora="c")
    y = y0 + alt + 12
    F.textos_bloco(MARGEM, y, [
        "**Folhas",
        "2 e 3: piso (2 metades, emendar pelas cruzes) · 4: paredes da guarita · 5: telhado e laterais da moldura",
        "6: frente/fundo e meio da moldura, guia da calçada · 7: carro, totem, braço, botão, batente e tiras",
        "8: plano de corte da chapa. Etiquetas: etiquetas_pimaco6282.pdf (CARTA). Adesivos: adesivos_A4.pdf",
        "Material extra: fita crepe (dobradiças) e cola branca (tiras, EVA e carros).",
    ], 2.5)
    F.regua(MARGEM + 2, A4[1] - 14)
    F.fim()


# ---------------------------------------------------------------- piso inteiro (página auxiliar)
OX, OY = 10.0, 12.0
EMENDA = 155.0


def desenhar_piso(doc, pecas, todas):
    W, D = d.PISO_W, d.PISO_D
    F = Folha(doc, W + 2 * OX, D + 2 * OY)

    def p(x, y):
        return OX + x, OY + (D - y)

    def R(x0, y0, x1, y1, **kw):
        a, b = p(x0, y1)
        c, e = p(x1, y0)
        F.ret(a, b, c, e, **kw)

    def poly(pts, **kw):
        F.poly([p(x, y) for x, y in pts], **kw)

    def txt(x, y, s, tam=2.2, cor=PRETO, **kw):
        a, b = p(x, y)
        F.texto(a, b, s, tam, cor, **kw)

    def pegada(it, **kw):
        ox, oy, _ = it["o"]
        a0, b0, a1, b1 = caixa_contorno(it["c"])
        if it["pl"] == "xz":
            R(ox + a0, oy, ox + a1, oy + d.T, **kw)
        else:
            R(ox, oy + a0, ox + d.T, oy + a1, **kw)

    # moldura por baixo (referência)
    for it in todas:
        if it["cod"] in ("EF", "ES", "EM"):
            pegada(it, cor=CINZA_CLARO, w=0.2, dashes="[3 1 1 1] 0")
    # travas coladas embaixo do piso (tracejado marrom)
    for x0, y0, x1, y1, nome in d.travas_piso():
        R(x0, y0, x1, y1, cor=MARROM, w=0.3, dashes="[1.5 1] 0")
    tf = d.travas_piso()[0]
    txt(tf[2] + 1.5, tf[1] + 1, "TP: colar POR BAIXO", 1.8, MARROM)
    # paredes, totem, Pi (referência)
    for it in todas:
        if it["cod"] in ("G1", "G2", "G3", "S1", "S2"):
            pegada(it, cor=CINZA, w=0.15, dashes="[1 1] 0")
    gx0, gx1, gy1 = d.GUARITA_X0, d.GUARITA_X1, d.GUARITA_Y1
    X, Y = d.X, d.Y
    R(X(d.PI[0]), Y(d.PI[3]), X(d.PI[2]), Y(d.PI[1]), cor=CINZA_CLARO, w=0.2, dashes="[2 1] 0")
    txt((X(d.PI[0]) + X(d.PI[2])) / 2, Y(30), "Raspberry Pi (entre os batentes)", 2.0, CINZA, ancora="c")
    txt((gx0 + gx1) / 2, gy1 - 7, "GUARITA: chão sem EVA", 2.4, CINZA, negrito=True, ancora="c")
    txt(d.TOTEM_X0 + 4, d.US_Y + d.TOTEM_L / 2 + 2.5, "totem", 2.0, CINZA)
    # grama
    R(0, 0, d.ENTRADA_X0 - d.FAIXA, d.ILHA_Y1, cor=VERDE, w=0.25, dashes="[2 1] 0")
    txt(2, d.ILHA_Y1 - 4, "grama (papel)", 2.0, VERDE)
    # tiras coladas em cima e batentes
    for it in todas:
        if it["cod"] in ("GP", "B1"):
            poly(it["c"], cor=MARROM, fill=CREME_COLA, w=0.2)
    txt(X(d.PI[0]) + 9, Y(d.PI[1]) - 3.5, "B1 colar", 1.8, MARROM)
    gl = d.guias_piso()
    txt(gl[1][0] - 0.5, (gl[1][1] + gl[1][3]) / 2, "GP", 1.8, MARROM, ancora="d")
    txt(gl[2][2] + 0.5, (gl[2][1] + gl[2][3]) / 2, "GP", 1.8, MARROM)
    txt((gl[3][0] + gl[3][2]) / 2, gl[3][3] + 1.2, "GP colar (guia do fundo)", 1.8, MARROM, ancora="c")
    # etiquetas PIMACO
    for cod, tipo, dado in d.marcas_piso():
        if tipo == "faixa":
            x0, y0, x1, y1 = dado
            R(x0, y0, x1, y1, cor=CINZA, w=0.15, dashes="[1 1] 0")
            if cod in ("C1", "C2"):
                continue
            if x1 - x0 > y1 - y0:
                txt((x0 + x1) / 2, y1 + 1.2, cod, 1.8, CINZA, ancora="c")
            else:
                txt(x1 + 0.6, (y0 + y1) / 2, cod, 1.8, CINZA)
        elif tipo == "seta":
            poly(dado, cor=CINZA, w=0.15, dashes="[1 1] 0")
            cx = sum(q[0] for q in dado) / len(dado)
            cy = sum(q[1] for q in dado) / len(dado)
            txt(cx, cy - 6.5, cod, 1.8, CINZA, ancora="c")
        else:
            x0, y0, x1, y1 = dado[1:]
            R(x0, y0, x1, y1, cor=CINZA, w=0.15, dashes="[1 1] 0")
            t = dado[0] if tipo == "escrita" else str(dado[0])
            txt((x0 + x1) / 2, (y0 + y1) / 2 - 0.8, f"{cod} {t}" if tipo == "escrita" else t, 1.8, CINZA, ancora="c")
    cal = gl[0]
    txt((cal[0] + cal[2]) / 2 + 30, cal[1] + 1.4, "GP calçada (colar) + etiquetas C1 e C2", 1.8, MARROM, ancora="c")
    # EVA: recorte da guarita (azul tracejado)
    s_ = d.SEM_EVA
    poly([(gx0 - s_, 0), (gx0 - s_, gy1 + s_), (gx1 + s_, gy1 + s_), (gx1 + s_, 0)], cor=AZUL, w=0.4,
         dashes="[4 2] 0", fechar=False)
    txt(gx1 + s_ - 1, gy1 + s_ + 2.5, "EVA: recortar aqui", 2.0, AZUL, ancora="d")
    # o piso: contorno, furos e linhas de acesso
    P1 = pecas["P1"]
    poly(P1["c"], cor=PRETO, w=0.35)
    for f in P1["f"]:
        poly(f, cor=VERMELHO, fill=ROSA, w=0.25)
    for xa, ya, xb, yb in d.fendas_acesso():
        a, b = p(xa, ya)
        c, e = p(xb, yb)
        F.linha(a, b, c, e, VERMELHO, 0.45, dashes="[1.5 1] 0")
    fc = d.FURO_CABOS
    txt((fc[0] + fc[2]) / 2, (fc[1] + fc[3]) / 2 + 1, "furo de cabos", 2.0, VERMELHO, ancora="c")
    fr = d.FURO_REDE
    txt((fr[0] + fr[2]) / 2, (fr[1] + fr[3]) / 2, "furo da rede", 2.0, VERMELHO, ancora="c")
    for xa, ya, xb, yb in d.fendas_acesso():
        txt(xa + 1.0, 7.5, "acesso", 1.6, VERMELHO)
    us = d.US_RASGO
    txt(us[2] + 1.5, us[3] + 1.5, "recorte do sensor", 1.8, VERMELHO)
    # emenda das 2 metades
    for yy in (12.0, 100.0, 188.0):
        a, b = p(EMENDA, yy)
        F.linha(a - 4, b, a + 4, b, PRETO, 0.25)
        F.linha(a, b - 4, a, b + 4, PRETO, 0.25)
        F.circ(a, b, 1.5, PRETO, None, 0.2)
    txt(4, -4.5, "FRENTE (lado de quem opera a maquete) ↓", 2.4, PRETO, negrito=True)
    txt(W - 2, D + 2.2, "FUNDO", 2.4, PRETO, negrito=True, ancora="d")
    F.fim()
    return F


def folhas_piso(doc, aux):
    W, D = d.PISO_W, d.PISO_D
    metades = [("esquerda", -3.0, EMENDA + 6.0, 2), ("direita", EMENDA - 6.0, W + 3.0, 3)]
    for nome, xa, xb, n in metades:
        F = Folha(doc)
        F.cabecalho(f"P1 Piso: metade {nome}", "Vista de cima, frente embaixo. Sobreponha as 2 folhas pelas 3 cruzes e "
                    "prenda com fita.", f"folha {n}/{TOTAL}")
        clip = pymupdf.Rect((OX + xa) * MM, (OY - 9) * MM, (OX + xb) * MM, (OY + D + 9) * MM)
        x_pg, y_pg = 14.0, 22.0
        dest = pymupdf.Rect(x_pg * MM, y_pg * MM, (x_pg + xb - xa) * MM, (y_pg + D + 18) * MM)
        F.page.show_pdf_page(dest, aux, 0, clip=clip)
        y = y_pg + D + 25
        F.textos_bloco(MARGEM, y, [
            "**Piso (papelão 311 × 200): sem rasgos",
            "• Contorno: o retângulo já desenhado (281 × 200) cresce 30 mm para a direita. Recorte do sensor: aberto na borda.",
            "• Furos (vermelho): corte reto pela linha de acesso (tracejada), da borda da frente até o furo, e recorte o furo.",
            "  Depois passe fita crepe por baixo da linha de acesso. A tira da calçada, colada por cima, também fecha o corte.",
            "• EVA preto: mesmo molde. Contorno, recorte da guarita (azul) e recorte do sensor. Cole com cola branca.",
            "• Tiras: GP e B1 colam em cima; TP (tracejado marrom) colam por baixo. Etiquetas: códigos em cinza.",
        ], 2.35)
        F.regua(MARGEM + 2, A4[1] - 12)
        F.fim()


# ---------------------------------------------------------------- folha 4: paredes da guarita
def folha_paredes(doc, pecas, qtd):
    F = Folha(doc)
    F.cabecalho("Guarita: paredes", "Fundo + 2 laterais com dobradiças de fita (dobram planas). O painel fica solto.",
                f"folha 4/{TOTAL}")
    x, y = 10.0, 24.0
    gx0 = d.GUARITA_X0
    M, w, h = desenhar_peca(F, pecas["G1"], x, y)
    rotulo(F, "G1", qtd["G1"], x + w * 0.72, y + 30, ["vista de FORA (você de frente para o painel)", "↑ em cima"])
    xp, zp = M((d.POT_RECORTE[0] + d.POT_RECORTE[2]) / 2 - gx0, d.POT_RECORTE[1])
    F.texto(xp, zp + 4, "tubinho", 2.0, VERMELHO, ancora="c")
    lx, lz = M((d.LED_RECORTE[0] + d.LED_RECORTE[2]) / 2 - gx0, d.LED_RECORTE[1])
    F.texto(lx, lz + 4, "LED", 2.0, VERMELHO, ancora="c")
    ex, ez = M((d.ENERGIA_RASGO[0] + d.ENERGIA_RASGO[2]) / 2 - gx0, d.ENERGIA_RASGO[3])
    F.texto(ex, ez - 1.5, "energia", 2.0, VERMELHO, ancora="c")
    y += h + 10
    M, w, h = desenhar_peca(F, pecas["G2"], x, y)
    gx = d.GUARITA_X1 - d.GUARITA_X0
    dobradica(F, M, 0.6, 2, 0.6, d.GUARITA_H - 2, "fita", 1)
    dobradica(F, M, gx - 0.6, 2, gx - 0.6, d.GUARITA_H - 2, "fita", -1)
    rotulo(F, "G2", qtd["G2"], x + w / 2, y + 22, ["recortes de baixo: servos (em pé, eixo para fora)",
                                                     "dobradiças (verde) nas 2 pontas, com as laterais G3", "↑ em cima"])
    y += h + 10
    M, w, h = desenhar_peca(F, pecas["G3"], x, y)
    gl = d.GUARITA_Y1 - d.GUARITA_Y0 - 2 * d.T
    dobradica(F, M, gl - 0.6, 2, gl - 0.6, d.GUARITA_H - 2, "fita", -1)
    rotulo(F, "G3", qtd["G3"], x + w / 2 - 4, y + 22, ["↑ em cima", "← frente  |  fundo (fita) →"], tam=2.8)
    F.textos_bloco(x + w + 10, y + 4, [
        "**Montagem da guarita",
        "1. Junte G2 com as 2 G3 pelas quinas de trás",
        "    (fita crepe por fora e por dentro): vira um U.",
        "2. Ponha os servos em pé no piso, no lugar;",
        "    desça o U por cima: os servos entram",
        "    pelos recortes de baixo do fundo.",
        "3. O U fica entre as guias GP coladas no piso.",
        "4. Pi + placa entre os batentes.",
        "5. Painel G1: atrás da tira da calçada,",
        "    encostado na frente das laterais. O botão",
        "    do pot, por fora, segura ele em pé.",
        "6. Telhado por cima (travas GT por dentro).",
        "Para tirar o painel: puxe o botão, incline",
        "para a frente e levante.",
    ], 2.4)
    F.regua(MARGEM + 2, A4[1] - 12)
    F.fim()


# ---------------------------------------------------------------- folha 5: telhado + laterais da moldura
def folha_telhado(doc, pecas, qtd):
    F = Folha(doc, A4[1], A4[0])
    F.cabecalho("Telhado e laterais da moldura", "Telhado visto de cima (frente embaixo); as travas GT colam por baixo.",
                f"folha 5/{TOTAL}")
    x, y = 9.0, 22.0
    G4 = pecas["G4"]
    M, w, h = desenhar_peca(F, G4, x, y)
    ox, oy, _ = G4["o"]
    for x0, y0, x1, y1, nome in d.travas_telhado():
        a, b = M(x0 - ox, y1 - oy)
        c, e = M(x1 - ox, y0 - oy)
        F.ret(a, b, c, e, cor=MARROM, w=0.3, dashes="[1.5 1] 0")
    rotulo(F, "G4", qtd["G4"], x + w / 2, y + h / 2 - 4, ["vista de cima, FRENTE embaixo ↓",
                                                           "tracejado marrom: travas GT (colar POR BAIXO)"])
    F.textos_bloco(x + w + 8, y + 6, [
        "**Telhado",
        "Retângulo liso. As 3 travas",
        "GT colam embaixo, por dentro",
        "das laterais e do fundo:",
        "o telhado encaixa no U e não",
        "escorrega. O painel da frente",
        "sai sem tirar o telhado.",
        "",
        "**Moldura (estrutura de 5 cm)",
        "4 painéis com dobradiças nos",
        "cantos (o 4º canto fecha com",
        "fita na montagem). Os vãos",
        "embaixo são para os cabos.",
    ], 2.4)
    y += h + 13
    M, w, h = desenhar_peca(F, pecas["ES"], x, y)
    comp = d.MOLD_Y[1] - d.MOLD_Y[0] - 2 * d.T
    dobradica(F, M, 0.6, 2, 0.6, d.ELEV_H - 2, "fita", 1)
    dobradica(F, M, comp - 0.6, 2, comp - 0.6, d.ELEV_H - 2, "fita", -1)
    rotulo(F, "ES", qtd["ES"], x + w / 2, y + 14, ["↑ em cima (encosta no piso)", "o vão é a passagem do cabo do sensor"])
    F.regua(MARGEM + 2, A4[0] - 10)
    F.fim()


# ---------------------------------------------------------------- folha 6: frente/fundo e meio da moldura
def folha_moldura(doc, pecas, qtd, todas):
    F = Folha(doc, A4[1], A4[0])
    F.cabecalho("Moldura: frente/fundo e painel do meio", "A frente e o fundo são iguais (×2). O painel do meio fica "
                "solto, entre 2 travas TP coladas embaixo do piso.", f"folha 6/{TOTAL}")
    x, y = 9.0, 22.0
    M, w, h = desenhar_peca(F, pecas["EF"], x, y)
    comp = d.MOLD_X[1] - d.MOLD_X[0]
    dobradica(F, M, 0.6, 2, 0.6, d.ELEV_H - 2, "fita", 1)
    dobradica(F, M, comp - 0.6, 2, comp - 0.6, d.ELEV_H - 2, "fita", -1)
    rotulo(F, "EF", qtd["EF"], x + w / 2, y + 14, ["↑ em cima", "o vão é a passagem do cabo de rede"])
    y += h + 13
    M, w, h = desenhar_peca(F, pecas["EM"], x, y)
    rotulo(F, "EM", qtd["EM"], x + w / 2, y + 14, ["↑ em cima", "solto; fica de pé entre as travas TP do meio"])
    F.textos_bloco(x + w + 10, y + 4, [
        "**Montagem da moldura",
        "1. Junte EF, ES, EF, ES com fita nas quinas",
        "    (por fora e por dentro), formando um anel.",
        "2. Feche a última quina com um pedaço de fita.",
        "3. Ponha o painel do meio EM em pé.",
        "4. Desça o piso: as travas TP de baixo",
        "    encaixam por dentro da moldura e dos",
        "    dois lados do EM.",
        "Para guardar: tire a fita da última quina e",
        "dobre a moldura em zigue-zague.",
    ], 2.4)
    y += h + 12
    cal = [it for it in todas if it["cod"] == "GP" and "calçada" in it["n"]][0]
    a0, b0, a1, b1 = caixa_contorno(cal["c"])
    F.ret(x, y, x + (a1 - a0), y + (b1 - b0), cor=PRETO, fill=CREME_COLA, w=0.3)
    F.texto(x, y + (b1 - b0) + 4, f"GP  guia da calçada  ×1  ({mm(a1 - a0)} × {mm(b1 - b0)}): cola na frente da guarita, "
            "encostada no painel; as etiquetas C1 e C2 vão em cima", 2.3, PRETO)
    F.regua(MARGEM + 2, A4[0] - 10)
    F.fim()


# ---------------------------------------------------------------- folha 7: peças pequenas + tiras
def folha_pequenas(doc, pecas, qtd, todas):
    F = Folha(doc, A4[1], A4[0])
    F.cabecalho("Peças pequenas e tiras", "Carro (caixinha colada), totem do sensor, braço da cancela, botão do pot, "
                "batente do Pi e as tiras de 5 mm.", f"folha 7/{TOTAL}")
    x, y = 9.0, 24.0
    xx = x
    hmax = 0
    for cod, rot, extra in (("CL", 0, ["2 por carro"]), ("CF", 0, ["2 por carro"]), ("CT", 90, ["1 por carro"]),
                            ("S1", 0, ["↑ em cima", "janelas = sensor"]), ("S2", 0, ["fita na quina", "com S1"])):
        it = pecas[cod]
        M, w, h = desenhar_peca(F, it, xx, y, rot=rot)
        if cod == "S1":
            L1 = d.TOTEM_L
            dobradica(F, M, 0.6, 2, 0.6, d.TOTEM_H - 2, "", 1)
            dobradica(F, M, L1 - 0.6, 2, L1 - 0.6, d.TOTEM_H - 2, "", -1)
        F.texto(xx + w / 2, y + h + 4.5, f"{cod} ×{qtd[cod]}", 2.6, PRETO, negrito=True, ancora="c")
        F.texto(xx + w / 2, y + h + 8.0, NOMES[cod], 1.9, PRETO, ancora="c")
        for i, e in enumerate(extra):
            F.texto(xx + w / 2, y + h + 11.0 + 2.8 * i, e, 1.9, CINZA, ancora="c")
        xx += max(w, 22) + 10
        hmax = max(hmax, h)
    y2 = y + hmax + 24
    xx = x
    for cod, extra in (("C1", ["● = eixo do servo"]), ("K1", []), ("B1", ["colar no piso"])):
        it = pecas[cod]
        M, w, h = desenhar_peca(F, it, xx, y2)
        if cod == "C1":
            F.circ(xx + w - d.BRACO_ATRAS, y2 + h / 2, 1.0, PRETO, PRETO, 0.2)
        F.texto(xx + w / 2, y2 + h + 4.5, f"{cod} ×{qtd[cod]}", 2.6, PRETO, negrito=True, ancora="c")
        F.texto(xx + w / 2, y2 + h + 8.0, NOMES[cod], 1.9, PRETO, ancora="c")
        for i, e in enumerate(extra):
            F.texto(xx + w / 2, y2 + h + 11.0 + 2.8 * i, e, 1.9, CINZA, ancora="c")
        xx += max(w, 22) + 10
    xt, yt = 128.0, y2 - 4
    F.texto(xt, yt, "Tiras de 5 mm (cola branca)", 2.8, PRETO, negrito=True)
    yt += 4
    for cod, nome, comp, larg, q in sorted(tiras(todas), key=lambda t: (t[0], -t[2])):
        if "calçada" in nome:
            continue
        F.texto(xt, yt + 2.2, f"{cod} ×{q}  {nome} ({mm(comp)} × {mm(larg)})", 2.0, PRETO)
        F.ret(xt, yt + 3.2, xt + comp, yt + 3.2 + larg, cor=PRETO, fill=CREME_COLA, w=0.25)
        yt += larg + 6.2
    F.textos_bloco(x, y2 + 30, [
        "**Carro (8): caixinha colada",
        "1. Cole os adesivos nas peças.",
        "2. Teto CT virado para baixo; cole as",
        "    2 laterais CL em pé nas bordas compridas",
        "    e a frente/traseira CF entre elas.",
        "**Totem: S1 + 2 S2 com fita nas quinas;",
        "o sensor fica dentro, pinos no recorte.",
    ], 2.3)
    F.regua(MARGEM + 2, A4[0] - 10)
    F.fim()


# ---------------------------------------------------------------- folha 8: plano de corte
def folha_plano(doc, qtd, todas):
    F = Folha(doc)
    F.cabecalho("Plano de corte da chapa de papelão (1 m × 1 m), escala 1:6",
                "Sugestão de onde tirar cada peça. Deixe ~4 mm entre as peças.", f"folha 8/{TOTAL}")
    k = 1 / 6
    x0, y0 = 10.0, 24.0
    S = 1000.0
    F.ret(x0, y0, x0 + S * k, y0 + S * k, cor=PRETO, w=0.4)
    itens = []
    for i, it in enumerate(todas):
        a0, b0, a1, b1 = caixa_contorno(it["c"])
        itens.append((i, a1 - a0, b1 - b0))
    lugar, n = d.empilhar(itens, largura=S - 8, fundo=S - 8)
    if n > 1:
        print("AVISO: as peças não cabem numa chapa só")
    cores = {"P1": (0.85, 0.85, 0.85), "EF": (0.8, 0.88, 0.95), "ES": (0.8, 0.88, 0.95), "EM": (0.8, 0.88, 0.95),
             "G1": (0.98, 0.93, 0.8), "G2": (0.98, 0.93, 0.8), "G3": (0.98, 0.93, 0.8), "G4": (0.85, 0.87, 0.9)}
    for i, px, py, w, h, cam, girou in lugar:
        cod = todas[i]["cod"]
        xr0, yr0 = x0 + (4 + px) * k, y0 + (4 + py) * k
        F.ret(xr0, yr0, xr0 + w * k, yr0 + h * k, cor=PRETO, fill=cores.get(cod, (0.95, 0.95, 0.95)), w=0.15)
        if w * k > 6 and h * k > 2.2:
            F.texto(xr0 + w * k / 2, yr0 + h * k / 2 + 0.8, cod, 2.0 if w * k > 12 else 1.4, PRETO, ancora="c")
    y = y0 + S * k + 8
    F.texto(x0, y, "Lista de peças de papelão", 3.0, PRETO, negrito=True)
    y += 5
    vistos = {}
    for it in todas:
        vistos.setdefault(it["cod"], it)
    col = [x0, x0 + 12, x0 + 74, x0 + 88]
    for c, t in zip(col, ("Código", "Peça", "Qtd", "Medida")):
        F.texto(c, y, t, 2.3, CINZA, negrito=True)
    y += 3.8
    for cod in ("P1", "EF", "ES", "EM", "G1", "G2", "G3", "G4", "S1", "S2", "C1", "K1", "B1", "CL", "CF", "CT"):
        F.texto(col[0], y, cod, 2.3, PRETO, negrito=True)
        F.texto(col[1], y, NOMES[cod], 2.3)
        F.texto(col[2], y, f"×{qtd[cod]}", 2.3)
        F.texto(col[3], y, medida(vistos[cod]), 2.3)
        y += 3.4
    F.texto(col[0], y, f"+ tiras de 5 mm: GP ×{qtd['GP']}, TP ×{qtd['TP']}, GT ×{qtd['GT']} "
            "(comprimentos nas folhas 6 e 7)", 2.3, PRETO)
    F.regua(MARGEM + 2, A4[1] - 12)
    F.fim()


def main(saida):
    os.makedirs(saida, exist_ok=True)
    pecas, qtd, todas = montar()
    aux = pymupdf.open()
    desenhar_piso(aux, pecas, todas)
    doc = pymupdf.open()
    folha_capa(doc)
    folhas_piso(doc, aux)
    folha_paredes(doc, pecas, qtd)
    folha_telhado(doc, pecas, qtd)
    folha_moldura(doc, pecas, qtd, todas)
    folha_pequenas(doc, pecas, qtd, todas)
    folha_plano(doc, qtd, todas)
    destino = os.path.join(saida, "gabaritos_A4.pdf")
    doc.subset_fonts()
    doc.save(destino, garbage=3, deflate=True)
    print("gerado:", destino, f"({len(doc)} folhas)")
    return destino


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../impressao")
