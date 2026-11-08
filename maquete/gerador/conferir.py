# -*- coding: utf-8 -*-
"""Confere a montagem: nenhuma peça de papelão pode invadir outra.

Cada peça é um contorno 2D (com furos) extrudado na espessura, igual ao 3D e aos gabaritos.
Se uma aba não tiver o rasgo certo (ou o rasgo estiver no lugar errado), a aba invade a outra
peça e aparece aqui. Também confere se toda aba encosta em alguma peça (não fica no ar).

Uso:  python -B conferir.py
"""
import itertools
import sys

import numpy as np

import design as d
import gerar_3d as g

PASSO = 0.2      # mm, grade de amostragem
EPS = 0.06       # tolerância nas faces (peças encostadas não contam como invasão)


def montar():
    g.piso()
    g.elevacao()
    g.guarita()
    g.eletronica()
    g.totem()
    g.cancelas()
    g.carros()
    return [it for it in g.ITENS if it["k"] == "placa" and it["cod"]]


def para_local(it, P):
    """Pontos do mundo (N x 3, coordenadas da maquete) -> (a, b, w) da peça."""
    ox, oy, oz = it["o"]
    if it["pl"] == "xy":
        return P[:, 0] - ox, P[:, 1] - oy, P[:, 2] - oz
    if it["pl"] == "xz":
        return P[:, 0] - ox, P[:, 2] - oz, P[:, 1] - oy
    return P[:, 1] - oy, P[:, 2] - oz, P[:, 0] - ox


def dentro_poly(a, b, poly, eps):
    """Ray casting vetorizado; eps > 0 encolhe (só o interior conta)."""
    poly = np.asarray(poly, float)
    x0, y0 = poly[:, 0], poly[:, 1]
    x1, y1 = np.roll(x0, -1), np.roll(y0, -1)
    res = np.zeros(a.shape, bool)
    for i in range(len(poly)):
        cond = (y0[i] > b) != (y1[i] > b)
        xint = x0[i] + (b - y0[i]) * (x1[i] - x0[i]) / (y1[i] - y0[i] + 1e-12)
        res ^= cond & (a < xint)
    if eps > 0:   # tira a borda: distância até cada segmento
        dmin = np.full(a.shape, np.inf)
        for i in range(len(poly)):
            vx, vy = x1[i] - x0[i], y1[i] - y0[i]
            L2 = vx * vx + vy * vy + 1e-12
            t = np.clip(((a - x0[i]) * vx + (b - y0[i]) * vy) / L2, 0, 1)
            dmin = np.minimum(dmin, np.hypot(a - (x0[i] + t * vx), b - (y0[i] + t * vy)))
        res &= dmin > eps
    return res


def furo_poly(f):
    if isinstance(f, dict):
        a, b, r = f["c"]
        ang = np.linspace(0, 2 * np.pi, 48, endpoint=False)
        return np.c_[a + r * np.cos(ang), b + r * np.sin(ang)]
    return f


def solido(it, P, eps=EPS):
    a, b, w = para_local(it, P)
    m = (w > eps) & (w < it["t"] - eps) & dentro_poly(a, b, it["c"], eps)
    for f in it["f"]:
        m &= ~dentro_poly(a, b, furo_poly(f), -1)
    return m


def caixa(it):
    """Caixa envolvente no mundo."""
    c = np.asarray(it["c"], float)
    a0, b0 = c.min(0)
    a1, b1 = c.max(0)
    ox, oy, oz = it["o"]
    t = it["t"]
    if it["pl"] == "xy":
        return np.array([ox + a0, oy + b0, oz]), np.array([ox + a1, oy + b1, oz + t])
    if it["pl"] == "xz":
        return np.array([ox + a0, oy, oz + b0]), np.array([ox + a1, oy + t, oz + b1])
    return np.array([ox, oy + a0, oz + b0]), np.array([ox + t, oy + a1, oz + b1])


def grade(lo, hi):
    eixos = [np.arange(lo[k] + PASSO / 2, hi[k], PASSO) for k in range(3)]
    if any(len(e) == 0 for e in eixos):
        return np.zeros((0, 3))
    X, Y, Z = np.meshgrid(*eixos, indexing="ij")
    return np.c_[X.ravel(), Y.ravel(), Z.ravel()]


def nome(it):
    return f"{it['cod']} ({it['n'] or it['cod']})"


def main():
    pecas = montar()
    caixas = [caixa(it) for it in pecas]
    problemas = 0
    pares = 0
    for (i, A), (j, B) in itertools.combinations(enumerate(pecas), 2):
        (la, ha), (lb, hb) = caixas[i], caixas[j]
        lo, hi = np.maximum(la, lb), np.minimum(ha, hb)
        if np.any(hi - lo <= 0.1):
            continue
        if A.get("u") != B.get("u") and (A.get("u") or B.get("u")) and not (A["cod"] in ("P1", "EVA") or B["cod"] in ("P1", "EVA")):
            pass
        P = grade(lo, hi)
        if len(P) == 0:
            continue
        pares += 1
        m = solido(A, P) & solido(B, P)
        if m.any():
            problemas += 1
            q = P[m]
            print(f"INVASÃO: {nome(A)} x {nome(B)}: {m.sum()} pontos, em X {q[:, 0].min():.1f}-{q[:, 0].max():.1f}, "
                  f"Y {q[:, 1].min():.1f}-{q[:, 1].max():.1f}, Z {q[:, 2].min():.1f}-{q[:, 2].max():.1f}")
    print(f"{len(pecas)} peças, {pares} pares que se tocam conferidos, {problemas} invasões")
    # eletrônica e plugues contra o papelão
    elet = [it for it in g.ITENS if it["k"] in ("caixa", "cil") and it["g"] in ("eletronica", "cabos")]
    choques = 0
    for E in elet:
        if E["k"] == "caixa":
            le, he = np.minimum(E["a"], E["b"]), np.maximum(E["a"], E["b"])
        else:
            p = np.array(E["p"], float)
            ax = "xyz".index(E["ax"])
            le, he = p - E["r"], p + E["r"]
            le[ax], he[ax] = p[ax], p[ax] + E["h"]
        for i, B in enumerate(pecas):
            lo, hi = np.maximum(le, caixas[i][0]), np.minimum(he, caixas[i][1])
            if np.any(hi - lo <= 0.1):
                continue
            P = grade(lo, hi)
            if len(P) == 0:
                continue
            if E["k"] == "caixa":
                mE = np.all((P > le + EPS) & (P < he - EPS), axis=1)
            else:
                outros = [k for k in range(3) if k != ax]
                r2 = ((P[:, outros[0]] - p[outros[0]]) ** 2 + (P[:, outros[1]] - p[outros[1]]) ** 2)
                mE = (r2 < (E["r"] - EPS) ** 2) & (P[:, ax] > le[ax] + EPS) & (P[:, ax] < he[ax] - EPS)
            m = mE & solido(B, P)
            if m.any():
                choques += 1
                q = P[m]
                print(f"CHOQUE: eletrônica {E['k']} em X {le[0]:.1f}-{he[0]:.1f} Y {le[1]:.1f}-{he[1]:.1f} "
                      f"Z {le[2]:.1f}-{he[2]:.1f} x {nome(B)}: em X {q[:, 0].min():.1f}-{q[:, 0].max():.1f}, "
                      f"Y {q[:, 1].min():.1f}-{q[:, 1].max():.1f}, Z {q[:, 2].min():.1f}-{q[:, 2].max():.1f}")
    print(f"{len(elet)} peças de eletrônica/plugues conferidas, {choques} choques")
    problemas += choques
    erros = d.checar()
    print("design.checar():", "OK" if not erros else "; ".join(erros))
    return 1 if (problemas or erros) else 0


if __name__ == "__main__":
    sys.exit(main())
