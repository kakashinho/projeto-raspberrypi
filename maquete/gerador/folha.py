# -*- coding: utf-8 -*-
"""Ajudante para desenhar folhas em escala 1:1 com PyMuPDF (tudo em mm, origem no canto de cima)."""
import math

import pymupdf

MM = 72 / 25.4
FONTE = "C:/Windows/Fonts/arial.ttf"
FONTE_B = "C:/Windows/Fonts/arialbd.ttf"
A4 = (210.0, 297.0)
MARGEM = 7.0

PRETO = (0, 0, 0)
CINZA = (0.45, 0.45, 0.45)
CINZA_CLARO = (0.75, 0.75, 0.75)
VERMELHO = (0.85, 0.1, 0.1)
ROSA = (1.0, 0.86, 0.86)
AZUL = (0.15, 0.4, 0.85)
VERDE = (0.2, 0.6, 0.25)
MARROM = (0.55, 0.38, 0.2)
BRANCO = (1, 1, 1)


class Folha:
    def __init__(self, doc, largura=A4[0], altura=A4[1]):
        self.W, self.H = largura, altura
        self.page = doc.new_page(width=largura * MM, height=altura * MM)
        self.page.insert_font(fontname="F0", fontfile=FONTE)
        self.page.insert_font(fontname="F1", fontfile=FONTE_B)
        self.f0 = pymupdf.Font(fontfile=FONTE)
        self.f1 = pymupdf.Font(fontfile=FONTE_B)
        self.sh = self.page.new_shape()
        self.textos = []

    # ------------------------------------------------------------ formas (mm)
    def P(self, x, y):
        return pymupdf.Point(x * MM, y * MM)

    def poly(self, pts, cor=PRETO, fill=None, w=0.3, dashes=None, op=1.0, fechar=True):
        self.sh.draw_polyline([self.P(x, y) for x, y in pts] + ([self.P(*pts[0])] if fechar else []))
        self.sh.finish(color=cor, fill=fill, width=w * MM, dashes=dashes, fill_opacity=op, closePath=False)

    def ret(self, x0, y0, x1, y1, **kw):
        self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], **kw)

    def linha(self, x0, y0, x1, y1, cor=PRETO, w=0.3, dashes=None):
        self.sh.draw_line(self.P(x0, y0), self.P(x1, y1))
        self.sh.finish(color=cor, width=w * MM, dashes=dashes)

    def circ(self, x, y, r, cor=PRETO, fill=None, w=0.3, dashes=None, op=1.0):
        self.sh.draw_circle(self.P(x, y), r * MM)
        self.sh.finish(color=cor, fill=fill, width=w * MM, dashes=dashes, fill_opacity=op)

    def hachura(self, x0, y0, x1, y1, cor=CINZA, passo=1.5, w=0.15):
        """Hachura a 45° dentro do retângulo (área de colagem)."""
        L = (x1 - x0) + (y1 - y0)
        k = 0.0
        while k < L:
            # reta x - y = x0 - y0 + k ... recortada no retângulo
            a = (x0 + k, y0) if k <= x1 - x0 else (x1, y0 + k - (x1 - x0))
            b = (x0, y0 + k) if k <= y1 - y0 else (x0 + k - (y1 - y0), y1)
            self.linha(a[0], a[1], b[0], b[1], cor, w)
            k += passo

    # ------------------------------------------------------------ texto (mm)
    def largura(self, s, tam, negrito=False):
        fs = tam * MM * 1.35
        return (self.f1 if negrito else self.f0).text_length(s, fontsize=fs) / MM

    def texto(self, x, y, s, tam=2.6, cor=PRETO, negrito=False, ancora="e", rot=0):
        """(x, y) = linha de base; ancora 'e' esquerda, 'c' centro, 'd' direita. tam ~ altura da letra (mm)."""
        fs = tam * MM * 1.35
        larg = self.largura(s, tam, negrito)
        dx = {"e": 0, "c": -larg / 2, "d": -larg}[ancora]
        if rot == 0:
            pt = self.P(x + dx, y)
        else:      # 90: texto subindo
            pt = self.P(x, y - dx)
        self.textos.append((pt, s, fs, "F1" if negrito else "F0", cor, rot))

    def textos_bloco(self, x, y, linhas, tam=2.6, entre=1.55, cor=PRETO):
        for i, ln in enumerate(linhas):
            neg = ln.startswith("**")
            self.texto(x, y + i * tam * entre, ln.strip("*"), tam, cor, negrito=neg)
        return y + len(linhas) * tam * entre

    # ------------------------------------------------------------ marcas da folha
    def regua(self, x, y, comp=100.0):
        """Régua de conferência: comp mm (283,46 pt para 100 mm)."""
        self.linha(x, y, x + comp, y, PRETO, 0.35)
        for k in range(0, int(comp) + 1, 5):
            h = 3.0 if k % 10 == 0 else 1.6
            self.linha(x + k, y, x + k, y - h, PRETO, 0.25)
        for k in (0, 50, 100):
            if k <= comp:
                self.texto(x + k, y + 3.2, str(k), 2.0, PRETO, ancora="c")
        self.texto(x + comp + 2, y, f"{comp:.0f} mm: confira com uma régua", 2.2, PRETO)
        self.texto(x, y - 5.5, "IMPRIMIR EM TAMANHO REAL (100 %), sem ajustar à página", 2.4, VERMELHO, negrito=True)
        self.regua_pos = (x, y, comp)

    def cabecalho(self, titulo, sub, pagina):
        m = MARGEM
        self.texto(m, m + 4, titulo, 4.0, PRETO, negrito=True)
        self.texto(self.W - m, m + 4, pagina, 2.6, CINZA, ancora="d")
        self.texto(m, m + 9, sub, 2.4, CINZA)

    def fim(self):
        self.sh.commit()
        for pt, s, fs, fn, cor, rot in self.textos:
            self.page.insert_text(pt, s, fontsize=fs, fontname=fn, color=cor, rotate=rot)


# ---------------------------------------------------------------- peças (contorno local a, b)
def caixa_contorno(c):
    xs = [p[0] for p in c]
    ys = [p[1] for p in c]
    return min(xs), min(ys), max(xs), max(ys)


def mapeador(c, x_pg, y_pg, rot=0, espelho=False):
    """Função (a, b) -> (x, y) na folha. A peça ocupa a caixa a partir de (x_pg, y_pg), com b para cima.
    rot=90 gira a peça 90° (a passa a subir). Devolve (função, largura, altura)."""
    a0, b0, a1, b1 = caixa_contorno(c)
    bw, bh = a1 - a0, b1 - b0
    if rot == 0:
        def M(a, b):
            u = a - a0
            if espelho:
                u = bw - u
            return x_pg + u, y_pg + (bh - (b - b0))
        return M, bw, bh

    def M(a, b):      # gira 90° no sentido anti-horário
        u2 = bh - (b - b0)
        v2 = a - a0
        if espelho:
            u2 = bh - u2
        return x_pg + u2, y_pg + (bw - v2)
    return M, bh, bw


def desenhar_peca(F, it, x_pg, y_pg, rot=0, espelho=False, furos_cor=VERMELHO):
    """Desenha contorno (corte, preto) e furos (vermelho, para recortar)."""
    M, w, h = mapeador(it["c"], x_pg, y_pg, rot, espelho)
    F.poly([M(a, b) for a, b in it["c"]], PRETO, None, 0.3)
    for f in it["f"]:
        if isinstance(f, dict):
            a, b, r = f["c"]
            x, y = M(a, b)
            F.circ(x, y, r, furos_cor, ROSA, 0.3)
            F.linha(x - 1, y, x + 1, y, furos_cor, 0.15)
            F.linha(x, y - 1, x, y + 1, furos_cor, 0.15)
        else:
            F.poly([M(a, b) for a, b in f], furos_cor, ROSA, 0.3)
    return M, w, h


def seta(F, x, y, ang, comp=6, cor=PRETO, w=0.3):
    """Setinha (ang em graus, 0 = direita, 90 = para cima na folha)."""
    r = math.radians(ang)
    dx, dy = math.cos(r), -math.sin(r)
    x1, y1 = x + dx * comp, y + dy * comp
    F.linha(x, y, x1, y1, cor, w)
    for s in (1, -1):
        rr = r + math.pi + s * 0.45
        F.linha(x1, y1, x1 + math.cos(rr) * 1.8, y1 - math.sin(rr) * 1.8, cor, w)
