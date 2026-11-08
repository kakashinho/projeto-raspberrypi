# -*- coding: utf-8 -*-
"""Confere os PDFs de impressão: tamanho da folha, área imprimível, régua de 100 mm e etiquetas.

Uso:  python -B conferir_pdf.py ../impressao
"""
import os
import sys

import numpy as np
import pymupdf

import design as d

MM = 72 / 25.4
MARGEM_MIN = 5.0        # mm: a maioria das impressoras não imprime mais perto da borda


def conteudo(page):
    """Caixas (em mm) do que foi desenhado ou escrito (sem enxergar recortes de páginas embutidas)."""
    caixas = []
    for dr in page.get_drawings():
        r = dr["rect"]
        caixas.append((r.x0 / MM, r.y0 / MM, r.x1 / MM, r.y1 / MM))
    for b in page.get_text("dict")["blocks"]:
        x0, y0, x1, y1 = b["bbox"]
        caixas.append((x0 / MM, y0 / MM, x1 / MM, y1 / MM))
    return caixas


def tinta_na_borda(page, margem=MARGEM_MIN):
    """Renderiza a página e procura qualquer pixel não branco a menos de `margem` mm da borda."""
    pix = page.get_pixmap(dpi=100, colorspace=pymupdf.csRGB)
    a = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)
    m = int(round(margem / 25.4 * 100))
    escuro = a[:, :, :3].min(axis=2) < 245
    faixas = [escuro[:m, :], escuro[-m:, :], escuro[:, :m], escuro[:, -m:]]
    return sum(int(f.sum()) for f in faixas)


def regua_ok(page):
    for dr in page.get_drawings():
        for it in dr["items"]:
            if it[0] == "l":
                p, q = it[1], it[2]
                if abs(p.y - q.y) < 0.01 and abs(abs(q.x - p.x) - 100 * MM) < 0.05:
                    return True
    return False


def main(pasta):
    erros = []
    esperado = {"gabaritos_A4.pdf": "A4", "adesivos_A4.pdf": "A4", "etiquetas_pimaco6282.pdf": "carta",
                "etiquetas_pimaco6282_teste.pdf": "carta"}
    for nome, tipo in esperado.items():
        doc = pymupdf.open(os.path.join(pasta, nome))
        for i, page in enumerate(doc):
            W, H = page.rect.width / MM, page.rect.height / MM
            ok_tam = (abs(min(W, H) - 210) < 0.1 and abs(max(W, H) - 297) < 0.1) if tipo == "A4" else \
                (abs(W - 215.9) < 0.1 and abs(H - 279.4) < 0.1)
            if not ok_tam:
                erros.append(f"{nome} p{i + 1}: folha {W:.1f} x {H:.1f} mm")
            if "teste" not in nome:          # no teste, o contorno das etiquetas vai até a borda (de propósito)
                n = tinta_na_borda(page)
                if n:
                    erros.append(f"{nome} p{i + 1}: {n} pixels impressos a menos de {MARGEM_MIN:.0f} mm da borda")
            if tipo == "A4" and not regua_ok(page):
                erros.append(f"{nome} p{i + 1}: régua de 100 mm não encontrada")
            if nome == "etiquetas_pimaco6282.pdf":
                P = d.PIMACO
                lw, lh = P["etiqueta"]
                gap = P["folha"][0] - 2 * P["margem_lat"] - 2 * lw
                cel = [(P["margem_lat"] + j * (lw + gap), P["margem_sup"] + k * lh) for k in range(7) for j in range(2)]
                for c in conteudo(page):
                    if c[3] < P["margem_sup"] - 1:       # aviso no alto da folha (fora das etiquetas)
                        continue
                    if not any(x - 0.01 <= c[0] and c[2] <= x + lw + 0.01 and y - 0.01 <= c[1] and c[3] <= y + lh + 0.01
                               for x, y in cel):
                        erros.append(f"{nome}: desenho atravessa a borda de uma etiqueta: "
                                     f"({c[0]:.1f}, {c[1]:.1f}) - ({c[2]:.1f}, {c[3]:.1f})")
                        break
        print(f"{nome}: {len(doc)} folha(s)")
    print("OK" if not erros else "PROBLEMAS:\n  " + "\n  ".join(erros))
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "../impressao"))
