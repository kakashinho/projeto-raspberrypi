# -*- coding: utf-8 -*-
"""Planta vista de cima, cotada, para validar o layout (Fase 1).

Uso:  python gerar_planta.py ../previas/planta.png
Todas as medidas vêm de design.py. A frente da maquete fica embaixo na imagem.
"""
import math
import sys

import pymupdf

import design as d

MM = 72 / 25.4
MARG = 22.0
LEG = 78.0
FONTE = "C:/Windows/Fonts/arial.ttf"
FONTE_B = "C:/Windows/Fonts/arialbd.ttf"

ASFALTO = (0.17, 0.17, 0.19)
BRANCO = (0.97, 0.97, 0.97)
PAPELAO = (0.78, 0.69, 0.53)
GRAMA = (0.36, 0.58, 0.30)
CALCADA = (0.72, 0.72, 0.70)
PI_VERDE = (0.13, 0.50, 0.28)
SERVO_AZUL = (0.18, 0.38, 0.85)
SENSOR_AZUL = (0.10, 0.30, 0.70)
PRATA = (0.80, 0.82, 0.85)
VERMELHO = (0.85, 0.12, 0.12)
PRETO = (0, 0, 0)
COTA = (0.25, 0.25, 0.25)

PAGE_W = (d.PISO_W + 2 * MARG) * MM
PAGE_H = (d.PISO_D + 2 * MARG + LEG) * MM


def P(x, y):
    return pymupdf.Point((MARG + x) * MM, (MARG + d.PISO_D - y) * MM)


def R(x0, y0, x1, y1):
    a, b = P(min(x0, x1), max(y0, y1)), P(max(x0, x1), min(y0, y1))
    return pymupdf.Rect(a, b)


class Desenho:
    def __init__(self):
        self.doc = pymupdf.open()
        self.page = self.doc.new_page(width=PAGE_W, height=PAGE_H)
        self.page.insert_font(fontname="F0", fontfile=FONTE)
        self.page.insert_font(fontname="F1", fontfile=FONTE_B)
        self.f0 = pymupdf.Font(fontfile=FONTE)
        self.f1 = pymupdf.Font(fontfile=FONTE_B)
        self.sh = self.page.new_shape()

    def ret(self, x0, y0, x1, y1, fill=None, cor=None, w=0.3, op=1.0, dashes=None):
        self.sh.draw_rect(R(x0, y0, x1, y1))
        self.sh.finish(color=cor, fill=fill, width=w * MM, fill_opacity=op, dashes=dashes)

    def poli(self, pts, fill=None, cor=None, w=0.3, op=1.0, fechar=True):
        self.sh.draw_polyline([P(x, y) for x, y in pts])
        self.sh.finish(color=cor, fill=fill, width=w * MM, fill_opacity=op, closePath=fechar)

    def linha(self, x0, y0, x1, y1, cor=PRETO, w=0.3, dashes=None):
        self.sh.draw_line(P(x0, y0), P(x1, y1))
        self.sh.finish(color=cor, width=w * MM, dashes=dashes)

    def circ(self, x, y, r, fill=None, cor=None, w=0.3):
        self.sh.draw_circle(P(x, y), r * MM)
        self.sh.finish(color=cor, fill=fill, width=w * MM)

    def texto(self, x, y, s, tam=2.6, cor=PRETO, negrito=False, centro=True, rot=0):
        """tam em mm (altura aproximada da letra)."""
        fs = tam * MM * 1.35
        fonte = self.f1 if negrito else self.f0
        larg = fonte.text_length(s, fontsize=fs)
        p = P(x, y)
        if rot == 0:
            pt = pymupdf.Point(p.x - (larg / 2 if centro else 0), p.y + fs * 0.35)
        else:   # 90 graus: texto subindo
            pt = pymupdf.Point(p.x + fs * 0.35, p.y + (larg / 2 if centro else 0))
        self.textos.append((pt, s, fs, "F1" if negrito else "F0", cor, rot))

    def seta(self, x, y, ang, comp=14, larg=6, cor=BRANCO):
        """Seta pintada no piso; ang em graus (0 = +X, 90 = +Y)."""
        a = math.radians(ang)
        ux, uy = math.cos(a), math.sin(a)
        nx, ny = -uy, ux
        h, c = comp * 0.45, larg * 0.32
        pts = [(-comp / 2, -c), (comp / 2 - h, -c), (comp / 2 - h, -larg / 2), (comp / 2, 0),
               (comp / 2 - h, larg / 2), (comp / 2 - h, c), (-comp / 2, c)]
        self.poli([(x + px * ux + py * nx, y + px * uy + py * ny) for px, py in pts], fill=cor)

    def cota_h(self, x0, x1, y, s, acima=False):
        self.linha(x0, y, x1, y, COTA, 0.2)
        for x in (x0, x1):
            self.linha(x, y - 1.6, x, y + 1.6, COTA, 0.2)
        self.texto((x0 + x1) / 2, y + (2.6 if acima else -3.2), s, 2.2, COTA)

    def cota_v(self, y0, y1, x, s):
        self.linha(x, y0, x, y1, COTA, 0.2)
        for y in (y0, y1):
            self.linha(x - 1.6, y, x + 1.6, y, COTA, 0.2)
        self.texto(x - 2.6, (y0 + y1) / 2, s, 2.2, COTA, rot=90)

    def carro(self, cx, y0, cor, frente_para_cima=True):
        L, W = d.CARRO_L, d.CARRO_W
        x0, x1, y1 = cx - W / 2, cx + W / 2, y0 + L
        self.ret(x0, y0, x1, y1, fill=cor, cor=PRETO, w=0.25)
        # teto e vidros (o para-brisa fica do lado da frente do carro)
        tf = (0.12, 0.14, 0.18)
        if frente_para_cima:
            self.ret(x0 + 3, y0 + L * 0.30, x1 - 3, y0 + L * 0.72, fill=tf)
            self.ret(x0 + 4, y0 + L * 0.40, x1 - 4, y0 + L * 0.66, fill=cor)
        else:
            self.ret(x0 + 3, y0 + L * 0.28, x1 - 3, y0 + L * 0.70, fill=tf)
            self.ret(x0 + 4, y0 + L * 0.34, x1 - 4, y0 + L * 0.60, fill=cor)


def desenhar(saida):
    g = Desenho()
    g.textos = []

    # ---------------------------------------------------------------- piso e calçadas
    g.ret(0, 0, d.PISO_W, d.PISO_D, fill=ASFALTO, cor=PRETO, w=0.5)
    # ilha do sensor (grama impressa) e calçada da frente / da direita
    g.ret(0, 0, d.ENTRADA_X0, d.GUARITA_Y1, fill=GRAMA)
    g.ret(d.GUARITA_X0, 0, d.GUARITA_X1, d.GUARITA_Y0, fill=CALCADA)
    g.ret(d.SAIDA_X1, 0, d.PISO_W, d.GUARITA_Y1, fill=CALCADA)
    # meio-fio branco nas bordas das faixas de rolamento
    F = d.FAIXA
    g.ret(d.ENTRADA_X0 - F, 0, d.ENTRADA_X0, d.GUARITA_Y1, fill=BRANCO)
    g.ret(d.SAIDA_X1, 0, d.SAIDA_X1 + min(F, d.PISO_W - d.SAIDA_X1), d.GUARITA_Y1, fill=BRANCO)

    # ---------------------------------------------------------------- vagas
    for k in range(d.N_VAGAS + 1):
        x = d.VAGAS_X0 + k * d.VAGA_PASSO
        g.ret(x, d.VAGAS_Y0, x + F, d.PISO_D - 2, fill=BRANCO)
    g.ret(d.VAGAS_X0, d.PISO_D - 2 - F, d.VAGAS_X0 + d.VAGAS_W, d.PISO_D - 2, fill=BRANCO)
    for k in range(d.N_VAGAS):
        cx = d.VAGAS_X0 + F / 2 + (k + 0.5) * d.VAGA_PASSO
        g.texto(cx, d.VAGAS_Y0 + 8, str(k + 1), 5, BRANCO, negrito=True)

    # setas: entra pela esquerda, anda no corredor para a direita, sai pela direita
    yc = (d.GUARITA_Y1 + d.VAGAS_Y0) / 2
    for x in (d.PISO_W * 0.40, d.PISO_W * 0.62):
        g.seta(x, yc, 0, 18, 8)
    g.seta(d.ENTRADA_X0 + d.FAIXA_ENTRADA / 2, 12, 90, 14, 7)
    g.seta(d.SAIDA_X0 + d.FAIXA_SAIDA / 2, 12, -90, 14, 7)

    # ---------------------------------------------------------------- carros
    cores = [(0.85, 0.15, 0.15), (0.95, 0.75, 0.10), (0.15, 0.35, 0.80), (0.92, 0.92, 0.92),
             (0.95, 0.50, 0.10), (0.20, 0.60, 0.40)]
    g.carro(d.ENTRADA_X0 + d.FAIXA_ENTRADA / 2, d.CARRO_ESPERA_Y0, cores[0])
    for i, k in enumerate([1, 2, 4, 6]):
        if k >= d.N_VAGAS:
            continue
        cx = d.VAGAS_X0 + F / 2 + (k + 0.5) * d.VAGA_PASSO
        g.carro(cx, d.VAGAS_Y0 + 3.0, cores[1 + i % 5])

    # ---------------------------------------------------------------- guarita: interior
    X, Y = d.X, d.Y
    T = d.T
    g.ret(d.GUARITA_X0, d.GUARITA_Y0, d.GUARITA_X1, d.GUARITA_Y1, fill=(0.90, 0.87, 0.80))
    # furo de cabos (sob o balanço da placa)
    fx0, fy0, fx1, fy1 = d.FURO_CABOS
    g.ret(fx0, fy0, fx1, fy1, fill=(0.05, 0.05, 0.05), cor=VERMELHO, w=0.35, dashes="[3 2] 0")
    # Pi
    g.ret(X(d.PI[0]), Y(d.PI[3]), X(d.PI[2]), Y(d.PI[1]), fill=PI_VERDE, cor=PRETO, w=0.25)
    g.ret(X(d.PI[2]) - 17, Y(61), X(d.PI_USB_ETH_U), Y(18), fill=PRATA, cor=PRETO, w=0.2)
    for u, v in d.PI_FUROS:
        g.circ(X(u), Y(v), 1.4, fill=(0.85, 0.75, 0.3))
    # batente: cantoneiras em L, 1 mm fora do contorno do Pi
    bx0, bx1 = X(d.PI[0]) - 1, X(d.PI[2]) + 1
    by0, by1 = Y(d.PI[3]) - 1, Y(d.PI[1]) + 1
    perna = 9
    for cx, cy, sx, sy in [(bx0, by0, 1, 1), (bx1, by0, -1, 1), (bx0, by1, 1, -1), (bx1, by1, -1, -1)]:
        g.poli([(cx, cy + sy * perna), (cx, cy), (cx + sx * perna, cy)], cor=(0.45, 0.30, 0.15), w=1.6,
               fechar=False)
    # placa de interface (semi-transparente)
    g.ret(X(0), Y(50), X(100), Y(0), fill=(0.98, 0.98, 0.96), cor=(0.3, 0.3, 0.3), w=0.25, op=0.78,
          dashes="[2 1] 0")
    # componentes que importam para a maquete
    pu, pv = d.PECAS["RV1"]
    g.ret(X(pu) - 1.6, Y(pv), X(pu) + 1.6, Y(d.POT_PONTA_V), fill=PRATA, cor=PRETO, w=0.2)
    g.circ(X(pu), Y(pv + 4), 6.5, fill=(0.80, 0.62, 0.25), cor=PRETO, w=0.2)
    lu, lv = d.PECAS["D1"]
    g.circ(X(lu), Y(lv), 2.6, fill=(0.2, 0.9, 0.3), cor=PRETO, w=0.2)
    su, sv = d.PECAS["SW1"]
    g.ret(X(su) - 3, Y(sv) - 3, X(su) + 3, Y(sv) + 3, fill=(0.2, 0.2, 0.2))
    for ref in ("J2", "J3"):
        u, v = d.PECAS[ref]
        g.ret(X(u) - 1.3, Y(v) - 3.8, X(u) + 1.3, Y(v) + 3.8, fill=PRETO)
    u, v = d.PECAS["J4"]
    g.ret(X(u) - 1.3, Y(v) - 5, X(u) + 1.3, Y(v) + 5, fill=PRETO)

    # servos: corpo dentro da guarita, eixo e braço do lado de fora (fundo)
    yb_in = d.GUARITA_Y1 - T
    for x0 in (d.SERVO_E_X0, d.SERVO_S_X0):
        g.ret(x0, yb_in - d.SERVO_ABAIXO_ABA, x0 + d.SERVO_CORPO[0], yb_in, fill=SERVO_AZUL, cor=PRETO, w=0.2)
        g.ret(x0, d.GUARITA_Y1, x0 + d.SERVO_CORPO[0], d.GUARITA_Y1 + 6.8, fill=SERVO_AZUL, cor=PRETO, w=0.2)

    # cabos: servos -> J2/J3 por dentro; sensor -> J4 -> furo; energia -> frente
    cab = (0.95, 0.55, 0.10)
    yv_fundo = (Y(0) + yb_in) / 2          # vão entre a borda da placa e a parede do fundo
    for ref, sx0 in (("J2", d.SERVO_E_X0), ("J3", d.SERVO_S_X0)):
        u, v = d.PECAS[ref]
        cxs = sx0 + d.SERVO_CORPO[0] / 2
        g.poli([(X(u), Y(v)), (X(u), yv_fundo), (cxs + (8 if cxs < X(u) else -8), yv_fundo),
                (cxs, yb_in - d.SERVO_ABAIXO_ABA)], cor=cab, w=0.6, fechar=False)
    u4, v4 = d.PECAS["J4"]
    g.linha(X(u4), Y(v4), (fx0 + fx1) / 2, (fy0 + fy1) / 2, (0.9, 0.9, 0.9), 0.6)
    # o mesmo cabo continua POR BAIXO do piso até o rasgo do sensor (linha oculta)
    g.linha((fx0 + fx1) / 2, (fy0 + fy1) / 2, d.US_X_COSTAS - 1.3, d.US_Y, cab, 0.7, dashes="[4 2] 0")
    xm = X(d.MICRO_USB_U)
    g.ret(xm - 4, -14, xm + 4, Y(d.ENV_V) - 0.5, fill=(0.15, 0.15, 0.15), cor=(0.6, 0.6, 0.6), w=0.2)
    # rede: plugue rígido até o furo da rede; o cabo desce e sai pelos fundos, por baixo
    xe = X(d.PI_USB_ETH_U)
    yr = Y((d.REDE_V[0] + d.REDE_V[1]) / 2)
    rx0, ry0, rx1, ry1 = d.FURO_REDE
    g.ret(rx0, ry0, rx1, ry1, fill=(0.05, 0.05, 0.05), cor=VERMELHO, w=0.35, dashes="[3 2] 0")
    g.ret(xe, yr - 6, xe + d.REDE_PLUGUE, yr + 6, fill=(0.31, 0.61, 0.98), cor=PRETO, w=0.2)
    g.linha((rx0 + rx1) / 2, (ry0 + ry1) / 2, (rx0 + rx1) / 2, d.PISO_D + 8, (0.18, 0.5, 0.93), 0.8, dashes="[4 2] 0")

    # paredes da guarita (papelão)
    gx0, gx1, gy0, gy1 = d.GUARITA_X0, d.GUARITA_X1, d.GUARITA_Y0, d.GUARITA_Y1
    for r in [(gx0, gy0, gx1, gy0 + T), (gx0, gy1 - T, gx1, gy1), (gx0, gy0, gx0 + T, gy1), (gx1 - T, gy0, gx1, gy1)]:
        g.ret(*r, fill=PAPELAO, cor=PRETO, w=0.2)

    for gx0_, gy0_, gx1_, gy1_, _ in d.guias_piso():          # tiras coladas que prendem a guarita
        g.ret(gx0_, gy0_, gx1_, gy1_, fill=(0.62, 0.56, 0.47), cor=PRETO, w=0.15)
    for xa_, ya_, xb_, yb_ in d.fendas_acesso():               # linhas de acesso dos furos (tesoura)
        g.linha(xa_, ya_, xb_, yb_, VERMELHO, 0.4, dashes="[1.5 1] 0")
    g.ret(d.ENERGIA_RASGO[0], gy0, d.ENERGIA_RASGO[2], gy0 + T, fill=(0.05, 0.05, 0.05), cor=VERMELHO, w=0.3)
    g.ret(d.LED_JANELA[0], gy0, d.LED_JANELA[2], gy0 + T, fill=(0.2, 0.9, 0.3), cor=VERMELHO, w=0.3)
    xp = X(d.PECAS["RV1"][0])
    g.ret(xp - d.POT_TUBO_D / 2, d.POT_TUBO_Y[0], xp + d.POT_TUBO_D / 2, d.POT_TUBO_Y[1], fill=(0.98, 0.96, 0.9),
          cor=PRETO, w=0.2)
    g.ret(xp - d.POT_BOTAO / 2, d.POT_TUBO_Y[0], xp + d.POT_BOTAO / 2, d.POT_TUBO_Y[0] + T, fill=(0.82, 0.24, 0.24),
          cor=PRETO, w=0.2)

    # cancelas (fechadas)
    for xe, xf in [(d.CANCELA_E_X, d.ENTRADA_X0 - 1), (d.CANCELA_S_X, min(d.SAIDA_X1 + 1, d.PISO_W - 0.5))]:
        y = d.GUARITA_Y1 + 6.8
        g.ret(min(xe, xf), y, max(xe, xf), y + 3, fill=BRANCO, cor=PRETO, w=0.2)
        passo = 8
        sgn = 1 if xf > xe else -1
        x = xe + sgn * 6
        while (x - xf) * sgn < 0:
            x2 = x + sgn * passo / 2
            if (x2 - xf) * sgn > 0:
                x2 = xf
            g.ret(x, y, x2, y + 3, fill=VERMELHO)
            x += sgn * passo
        g.circ(xe, y + 1.5, 2.2, fill=(0.95, 0.95, 0.95), cor=PRETO, w=0.2)

    # ---------------------------------------------------------------- sensor
    yc = d.US_Y
    xs0 = d.US_X_COSTAS
    xf = xs0 + d.US_PLACA[2]
    ang = math.radians(7.5)
    dx = d.GUARITA_X0 - d.US_X_FACE
    g.poli([(d.US_X_FACE, yc - 8), (d.GUARITA_X0, yc - 8 - dx * math.tan(ang)),
            (d.GUARITA_X0, yc + 8 + dx * math.tan(ang)), (d.US_X_FACE, yc + 8)],
           fill=(1.0, 0.92, 0.3), op=0.30)
    ux0, uy0, ux1, uy1 = d.US_RASGO
    g.ret(ux0, uy0, ux1, uy1, fill=(0.05, 0.05, 0.05), cor=VERMELHO, w=0.3)  # rasgo dos pinos + conector
    ty0, ty1 = yc - d.TOTEM_L / 2, yc + d.TOTEM_L / 2
    AMAR = (0.91, 0.76, 0.35)
    g.ret(d.TOTEM_X0, ty0, d.TOTEM_X0 + T, ty1, fill=AMAR, cor=PRETO, w=0.2)
    for yy in (ty0, ty1 - T):
        g.ret(d.TOTEM_FUNDO_X, yy, d.TOTEM_X0, yy + T, fill=AMAR, cor=PRETO, w=0.2)
    g.ret(xs0, yc - d.US_PLACA[0] / 2, xf, yc + d.US_PLACA[0] / 2, fill=SENSOR_AZUL, cor=PRETO, w=0.2)
    for s in (-1, 1):
        cy = yc + s * 13.5
        g.ret(xf, cy - 8, d.US_X_FACE, cy + 8, fill=PRATA, cor=PRETO, w=0.2)

    g.sh.commit()

    # ---------------------------------------------------------------- textos
    g.texto(gx1 - 62, -3.5, "parede da frente = PAINEL", 2.2, PRETO, negrito=True, centro=False)
    g.texto(gx0 + 4, 1.4, "GUARITA", 2.4, (0.15, 0.15, 0.15), negrito=True, centro=False)
    g.texto(fx0 - 9, (fy0 + fy1) / 2 + 2, "furo de", 2.1, VERMELHO)
    g.texto(fx0 - 9, (fy0 + fy1) / 2 - 2.5, "cabos", 2.1, VERMELHO)
    g.texto(xm + 6, -7.5, "energia (micro-USB)", 2.0, PRETO, centro=False)
    g.texto((rx0 + rx1) / 2, ry1 + 2.4, "furo da rede", 2.1, VERMELHO)
    g.texto((rx0 + rx1) / 2 + 2, (d.GUARITA_Y1 + d.VAGAS_Y0) / 2 - 12, "rede (por baixo)", 1.9,
            (0.55, 0.75, 1.0), centro=False, rot=90)
    g.texto(xp, -7.5, "botão do pot", 2.0, PRETO)
    g.texto(d.LED_JANELA[2] + 1, -12.5, "recorte do LED (no painel)", 2.0, PRETO, centro=False)
    xc = (d.ENTRADA_X0 + d.GUARITA_X0) / 2
    yc_cabo = d.US_Y + ((fy0 + fy1) / 2 - d.US_Y) * (xc - d.US_X_COSTAS) / ((fx0 + fx1) / 2 - d.US_X_COSTAS)
    g.texto(xc, yc_cabo + 3.2, "cabo do sensor", 2.0, BRANCO, negrito=True)
    g.texto(xc, yc_cabo - 4.6, "(por baixo do piso)", 1.9, BRANCO, negrito=True)
    g.texto(d.ENTRADA_X0 + d.FAIXA_ENTRADA / 2, 2.2, "ENTRADA", 2.4, BRANCO, negrito=True)
    g.texto(d.SAIDA_X0 + d.FAIXA_SAIDA / 2, 2.2, "SAÍDA", 2.4, BRANCO, negrito=True)
    g.texto(d.US_X_FACE / 2 + 1, yc + 29, "sensor (totem)", 2.0, BRANCO)
    g.texto((d.ENTRADA_X0 + d.CANCELA_E_X) / 2, d.GUARITA_Y1 + 14, "cancela entrada (servo 1)", 2.0, BRANCO)
    g.texto((d.CANCELA_S_X + d.PISO_W) / 2 - 6, d.GUARITA_Y1 + 14, "cancela saída (servo 2)", 2.0, BRANCO)

    # cotas: largura (embaixo) e profundidade (esquerda)
    yv = -20
    xs = [0, d.ENTRADA_X0, d.GUARITA_X0, d.GUARITA_X1, d.SAIDA_X1, d.PISO_W]
    for a, b in zip(xs, xs[1:]):
        g.cota_h(a, b, yv, f"{b - a:.1f}")
    g.cota_h(0, d.PISO_W, yv - 8, f"{d.PISO_W:.0f}")
    ys = [0, d.GUARITA_Y0, d.GUARITA_Y1, d.VAGAS_Y0, d.PISO_D]
    for a, b in zip(ys, ys[1:]):
        g.cota_v(a, b, -6, f"{b - a:.1f}")
    g.cota_v(0, d.PISO_D, -14, f"{d.PISO_D:.0f}")
    g.cota_h(d.VAGAS_X0, d.VAGAS_X0 + d.VAGA_PASSO, d.PISO_D + 3, f"vaga {d.VAGA_PASSO:.0f} x {d.VAGA_FUNDO:.0f}", acima=True)

    # legenda
    yl = -40
    g.texto(0, yl, f"Planta v5 (tesoura). Piso {d.PISO_W:.0f} x {d.PISO_D:.0f} mm, vista de cima, frente embaixo. "
                   f"Carro {d.CARRO_L:.0f} x {d.CARRO_W:.0f} x {d.CARRO_H:.0f} mm, {d.N_VAGAS} vagas, corredor {d.CORREDOR:.0f} mm.",
            2.5, PRETO, centro=False)
    g.texto(0, yl - 5.5, "Placa de interface tracejada (por cima do Pi verde). Servos em azul, com o corpo dentro da guarita e o braço "
                         "atrás dela. Furos com borda vermelha; tracejado vermelho = linha de acesso. Faixas em etiqueta PIMACO.", 2.3, COTA,
            centro=False)
    furos = [
        ("Furo de cabos (piso, sob a placa)", d.FURO_CABOS),
        ("Furo da rede (piso)", d.FURO_REDE),
        ("Recorte do sensor (aberto na borda esquerda)", d.US_RASGO),
    ]
    yt = yl - 13
    g.texto(0, yt, "Furos e rasgos no piso: X de / até, Y de / até (mm, a partir do canto da frente-esquerda)", 2.3, PRETO,
            negrito=True, centro=False)
    for i, (nome, (a, b, c, e)) in enumerate(furos):
        g.texto(0, yt - 5.2 * (i + 1), f"{nome}: X {a:.1f} / {c:.1f}, Y {b:.1f} / {e:.1f}  ({c - a:.1f} x {e - b:.1f})",
                2.2, COTA, centro=False)
    gx0_ = d.GUARITA_X0
    pot_x = X(d.PECAS["RV1"][0])
    paredes = [
        f"Painel (parede da frente): recortes abertos em cima: tubinho {d.POT_RECORTE[2] - d.POT_RECORTE[0]:.0f} mm de largura "
        f"(centro a {pot_x - gx0_:.1f} da ponta esquerda, até {d.POT_RECORTE[1]:.1f} de altura) e LED "
        f"{d.LED_RECORTE[2] - d.LED_RECORTE[0]:.0f} mm (a {d.LED_RECORTE[0] - gx0_:.1f} da ponta, até {d.LED_RECORTE[1]:.0f});",
        f"recorte da energia {d.ENERGIA_RASGO[2] - d.ENERGIA_RASGO[0]:.0f} x {d.ENERGIA_RASGO[3]:.0f} (de baixo) a "
        f"{d.ENERGIA_RASGO[0] - gx0_:.1f} da ponta. Parede do fundo: 2 recortes abertos embaixo para os servos, "
        f"{d.SERVO_FURO[0]} x {d.SERVO_RECORTE_Z:.2f}, centros a {d.CANCELA_E_X - gx0_:.1f} e {d.CANCELA_S_X - gx0_:.1f} "
        "da ponta esquerda.",
    ]
    for i, t in enumerate(paredes):
        g.texto(0, yt - 5.2 * (len(furos) + 1 + i), t, 2.2, COTA, centro=False)

    for pt, s, fs, fn, cor, rot in g.textos:
        g.page.insert_text(pt, s, fontsize=fs, fontname=fn, color=cor, rotate=rot)

    if saida.lower().endswith(".pdf"):
        g.doc.save(saida)
    else:
        g.page.get_pixmap(dpi=200).save(saida)
    print("gerado:", saida)


if __name__ == "__main__":
    desenhar(sys.argv[1] if len(sys.argv) > 1 else "../previas/planta_v5.png")
